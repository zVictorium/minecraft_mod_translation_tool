import os
import json
from zipfile import ZipFile, ZIP_DEFLATED
import shutil

from .logs import log_subtitle, log_message
from .translator import Translator


JAR = '.jar'
JSON = '.json'
LANG = '.lang'


class FileManager():
    """
    A utility class for managing translation of Minecraft mod files.

    This class provides methods to unpack mod JAR files, translate language files within them,
    and convert the translated mod folders back to JAR files. It supports translating both JSON and LANG file formats.

    Args:
        settings (Settings): An instance of the Settings class containing various configuration parameters.

    Attributes:
        temp_path (str): Path to the temporary directory for unpacking and processing mod files.
        translation_path (str): Path to the directory where translated mod files will be stored.
        mods_path (str): Path to the directory containing the original mod JAR files.
        source_mc_lang (str): Source Minecraft language code.
        target_mc_lang (str): Target Minecraft language code.
        translator (Translator): An instance of the Translator class for language translation.

    Methods:
        create_needed_folders():
            Creates necessary folders if they do not exist.

        unpack_mods():
            Unpacks all mod JAR files into the temporary directory.

        get_lang_folders():
            Returns a list of paths to language folders containing translation files.

        edit_lang_files(lang_folders):
            Translates source language files to the target language in the specified folders.

        convert_translated_mods():
            Converts translated mod folders back into JAR files.

        remove_original_mod_files():
            Removes original mod JAR files from the mods folder.

        move_translated_mod_files():
            Moves translated mod files to the mods folder.

        remove_folder(folder_path: str):
            Removes an entire folder.

    Example:
        # Create a FileManager instance with appropriate settings
        settings = Settings(...)  # Initialize your Settings object
        file_manager = FileManager(settings)

        # Perform necessary operations
        file_manager.create_needed_folders()
        file_manager.unpack_mods()
        lang_folders = file_manager.get_lang_folders()
        file_manager.edit_lang_files(lang_folders)
        file_manager.convert_translated_mods()
        file_manager.remove_original_mod_files()
        file_manager.move_translated_mod_files()    
    """

    def __init__(self, settings):
        self.temp_path = settings.temp_path
        self.translation_path = settings.translation_path
        self.mods_path = settings.mods_path

        self.source_mc_lang = settings.source_mc_lang
        self.target_mc_lang = settings.target_mc_lang

        self.translator = Translator(
            settings.source_google_lang,
            settings.target_google_lang
        )

    def create_needed_folders(self):
        """
        Create necessary folders if they do not exist.
        """
        os.makedirs(self.temp_path, exist_ok=True)
        os.makedirs(self.translation_path, exist_ok=True)

    def unpack_mods(self):
        """
        Unpack all mod.jar files.
        """
        mod_list = os.listdir(self.mods_path)
        for mod_name in mod_list:
            if mod_name.endswith(JAR):
                mod_file_path = os.path.join(self.mods_path, mod_name)
                unpacking_destination = os.path.join(self.temp_path, mod_name)
                with ZipFile(mod_file_path, 'r') as zip:
                    log_message(f'Unpacking {mod_name}...')
                    zip.extractall(unpacking_destination)

    def get_lang_folders(self):
        """
        Get all language folder paths.
        """
        lang_folders = []
        for foldername, _, filenames in os.walk(self.temp_path):
            if f'{self.source_mc_lang.lower()}{JSON}' or f'{self.source_mc_lang}{LANG}' in filenames:
                if 'lang' in foldername and 'assets' in foldername:
                    lang_folders.append(foldername)
        return lang_folders

    def edit_lang_files(self, lang_folders):
        """
        Translate the source language file to the target language.
        """
        for lang_folder in lang_folders:
            mod_name = lang_folder.split('\\')[1]
            mod_name = mod_name.replace(JAR, '')
            log_subtitle(f'Translating {mod_name}...')
            self._translate_mod(lang_folder, mod_name, JSON)
            log_subtitle(f'Translating {mod_name}...')
            self._translate_mod(lang_folder, mod_name, LANG)

    def _translate_mod(self, lang_folder, mod_name, extension):

        if extension == JSON:
            source_lang = self.source_mc_lang.lower()
            target_lang = self.target_mc_lang.lower()
        elif extension == LANG:
            source_lang = self.source_mc_lang
            target_lang = self.target_mc_lang

        source_lang_file = os.path.join(
            lang_folder,
            f'{source_lang}{extension}'
        )
        target_lang_file = os.path.join(
            lang_folder,
            f'{target_lang}{extension}'
        )
        if not os.path.exists(target_lang_file) and os.path.exists(source_lang_file):
            log_subtitle(
                f'{mod_name} does not contain {target_lang}{extension} file. Translating...'
            )
            if extension == JSON:
                original_data = self._read_json_file(source_lang_file)
            elif extension == LANG:
                original_data = self._read_lang_file(source_lang_file)
            translated_data = self.translator.translate_data(original_data)
            if extension == JSON:
                self._write_json_file(translated_data, target_lang_file)
            elif extension == LANG:
                self._write_lang_file(translated_data, target_lang_file)

    def _read_json_file(self, path):
        """
        Read JSON file data.
        """
        with open(path) as file:
            try:
                data = json.load(file)
                return data
            except:
                return ''

    def _read_lang_file(self, path):
        """
        Read LANG file.
        """
        data = {}
        with open(path, 'r') as file:
            lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                key, value = line.split('=')
                data[key] = value
        return data

    def _write_json_file(self, data, path):
        """
        Write JSON file.
        """
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)

    def _write_lang_file(self, data, path):
        """
        Write LANG file.
        """
        text = ''
        for key, value in data.items():
            text += f'{key}={value}\n'

        with open(path, 'w') as file:
            file.write(text)

    def convert_translated_mods(self):
        """
        Convert all translated mod folders into JAR files.
        """
        mod_folder_list = os.listdir(self.temp_path)
        for mod_folder in mod_folder_list:
            log_message(f'Converting {mod_folder} into mod file...')
            unpacked_mod_path = os.path.join(self.temp_path, mod_folder)
            translation_path = os.path.join(
                self.translation_path,
                mod_folder
            )
            self._convert_folder_to_jar(unpacked_mod_path, translation_path)

    def _convert_folder_to_jar(self, folder_path, jar_path):
        """
        Convert folder to JAR file.
        """
        with ZipFile(jar_path, 'w', ZIP_DEFLATED) as jar:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    jar.write(
                        file_path,
                        os.path.relpath(file_path, folder_path)
                    )

    def remove_original_mod_files(self):
        """
        Remove files in mods folder.
        """
        for filename in os.listdir(self.mods_path):
            file_path = os.path.join(self.mods_path, filename)
            if os.path.isfile(file_path) and file_path.endswith(JAR):
                os.remove(file_path)

    def move_translated_mod_files(self):
        """
        Move files to mods folder.
        """
        for filename in os.listdir(self.translation_path):
            source_path = os.path.join(self.translation_path, filename)
            destination_path = os.path.join(self.mods_path, filename)
            shutil.move(source_path, destination_path)

    def remove_folder(self, folder_path):
        """
        Remove entire folder.
        """
        shutil.rmtree(folder_path)
