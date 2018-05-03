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

white = '\033[1;97m'
green = '\033[1;32m'
red = '\033[1;31m'
yellow = '\033[1;33m'
end = '\033[1;m'
important = '\033[35m[*]\033[1;m '
info = '\033[1;33m[!]\033[1;m '
que = '\033[1;34m[?]\033[1;m '
bad = '\033[1;31m[-]\033[1;m '
good = '\033[1;32m[+]\033[1;m '
run = '\033[1;97m[~]\033[1;m '

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