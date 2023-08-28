import os
from googletrans import Translator  

def normalInput(input, i):
    input = input.replace("\n", "")
    values = input.split('"')
    
    if i == 0:
        output = str('{\n')
        translatable = False
        id, textToTranslate = '', ''

    elif len(values) == 1:
        if values[0] == '  ':
            output = ''
        else:
            output = str('}')
        translatable = False
        id, textToTranslate = '', ''

    else:
        output = str(f'"{values[1]}": "{values[3]}",\n')
        id = str(values[1])
        textToTranslate = str(values[3])
        translatable = True
    
    return output, translatable, id, textToTranslate

translator = Translator()  
def translate(input):
    translatedText = translator.translate(input, dest='es')
    return translatedText.text


path = os.path.dirname(os.path.abspath(__file__))
data = ''

with open(path + "\\en_us.json", 'r', encoding='utf-8') as fileInput:
    i = 0

    for line in fileInput:
        line, translatable, id, textToTranslate = normalInput(line, i)
        if translatable == False:
            data += line
        else:
            print(textToTranslate)
            translation = translate(str(textToTranslate))
            translation = translation[0].upper() + translation[1:]
            data += f'"{id}": "{translation}",\n'
        i += 1

    print(data)
    fileInput.close()
    
with open(path + "\\es_es.json", "w", encoding='utf-8') as fileOutput:
    data = data.replace(',\n}', '\n}')
    fileOutput.write(data)
    fileOutput.close()

