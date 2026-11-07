"""CSV file handling utilities for the T-TEA platform.

This module provides a CSVHandler class for reading and writing CSV files
with a custom dialect and robust error handling.
"""

import csv
import io
import locale
import os
from pathlib import Path
from typing import Dict, List, Optional, TextIO, Union


class CSVHandler:
    """
    A class for handling CSV files with a custom dialect.

    Fully integrated with the application's singleton logger. Works with file
    paths or already-opened file-like objects (e.g., locked via portalocker).
    Handles common real-world issues: file locked by Excel, wrong
    encoding, corrupted files, missing directories, permission errors, etc.

    Parameters
    ----------
    dialect : str, default "custom_ttea"
        Name of the CSV dialect to register and use.
    delimiter : str, default ";"
        Field delimiter character.
    quotechar : str, default '"'
        Character used to quote fields containing special characters.
    doublequote : bool, default True
        Controls how quotechar instances inside fields are handled.
    skipinitialspace : bool, default True
        When True, whitespace immediately following the delimiter is ignored.
    lineterminator : str, default "\n"
        String used to terminate lines produced by the writer.
    quoting : int, default csv.QUOTE_MINIMAL
        Controls quoting behavior (one of csv.QUOTE_* constants).

    Attributes
    ----------
    dialect : str
        Registered CSV dialect name.
    log : Log
        Singleton logger instance used by the handler.

    Methods
    -------
    __init__(...)
        Initialise the handler and register the custom CSV dialect.
    write_csv(file_or_path, data, headers=None)
        Write data to a CSV file or an already-opened file object.
    read_csv(filename, as_dict=False)
        Read a CSV file safely, returning an empty list on any error.

    Examples
    --------
    >>> handler = CSVHandler()
    >>> handler.write_csv("test.csv", [["a", "b"], ["1", "2"]])
    """

    def __init__(
        self,
        dialect: str = "custom_ttea",  # custom dialect name to avoid conflicts
        delimiter: str = ";",
        quotechar: str = '"',
        doublequote: bool = True,
        skipinitialspace: bool = True,
        lineterminator: str = "\n",
        quoting: int = csv.QUOTE_MINIMAL,
    ) -> None:
        """
        Register a custom CSV dialect and prepare the handler.

        Parameters
        ----------
        dialect : str, default "custom_ttea"
            Name of the dialect to register.
        delimiter : str, default ";"
            Character separating fields.
        quotechar : str, default '"'
            Character for quoting fields.
        doublequote : bool, default True
            Handling of quotechar inside fields.
        skipinitialspace : bool, default True
            Ignore whitespace after delimiter.
        lineterminator : str, default "\n"
            Line terminator for writing.
        quoting : int, default csv.QUOTE_MINIMAL
            Quoting policy (csv.QUOTE_* constants).
        """
        # Singleton logger for the application
        from ttea.log import Log

        csv.register_dialect(
            dialect,
            delimiter=delimiter,
            quotechar=quotechar,
            doublequote=doublequote,
            skipinitialspace=skipinitialspace,
            lineterminator=lineterminator,
            quoting=quoting,
        )
        self.dialect = dialect
        # Same logger used throughout the application
        self.log = Log.get_log()

    def write_csv(
        self,
        file_or_path: Union[str, os.PathLike, TextIO],
        data: List[Union[Dict, List]],
        headers: Optional[List[str]] = None,
    ) -> None:
        """
        Write a list of rows or dictionaries to CSV.

        Creates parent directories if needed. Works with a file path or an
        already-opened file-like object (e.g., locked with portalocker).

        Parameters
        ----------
        file_or_path : str, PathLike or file-like
            Destination file path or an open file object.
        data : list of dict or list of list
            Rows to write. Dictionaries require ``headers``.
        headers : list of str, optional
            Field names when writing dictionaries. If provided, a header
            row is written first.

        Returns
        -------
        None
            The CSV file is written to disk or the open file object.

        Notes
        -----
        Logs success or raises logged exceptions on failure.
        """
        if isinstance(file_or_path, (str, os.PathLike)):
            path = Path(file_or_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            try:
                with open(path, "w", newline="", encoding="utf-8-sig") as f:
                    self._write_to_file(f, data, headers)
                self.log.log_info(f"CSV saved successfully: {path.name}")
            except Exception as e:
                self.log.log_error(f"Failed to save CSV {path}: {e}")
                raise
        else:
            # File already open (e.g., portalocker.Lock)
            try:
                self._write_to_file(file_or_path, data, headers)
                # Does not log file name here because we don't have the path
            except Exception as e:
                self.log.log_error(f"Failed to write to locked CSV file: {e}")
                raise

    def _write_to_file(
        self,
        file: TextIO,
        data: List[Union[Dict, List]],
        headers: Optional[List[str]],
    ) -> None:
        """Write rows to an already-opened file object using the registered
        dialect.

        This is an internal helper called by :meth:`write_csv`. It assumes the
        file is open in text mode with proper encoding and newline=''.

        Parameters
        ----------
        file : TextIO
            Open file object ready for writing.
        data : list of dict or list of list
            Data rows to write.
        headers : list of str or None
            Field names for DictWriter, or None to write plain rows.

        Returns
        -------
        None
            Writes rows to the open file object.
        """
        if headers:
            writer = csv.DictWriter(
                file, fieldnames=headers, dialect=self.dialect
            )
            writer.writeheader()
            writer.writerows(data)
        else:
            writer = csv.writer(file, dialect=self.dialect)
            writer.writerows(data)

    def read_csv(
        self,
        filename: Optional[Union[str, os.PathLike]] = None,
        as_dict: bool = False,
        content: Optional[str] = None,
    ) -> List[Union[Dict, List]]:
        """
        Read a CSV file with comprehensive error handling.

        Returns an empty list instead of raising exceptions for any problem
        (file missing, locked by Excel, wrong encoding, corrupted, etc.).
        This guarantees the application never crashes due to CSV issues.

        Parameters
        ----------
        filename : str or PathLike, optional
            Path to the CSV file.
        as_dict : bool, default False
            If True, returns a list of dictionaries (using first row as keys).
        content : str, optional
            CSV content provided directly as a string.

        Returns
        -------
        list
            List of rows (dicts if ``as_dict=True``, otherwise lists).
            Empty list on any read error.

        Notes
        -----
        If ``content`` is provided, the ``filename`` parameter is ignored.

        Examples
        --------
        >>> handler = CSVHandler()
        >>> handler.read_csv(content='a;b\n1;2', as_dict=False)
        [['a', 'b'], ['1', '2']]
        """
        if content is not None:
            try:
                f = io.StringIO(content)
                if as_dict:
                    reader = csv.DictReader(f, dialect=self.dialect)
                else:
                    reader = csv.reader(f, dialect=self.dialect)
                return list(reader)
            except Exception as e:
                self.log.log_error(f"Error reading CSV content: {e}")
                return []

        path = Path(filename)

        if not path.exists():
            self.log.log_info(
                f"CSV file does not exist (normal on first run): {path.name}"
            )
            return []

        # List optimized and tested for PT-BR/PT-PT, Spanish, and English
        # on Windows, Linux, and Mac
        system_enc = locale.getpreferredencoding(False)
        encodings_to_try = ["utf-8-sig", "cp1252", "utf-8", "latin1"]

        # Avoids duplicates if system_enc is already in the list
        if system_enc.lower() not in [e.lower() for e in encodings_to_try]:
            encodings_to_try.insert(1, system_enc)

        for encoding in encodings_to_try:
            try:
                with open(path, "r", newline="", encoding=encoding) as file:

                    if as_dict:
                        reader = csv.DictReader(file, dialect=self.dialect)
                    else:
                        reader = csv.reader(file, dialect=self.dialect)

                    rows = list(reader)
                    return rows
            except PermissionError:
                self.log.log_warning(
                    f"CSV file locked (probably open in Excel): {path.name}"
                )
                return []
            except UnicodeDecodeError:
                continue
            except (OSError, csv.Error) as e:
                self.log.log_error(
                    f"Error reading CSV {path.name} with {encoding}: {type(e).__name__}: {e}"
                )
                return []
        self.log.log_error(
            f"Could not decode CSV {path.name}. "
            f"Encodings tried: {', '.join(encodings_to_try)}"
        )
        return []
