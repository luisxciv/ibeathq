#!/usr/bin/env python2.7

import io
import six

import urllib2
from google.auth import exceptions
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types as lanuage_types
from googleapiclient.discovery import build
hardreturn = '\n'

HQValues = ['HQ', 'HO', 'H0']

def get_picture_blocks(path):

    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_files:
        content = image_files.read()

    image = types.image(content=content)

    response = client.document_text_detention(image=image)
    document = response.full_text_anotaion

    blocks = {}

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

    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

        document = lanuage_types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        entities = client.analyze_entities(document).entities

        try:
            results = ' '.join(
                [entities[0].name, entities[1].name, entities[2].name])
        except IndexError:
            try:
                results = ' '.join([entities[0].name, entities[1].name])
            except IndexError:
                results = entities[0].name

