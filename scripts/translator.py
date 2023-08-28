from deep_translator import GoogleTranslator
from .logs import log_message


class Translator:
    """
    A class for translating text data from a source language to a target language.

    Attributes:
        source_language (str): The source language code.
        target_language (str): The target language code.
        capitalize (bool): Whether to capitalize the translated text.

    Methods:
        translate_data(data): Translates a dictionary of text data from source to target language.
        translate(string): Translates a single string from source to target language.

    Example:
        translator = Translator(source_language='en', target_language='fr', capitalize=True)
        data = {'greeting': 'hello', 'farewell': 'goodbye'}
        translated_data = translator.translate_data(data)
    """

    def __init__(self, source_language, target_language, capitalize=True):
        self.source_language = source_language
        self.target_language = target_language
        self.capitalize = capitalize

    def translate_data(self, data):
        """
        Translate data from source to target language.
        """
        for key, text in data.items():
            translated_text = self.translate(text)
            log_message(f'{text} → {translated_text}')
            data[key] = translated_text
        return data

    def translate(self, string):
        """
        Translate string from source to target language.
        """
        translator = GoogleTranslator(
            source=self.source_language,
            target=self.target_language
        )
        translated_string = translator.translate(string)
        if self.capitalize:
            translated_string = translated_string.capitalize()
        return translated_string
