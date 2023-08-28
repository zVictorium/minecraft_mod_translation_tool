import os
import json
import re

# Constants
CONFIG_JSON_PATH = 'config.json'

ORIGINAL_LANG = 'original_language'
TARGET_LANG = 'target_language'
MODS_PATH = 'mods_path'
TRANSLATION_PATH = 'translation_path'
REPLACE_ORIGINAL_MODS = 'replace_original_mods'


class Settings:
    """
    The Settings class is responsible for managing configuration settings
    for this Minecraft translation tool. It reads configuration data from the
    configuration JSON file, processes language codes, and handles path replacements.

    Attributes:
        source_mc_lang (str): Formatted source Minecraft language code.
        source_google_lang (str): Google language code derived from source Minecraft language.
        target_mc_lang (str): Formatted target Minecraft language code.
        target_google_lang (str): Google language code derived from target Minecraft language.
        mods_path (str): Path to Minecraft mods directory.
        temp_path (str): Temporary directory path.
        translation_path (str): Path for translated files.
        replace_mods (bool): Flag indicating whether to replace original mods.

    Methods:
        __init__(self, config_path=CONFIG_JSON_PATH):
            Initializes the Settings object by reading configuration data from a JSON file,
            processing language codes, and setting various paths and flags.

        _read_json_file(self, path):
            Reads and parses JSON data from the given path.
            Returns the parsed data or an empty string if an error occurs.

        _get_google_lang(self, mc_lang):
            Extracts the Google language code from a Minecraft language code.

        _replace_appdata(self, path):
            Replaces the '%Appdata%' placeholder in the given path with the actual AppData path.

        _format_lang(self, mc_lang):
            Formats a Minecraft language code into the desired format (e.g., 'en_US', 'es_ES').
    """

    def __init__(self, config_path=CONFIG_JSON_PATH):

        config_data = self._read_json_file(config_path)

        self.source_mc_lang = self._format_lang(
            config_data[ORIGINAL_LANG]
        )
        self.source_google_lang = self._get_google_lang(
            self.source_mc_lang
        )

        self.target_mc_lang = self._format_lang(
            config_data[TARGET_LANG]
        )
        self.target_google_lang = self._get_google_lang(
            self.target_mc_lang
        )

        self.mods_path = self._replace_appdata(config_data[MODS_PATH])
        self.temp_path = 'temp'
        self.translation_path = self._replace_appdata(
            config_data[TRANSLATION_PATH]
        )

        self.replace_mods = config_data[REPLACE_ORIGINAL_MODS]

    def _read_json_file(self, path):
        """
        Read JSON file data.
        """
        with open(path) as json_file:
            try:
                data = json.load(json_file)
                return data
            except:
                return ''

    def _get_google_lang(self, mc_lang):
        """
        Get Google language code from Minecraft language code.
        """
        google_lang = mc_lang.split('_')[0]
        return google_lang

    def _replace_appdata(self, path):
        """
        Replace %Appdata% for its respective path.
        """
        pattern = re.compile(r'%appdata%', re.IGNORECASE)
        appdata_path = os.getenv('APPDATA').replace('\\', '\\\\')
        new_path = re.sub(pattern, appdata_path, path)
        return new_path

    def _format_lang(self, mc_lang):
        """
        Format language code for Minecraft (e.g., us_US, es_ES...)
        """
        language, region = mc_lang.split('_')
        formatted_language_code = f'{language.lower()}_{region.upper()}'
        return formatted_language_code
