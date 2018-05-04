#!/usr/bin/env python2.7

import io

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
        block_numer = 1
        for block in page.blocks:
            block_words = 1
        for paragraph in block.paragraph:
            block_words.extend(paragraph.words)