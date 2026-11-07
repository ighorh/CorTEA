"""Global exception hook utilities for the T-TEA application.

This module installs hooks for uncaught exceptions in the main thread
and worker threads. It also shows an error dialog using translated
messages when Qt is available.
"""

import sys
import threading
from types import TracebackType

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication


class CriticalHooks:
    """Encapsulate global exception hooks for the application.

    This class registers handlers for uncaught exceptions in the main
    thread and worker threads, and displays a translated error dialog when
    Qt is available.

    Methods
    -------
    show_critical_error(exception)
        Display a translated critical error dialog for the given exception.
    global_exception_hook(exctype, value, traceback_obj)
        Handle uncaught exceptions on the main thread.
    threading_exception_hook(args)
        Handle uncaught exceptions in worker threads.
    setup_exception_hooks()
        Register global exception hooks for the application.

    Notes
    -----
    The class uses QCoreApplication.translate for translated error text.
    This mapping is intended for localized internationalization.

    Examples
    --------
    >>> CriticalHooks.setup_exception_hooks()
    """

    @staticmethod
    def show_critical_error(exception: BaseException) -> None:
        """Show a translated critical error dialog.

        Parameters
        ----------
        exception : BaseException
            The exception that caused the failure.

        Returns
        -------
        None

        Notes
        -----
        If the Qt message dialog cannot be displayed, falls back to printing
        the error to standard output.
        """
        from ttea.util import MessageService

        message = QCoreApplication.translate(
            "CriticalHooks",
            "Ocorreu um erro inesperado e o aplicativo será encerrado.\n"
            "Por favor, entre em contato com o suporte e envie o arquivo de log.\n"
            "Detalhes do erro: {0}",
        ).format(str(exception))

        try:
            MessageService.critical_global(message, None)
        except Exception:
            # Fallback in case the dialog fails or Qt is not yet ready
            print("Critical error (failed to display dialogue): ", exception)

    @staticmethod
    def global_exception_hook(
        exctype: type[BaseException],
        value: BaseException,
        traceback_obj: TracebackType | None,
    ) -> None:
        """Handle uncaught exceptions on the main thread.

        Parameters
        ----------
        exctype : type[BaseException]
            The exception class.
        value : BaseException
            The exception instance.
        traceback_obj : TracebackType | None
            The traceback object, if available.

        Returns
        -------
        None

        Notes
        -----
        The hook logs the exception and shows a dialog only if a
        QApplication instance exists. The application exits with status 1.
        """
        from ttea.log import Log

        Log.get_log().log_error("Untreated global exception")
        Log.get_log().log_error_with_stack(value, traceback_obj=traceback_obj)

        # Only attempt to show the interface if the QApplication already exists
        if QApplication.instance() is not None:
            try:
                CriticalHooks.show_critical_error(value)
            except Exception:
                print("Critical error (failed to display dialogue).")
        else:
            print("Critical error before QApplication initialization:", value)

        sys.__excepthook__(exctype, value, traceback_obj)
        sys.exit(1)

    @staticmethod
    def threading_exception_hook(args: threading.ExceptHookArgs) -> None:
        """Handle uncaught exceptions in worker threads.

        Parameters
        ----------
        args : threading.ExceptHookArgs
            Thread exception hook arguments.

        Returns
        -------
        None

        Notes
        -----
        This hook only logs the exception and does not show a dialog to
        avoid thread safety issues with Qt widgets.
        """
        from ttea.log import Log

        Log.get_log().log_error("Untreated exception in thread")
        Log.get_log().log_error_with_stack(
            args.exc_value, traceback_obj=args.exc_traceback
        )

    @staticmethod
    def setup_exception_hooks() -> None:
        """Register global exception hooks for the application.

        Returns
        -------
        None
        """
        sys.excepthook = CriticalHooks.global_exception_hook
        threading.excepthook = CriticalHooks.threading_exception_hook
