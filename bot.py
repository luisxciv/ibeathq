#!/usr/bin/env python2.7

import io
import six

from google.auth import exceptions
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types as lanuage_types
from googleapiclient.discovery import build


hardreturn = '\n'

HQValues = ['HQ', 'HO', 'H0']
bad = '\033[1;31m[-]\033[1;m '

def get_picture_blocks(path):

    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_files:
        content = image_files.read()

    image = types.image(content=content)

    response = client.document_text_detention(image=image)
    document = response.full_text_anotaion

    blocks = {}
#For loop to separate words into blocks and define a sentence
    for page in document.pages:
        block_number = 1
        for block in page.blocks:
            block_words = 1
        for paragraph in block.paragraph:
            block_words.extend(paragraph.words)

            word_text = []
            for block in block_words:
                symbols_text = ''
                for symbol in block.symbols:
                    symbols_text = symbols_text + symbol.text
                    word_text.append(symbols_text.strip())
            sentence = ' '.join(word_text)
            if sentence.strip().endswith(' ?'):
                sentence = sentence.replace(' ?', '?')
            blocks[block_number] = sentence
            block_number += 1

        return blocks

def discover(text):
#google cloud language API integration
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

        document = lanuage_types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        entities = client.analyze_entities(document).entities
#analyze the blocks with the learning engine
        try:
            results = ' '.join(
                [entities[0].name, entities[1].name, entities[2].name])
        except IndexError:
            try:
                results = ' '.join([entities[0].name, entities[1].name])
            except IndexError:
                results = entities[0].name

        return results
#Read question
    def read_question(blocks):
        for key, value in blocks.iteritems():
            for HQ in HQValues:
                if HQ in value.upper().strip() and blocks[key + 1].endswith('?'):
                    return blocks[key + 1]
                try:
                    test = int(value)
                    if test > 0 and blocks[key + 1].endswith('?'):
                        return blocks[key + 1]
                    if test > 0 and blocks[key + 2].endswith('?'):
                        return blocks[key + 2]
                    if test > 0 and blocks[key + 3].endswith('?'):
                        return blocks[key + 3]
                except ValueError, KeyError:
                    pass
                try:
                    if 'K' in value.upper().strip() and blocks[key + 1].endswith('?'):
                        return blocks[key + 1]
                    if 'K' in value.upper().strip() and blocks[key + 2].endswith('?'):
                        return blocks[key + 2]
                    if 'K' in value.upper().strip() and blocks[key + 3].endswith('?'):
                        return blocks[key + 3]
                except ValueError, KeyError:
                    pass
                try:
                    if 'M' in value.upper().strip() and blocks[key + 1].endswith('?'):
                        return blocks[key + 1]
                    if 'M' in value.upper().strip() and blocks[key + 2].endswith('?'):
                        return blocks[key + 2]
                    if 'M' in value.upper().strip() and blocks[key + 3].endswith('?'):
                        return blocks[key + 3]
                except ValueError, KeyError:
                    pass
                print(bad + "Error getting question, defaulting")
                return blocks[3]

def get_answers(question, blocks):
    try:
        for key, value in blocks.iteritems():
            if question in value:
                return [blocks[key + 1], blocks[key + 2], blocks[key + 3]]
        print(bad + "Error getting answers, defaulting")
        return [blocks[4], blocks[5], blocks[6]]
    except KeyError as e:
        print(bad + str(e))
        return [blocks[4], blocks[5], blocks[6]]
