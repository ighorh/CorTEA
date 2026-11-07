"""Logging utilities for the T-TEA Qt application.

This module provides a singleton Log class for application diagnostics,
including rotating file logging, system information capture, and exception
stack trace reporting.
"""

import importlib.metadata
import json
import logging
import os
import platform
import sys
import traceback
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, Optional

import psutil

from ttea.util import PathConfig


class Log:
    """Logging manager for application diagnostics and exceptions.

    This singleton class configures a rotating log file handler and provides
    methods to record informational events, warnings, and errors. It also
    collects system and Python environment data for richer diagnostics.

    Attributes
    ----------
    LOG_FILE_NAME : str
        Default log file name used for logging.
    LOG_FILE_PATH : str
        Default resolved path for the log file.
    _instance : Optional[Log]
        Cached singleton instance.

    Methods
    -------
    __new__(cls, *args, **kwargs)
        Create or return the singleton Log instance.
    __init__(log_file=None, log_level=logging.DEBUG)
        Initialize the logger and configure file handling.
    get_log()
        Retrieve the singleton Log instance.
    ensure_log_directory_exists()
        Create the log directory if necessary.
    get_system_info()
        Return system and hardware diagnostics.
    get_python_info()
        Return Python environment diagnostics.
    log_system_info()
        Write system and Python environment information to the log.
    log_error_with_stack(exception, variables=None, traceback_obj=None)
        Log exceptions with stack traces and optional context.
    log_info(message)
        Write an informational message to the log.
    log_warning(message)
        Write a warning message to the log.
    log_error(message)
        Write an error message to the log.

    Examples
    --------
    >>> log = Log.get_log()
    >>> log.log_info("Application started")
    >>> try:
    ...     x = 1 / 0
    ... except Exception as e:
    ...     log.log_error_with_stack(e, variables={"x": 0})
    """

    LOG_FILE_NAME = "tteaapp.log"
    LOG_FILE_PATH = PathConfig.log(LOG_FILE_NAME)
    _instance = None

    def __new__(cls, *args: tuple, **kwargs: dict) -> "Log":
        """Implements the Singleton pattern to ensure a single instance of
        the Log class.

        Parameters
        ----------
        cls : type
            The class being instantiated.
        *args : tuple
            Variable length argument list.
        **kwargs : dict
            Arbitrary keyword arguments.

        Returns
        -------
        Log
            The singleton instance of the Log class.

        Notes
        -----
        If no instance exists, a new one is created. Otherwise, the existing
        instance is returned.
        """
        if cls._instance is None:
            cls._instance = super(Log, cls).__new__(cls)
        return cls._instance

    def __init__(
        self, log_file: Optional[str] = None, log_level: int = logging.DEBUG
    ) -> None:
        """Initialize the logger with an optional file and log level.

        Parameters
        ----------
        log_file : str, optional
            Path to the log file. If None, uses `LOG_FILE_PATH`.
        log_level : int, optional
            Logging level such as logging.DEBUG or logging.INFO.
            Defaults to logging.DEBUG.

        Returns
        -------
        None

        Notes
        -----
        Creates the log directory if it does not exist.
        Configures a rotating file handler with a maximum size of 10 MiB and
        up to five backup files.
        Clears existing handlers to prevent duplicate output.
        """

        # Use default file if none specified
        self.log_file = log_file if log_file else self.LOG_FILE_PATH
        # Ensure log directory exists
        self.ensure_log_directory_exists()
        # Configure logger
        self.logger = logging.getLogger("Log")
        self.logger.setLevel(log_level)
        # Clear existing handlers to avoid duplicates
        if self.logger.handlers:
            self.logger.handlers.clear()
        # Configure rotating file handler (10MB per file, keep 5 backups)
        file_handler = RotatingFileHandler(
            self.log_file, maxBytes=10 * 1024 * 1024, backupCount=5
        )
        file_handler.setLevel(log_level)
        # Define log format
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        # Add handler to logger
        self.logger.addHandler(file_handler)
        self.logger.info("Log instance initialized.")

    @classmethod
    def get_log(cls) -> "Log":
        """Retrieve the singleton instance of the Log class.

        Parameters
        ----------
        cls : type
            The Log class.

        Returns
        -------
        Log
            The singleton instance of the Log class.

        Notes
        -----
        If no instance exists, a new one is created with default parameters.
        """
        if cls._instance is None:
            cls._instance = Log()
        return cls._instance

    def ensure_log_directory_exists(self) -> None:
        """Ensure the log directory exists, creating it if necessary.

        Returns
        -------
        None

        Notes
        -----
        Uses `os.makedirs` to create the directory tree for the log file path
        if it does not exist.
        """
        log_dir = os.path.dirname(os.path.abspath(self.log_file))
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def get_system_info(self) -> Dict[str, str]:
        """Retrieve system, hardware, and memory information.

        Returns
        -------
        Dict[str, str]
            Dictionary containing system information such as OS, processor,
            CPU cores, and memory usage.

        Notes
        -----
        - Uses `platform` module for system and hardware details.
        - Uses `psutil` for CPU and memory information.
        - Memory values are rounded for readability.
        """
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        info = {
            "OS": platform.system(),
            "OS Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "CPU Cores": psutil.cpu_count(logical=True),
            "Memory Total (GB)": round(
                psutil.virtual_memory().total / (1024**3), 2
            ),
            "Memory Used by App (MB)": round(memory_info.rss / (1024**2), 2),
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        return info

    def get_python_info(self) -> Dict[str, str]:
        """Retrieve Python installation and installed package information.

        Returns
        -------
        Dict[str, str]
            Dictionary containing Python version, executable path, and
            installed packages.

        Notes
        -----
        - Uses `importlib.metadata` to list installed packages.
        - Packages are sorted alphabetically and formatted as "name==version".
        """
        # Get installed packages
        packages = sorted(
            [
                f"{dist.metadata['Name']}=={dist.version}"
                for dist in importlib.metadata.distributions()
            ]
        )
        packages_str = ", ".join(packages) if packages else "No packages found"
        info = {
            "Python Version": sys.version,
            "Python Executable": sys.executable,
            "Installed Packages": packages_str,
        }
        return info

    def log_system_info(self) -> None:
        """Log system and Python environment information to the log file.

        Returns
        -------
        None

        Notes
        -----
        - Calls `get_system_info` and `get_python_info` to gather information.
        - Logs each key-value pair as an INFO-level message.
        """
        # Log system information
        self.logger.info("System Information:")
        system_info = self.get_system_info()
        for key, value in system_info.items():
            self.logger.info("%s: %s", key, value)
        # Log Python environment information
        self.logger.info("Python Environment Information:")
        python_info = self.get_python_info()
        for key, value in python_info.items():
            self.logger.info("%s: %s", key, value)

    def log_error_with_stack(
        self,
        exception: Exception,
        variables: Optional[Dict[str, Any]] = None,
        traceback_obj: Optional[Any] = None,
    ) -> None:
        """Log an error with stack trace and optional context.

        Parameters
        ----------
        exception : Exception
            The exception to log.
        variables : Dict[str, Any], optional
            Variables to include in the log output.
        traceback_obj : Any, optional
            Traceback object to format. If None, uses the current exception
            traceback.

        Returns
        -------
        None

        Notes
        -----
        Logs provided variables and non-builtin local variables from the
        caller frame. Also logs system and Python environment details.
        """
        # Log provided variables if any
        if variables:
            self.logger.error("Provided variables at the time of error:")
            for key, value in variables.items():
                formatted_value = json.dumps(value, indent=2, default=str)
                self.logger.error("%s: %s", key, formatted_value)
        # Capture local variables from the caller's frame
        caller_frame = sys._getframe(1)
        local_vars = caller_frame.f_locals
        if local_vars:
            self.logger.error("Local variables at the time of error:")
            for key, value in local_vars.items():
                # Filters Python built-in variables (starting with '__')
                if not key.startswith("__"):
                    formatted_value = json.dumps(value, indent=2, default=str)
                    self.logger.error("%s: %s", key, formatted_value)
        # System Information
        self.logger.error("Error detected. System information:")
        system_info = self.get_system_info()
        for key, value in system_info.items():
            self.logger.error("%s: %s", key, value)
        # Python information
        self.logger.error("Python Environment Information:")
        python_info = self.get_python_info()
        for key, value in python_info.items():
            self.logger.error("%s: %s", key, value)
        # Error message and stack trace
        self.logger.error("Exception: %s", str(exception))
        if traceback_obj:
            stack_trace = "".join(traceback.format_tb(traceback_obj))
            self.logger.error("Execution stack:\n%s", stack_trace)
        else:
            stack_trace = traceback.format_exc()
            self.logger.error(
                "Execution stack:\n%s",
                stack_trace if stack_trace else "No stack trace available",
            )

    def log_info(self, message: str) -> None:
        """Log an informational message.

        Parameters
        ----------
        message : str
            The message to log at the INFO level.

        Returns
        -------
        None
        """
        self.logger.info(message)

    def log_warning(self, message: str) -> None:
        """Log a warning message.

        Parameters
        ----------
        message : str
            The message to log at the WARNING level.

        Returns
        -------
        None
        """
        self.logger.warning(message)

    def log_error(self, message: str) -> None:
        """Log an error message.

        Parameters
        ----------
        message : str
            The message to log at the ERROR level.

        Returns
        -------
        None
        """
        self.logger.error(message)
