"""Application configuration constants and helper methods.

This module centralizes application path constants, version information,
format settings, and helper methods for translated titles and config
file checks.
"""

from PySide6.QtCore import QCoreApplication, QSettings

from ttea.util import PathConfig


class AppConfig:
    """Hold application configuration constants and helper methods.

    Attributes
    ----------
    ICON_APP : str
        Path to the application icon file resolved by PathConfig.
    LOGO_APP : str
        Path to the application logo file resolved by PathConfig.
    PLATAFORM_SUFIX : str
        Suffix identifier for the platform.
    PLATAFORM_MANUAL : str
        Identifier for the platform manual.
    VERSION : str
        Current application version string.
    DEFAULT_DATE_FORMAT : str
        Default date format string used when language is not en_US.
    DEFAULT_HOUR_FORMAT : str
        Default hour format string used when language is not en_US.
    DEFAULT_HOUR_MINUTE_FORMAT : str
        Default hour-minute format string used when language is not en_US.
    SETTINGS_GERAL : str
        Base key for general settings.
    SETTINGS_GERAL_DATE_MASK : str
        Settings key for the date format mask.
    SETTINGS_GERAL_HOUR_MASK : str
        Settings key for the hour format mask.
    SETTINGS_GERAL_HOUR_MINUTE_MASK : str
        Settings key for the hour-minute format mask.
    SETTINGS_GERAL_LANGUAGE : str
        Settings key for the language preference.
    SETTINGS_GERAL_VERSION : str
        Settings key for the application version.
    USA_DATE_FORMAT : str
        Alternative date format string used for English locale.
    USA_HOUR_FORMAT : str
        Alternative hour format string used for English locale.
    USA_HOUR_MINUTE_FORMAT : str
        Alternative hour-minute format string used for English locale.
    TRANSLATION_EXTENSION : str
        File extension for Qt translation files.

    Methods
    -------
    get_title()
        Return the translated application title.
    get_geral_date_mask()
        Return the configured general date format mask.
    get_geral_hour_mask()
        Return the configured general hour format mask.
    get_geral_hour_minute_mask()
        Return the configured general hour-minute format mask.
    config_file_exists(filename)
        Check whether the configuration file exists.

    Examples
    --------
    >>> AppConfig.get_title()
    'Plataforma T-TEA'
    >>> AppConfig.config_file_exists()
    True
    """

    ICON_APP: str = PathConfig.icon_system("appicon")
    LOGO_APP: str = PathConfig.image("ttealogo")
    PLATAFORM_SUFFIX: str = "TEA"
    PLATAFORM_MANUAL: str = "Manual"
    VERSION: str = "2.0"

    DEFAULT_DATE_FORMAT: str = "%d/%m/%Y"
    DEFAULT_HOUR_FORMAT: str = "%H:%M:%S"
    DEFAULT_HOUR_MINUTE_FORMAT: str = "%H:%M"
    SETTINGS_GERAL: str = "geral"
    SETTINGS_GERAL_DATE_MASK: str = f"{SETTINGS_GERAL}/date_mask"
    SETTINGS_GERAL_HOUR_MASK: str = f"{SETTINGS_GERAL}/hour_mask"
    SETTINGS_GERAL_HOUR_MINUTE_MASK: str = f"{SETTINGS_GERAL}/hour_minute_mask"
    SETTINGS_GERAL_LANGUAGE: str = f"{SETTINGS_GERAL}/language"
    SETTINGS_GERAL_VERSION: str = f"{SETTINGS_GERAL}/version"
    USA_DATE_FORMAT: str = "%m/%d/%Y"
    USA_HOUR_FORMAT: str = "%I:%M:%S %p"
    USA_HOUR_MINUTE_FORMAT: str = "%I:%M %p"
    TRANSLATION_EXTENSION: str = ".qm"

    @staticmethod
    def get_title() -> str:
        """Return the translated application title.

        Returns
        -------
        str
            The translated title of the T-TEA platform.

        Notes
        -----
        Uses QCoreApplication.translate to ensure the title is translated
        according to the current language settings.

        Examples
        --------
        >>> AppConfig.get_title()
        'Plataforma T-TEA'
        """
        return QCoreApplication.translate("TTeaApp", "Plataforma T-TEA")

    @staticmethod
    def get_geral_date_mask() -> str:
        """Return the general date mask from settings or a fallback.

        Returns
        -------
        str
            The date format mask to use for general display.

        Notes
        -----
        If a general date mask setting exists, it is returned. Otherwise,
        the method returns USA_DATE_FORMAT for English and
        DEFAULT_DATE_FORMAT for other languages.

        Examples
        --------
        >>> AppConfig.get_geral_date_mask()
        '%d/%m/%Y'
        """
        from ttea.model import AppModel

        settings = QSettings(PathConfig.config(), QSettings.IniFormat)
        saved_mask = settings.value(AppConfig.SETTINGS_GERAL_DATE_MASK)

        if saved_mask:  # Allow future manual override
            return saved_mask

        # Uses the current language, already validated
        # and with a fallback guaranteed by AppModel
        return (
            AppConfig.USA_DATE_FORMAT
            if AppModel().current_language == "en_US"
            else AppConfig.DEFAULT_DATE_FORMAT
        )

    @staticmethod
    def get_geral_hour_mask() -> str:
        """Return the general hour mask from settings or a fallback.

        Returns
        -------
        str
            The hour format mask to use for general display.

        Notes
        -----
        If a general hour mask setting exists, it is returned. Otherwise,
        the method returns USA_HOUR_FORMAT for English and
        DEFAULT_HOUR_FORMAT for other languages.

        Examples
        --------
        >>> AppConfig.get_geral_hour_mask()
        '%H:%M:%S'
        """
        from ttea.model import AppModel

        settings = QSettings(PathConfig.config(), QSettings.IniFormat)
        saved_mask = settings.value(AppConfig.SETTINGS_GERAL_HOUR_MASK)

        if saved_mask:  # Allow future manual override
            return saved_mask

        # Uses the current language, already validated
        # and with a fallback guaranteed by AppModel
        return (
            AppConfig.USA_HOUR_FORMAT
            if AppModel().current_language == "en_US"
            else AppConfig.DEFAULT_HOUR_FORMAT
        )

    @staticmethod
    def get_geral_hour_minute_mask() -> str:
        """Return the general hour-minute mask from settings or a fallback.

        Returns
        -------
        str
            The hour-minute format mask to use for general display.

        Notes
        -----
        If a general hour-minute mask setting exists, it is returned. Otherwise,
        the method returns USA_HOUR_MINUTE_FORMAT for English and
        DEFAULT_HOUR_MINUTE_FORMAT for other languages.

        Examples
        --------
        >>> AppConfig.get_geral_hour_minute_mask()
        '%I:%M %p'
        """
        from ttea.model import AppModel

        settings = QSettings(PathConfig.config(), QSettings.IniFormat)
        saved_mask = settings.value(AppConfig.SETTINGS_GERAL_HOUR_MINUTE_MASK)

        if saved_mask:  # Allow future manual override
            return saved_mask

        # Uses the current language, already validated
        # and with a fallback guaranteed by AppModel
        return (
            AppConfig.USA_HOUR_MINUTE_FORMAT
            if AppModel().current_language == "en_US"
            else AppConfig.DEFAULT_HOUR_MINUTE_FORMAT
        )

    @staticmethod
    def config_file_exists(filename: str = PathConfig.CONFIG_FILENAME) -> bool:
        """Check whether the configuration file exists.

        Parameters
        ----------
        filename : str
            Name of the configuration file to check.

        Returns
        -------
        bool
            True if the configuration file exists, False otherwise.

        Examples
        --------
        >>> AppConfig.config_file_exists()
        True
        """
        return PathConfig.config_file_exists(filename)
