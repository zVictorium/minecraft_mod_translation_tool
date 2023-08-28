# ⛏️ Minecraft Mod Translation Tool ⚒️

`Translate your favorite Minecraft mods into your language! 😄👍`

This is a Python tool designed to assist in the translation of Minecraft mod files from one language to another. It unpacks mod JAR files, translates the language files within them, and converts the translated mod folders back to JAR files. The tool supports both JSON and LANG file formats for translations.

☝️🤓 _I searched for a long time for an automatic translator of Minecraft mods into my language, but I didn't succeed, so I created these scripts myself with my knowledge of Python. It can be improved, but it does the job._

## 💡 Getting Started

1. Clone this repository to your local machine.

2. modify the `config.json` file to specify your source and target languages, paths, and other settings.

3. Run the `start.sh` (Linux) or `start.bat` (Windows) files to start the translation process.
   
    If it does not work, follow the next steps:

    1. Install the required dependencies using the following command:

        ```shell
        pip install -r requirements.txt
        ```
      
    2. Run the `main.py` script to start the translation process:

        ```shell
        python main.py
        ```

## ⚙️ Configuration

The `config.json` file contains settings that control how the translation tool operates. Here's an example of the default configuration:

```json
{
  "original_language": "en_us",
  "target_language": "es_es",
  "mods_path": "mods",
  "translation_path": "mods/translated",
  "replace_original_mods": false
}
```

- `original_language`: The language code of the source Minecraft language files. [**Minecraft Language List**](https://minecraft-archive.fandom.com/wiki/Languages)
- `target_language`: The language code of the target language for translation. [**Minecraft Language List**](https://minecraft-archive.fandom.com/wiki/Languages)
- `mods_path`: The path to the directory containing the original mod JAR files. You can use _**%appdata%**_.
- `translation_path`: The path where translated mod files will be stored. You can use _**%appdata%**_.
- `replace_original_mods`: Set this to `true` if you want to replace the original mod files with the translated versions.

## 📄 Project Structure

The project is organized into the following files and directories:

- `main.py`: The main script that orchestrates the translation process.
- `scripts/logs.py`: Contains functions for logging messages and titles.
- `scripts/settings.py`: Responsible for managing configuration settings.
- `scripts/translator.py`: Defines the `Translator` class for language translation.
- `scripts/file_manager.py`: Responsible for managing mod file operations.
- `config.json`: Configuration file specifying translation settings.
- `requirements.txt`: Lists the required Python packages for the project.

## 👨‍💻 Usage

1. The `main.py` script is the entry point. It reads the configuration settings, creates necessary folders, translates mod files, and performs the conversion.

2. The `settings.py` file contains the `Settings` class, which handles configuration reading and processing.

3. The `translator.py` file defines the `Translator` class used for text translation.

4. The `file_manager.py` file contains the `FileManager` class that handles unpacking, translation, and conversion of mod files.

## 🤝 Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. You could edit the `Translator` class to implement GPT translation... 😉

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

_Made by [zVictörium](https://zvictorium.github.io)._

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/victorium)