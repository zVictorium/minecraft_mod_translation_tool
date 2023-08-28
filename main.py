from scripts.logs import log_title
from scripts.file_manager import FileManager
from scripts.settings import Settings


settings = Settings()


def main():
    file_manager = FileManager(settings)
    file_manager.create_needed_folders()
    log_title('Unpacking mod files...')
    file_manager.unpack_mods()
    lang_folders = file_manager.get_lang_folders()
    log_title('Translating mods...')
    file_manager.edit_lang_files(lang_folders)
    log_title('Converting to mod files...')
    file_manager.convert_translated_mods()
    if settings.replace_mods:
        log_title('Replacing original mods...')
        file_manager.remove_original_mod_files()
        file_manager.move_translated_mod_files()
        file_manager.remove_folder(settings.translation_path)
    file_manager.remove_folder(settings.temp_path)
    log_title('All mods have been translated!')


if __name__ == '__main__':
    main()
