#!/usr/bin/env python2.7
import io
import os
import six
import json
import Queue
import urllib2
import argparse
import threading
import ConfigParser
from ssl import SSLError
from google.auth import exceptions
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types as lanuage_types
from googleapiclient.discovery import build

from time import strftime, gmtime

white = '\033[1;97m'
green = '\033[1;32m'
red = '\033[1;31m'
yellow = '\033[1;33m'
end = '\033[1;m'
important = '\033[35m[*]\033[1;m '
hardreturn = '\n'
info = '\033[1;33m[!]\033[1;m '
que = '\033[1;34m[?]\033[1;m '
bad = '\033[1;31m[-]\033[1;m '
good = '\033[1;32m[+]\033[1;m '
run = '\033[1;97m[~]\033[1;m '

HQValues = ['HQ', 'HO', 'H0']
def get_picture_blocks(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

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
###
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

def search_entity(service, question, answers, queue):
    question = discover(question)
    return search(service, question, answers, queue)


def search(service, question, answers, queue):
    try:
        query = '"' + question + '"' + ' (' + ' OR '.join(answers) + ')'
        results = service.cse().list(q=question, cx=customsearch_id,
                                     num=int(customsearch_results)).execute()
        if queue:
            return queue.put(results)
        if args.verbose:
            print(que + 'Query #1: ' + query + hardreturn)
        return results
    except SSLError:
        print(bad + 'SSL Error encountered, please wait for threads to finish.')
    except Exception as e:
        print(bad + str(e))


def choose(answer):
    print(good + 'Choose ' + green + answer + end)
#

def print_answers(num, answer, count):
    print(good + 'Answer %s: %s' % (str(num), answer) + green +
          ' Found: ' + str(count) + ' results' + end)

def find_answer(path):
    blocks = get_picture_blocks(path)
    question = read_question(blocks)
    print(que + 'Question: ' + question + hardreturn)
    answers = get_answers(question, blocks)
    service = build("customsearch", "v1",
                    developerKey=customsearch_developerKey)

    results1 = search(service, question, answers, None)

    keywords = question.split()

    try:
        question2 = ''.join([keywords[-1], keywords[-2], keywords[-3]])
    except IndexError:
        try:
            question2 = ''.join([keywords[-1], keywords[-2]])
        except IndexError:
            try:
                question2 = keywords[-1]
            except IndexError:


                ###here we start searching for answers and selecting the most common ones
                results2_queue = Queue.Queue()
                search2 = threading.Thread(target=search, args=(
                    service, question2, answers, results2_queue))
                search2.start()

                search3 = threading.Thread(target=search_entity, args=(
                    service, question, answers, results2_queue))
                search3.start()

                items = json.dumps(results1['items']).lower()
                countanswer1 = items.count(answers[1].lower())
                countanswer2 = items.count(answers[2].lower())
                countanswer3 = items.count(answers[3].lower())

                print(info + 'Google Answers:')
                print_answers(1, answers[0], countanswer1)
                print_answers(2, answers[1], countanswer2)
                print_answers(3, answers[2], countanswer3)
                if countanswer1 == countanswer2 and countanswer2 == countanswer3:
                    search2.join()
                    search3.join()
                    results2 = results2_queue.get()

                    items2 = json.dumps(results2['items']).lower()

                    countanswer1 = items.count(answers[0].lower())
                    countanswer2 = items.count(answers[0].lower())
                    countanswer3 = items.count(answers[0].lower())

                    if countanswer1 > countanswer2 and countanswer1 > countanswer3:
                        choose(answers[0])
                    elif countanswer2 > countanswer1 and countanswer2 > countanswer3:
                        choose(answers[1])
                    elif countanswer3 > countanswer1 and countanswer3 > countanswer2:
                        choose(answers[2])
                    else:
                        print(bad + 'Pick that best answer')
                elif countanswer1 > countanswer2 and countanswer1 > countanswer3:
                    choose(answers[0])
                elif countanswer2 > countanswer1 and countanswer2 > countanswer3:
                    choose(answers[1])
                elif countanswer3 > countanswer3 and countanswer3 > countanswer2:
                    choose(answers[2])
                else:
                    print(bad + 'Pick the highest scoring answer')
                print(hardreturn)


if __name__ == "__main__":
    try:
        config = ConfigParser.RawConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), 'bot.cfg'))
        #config.read(os.path.join(os.path.dirname(__file__), 'bot-523ce4ab538b.cfg'))
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.get(
            'bot_config', 'GOOGLE_APPLICATION_CREDENTIALS')

        customsearch_results = config.get('bot_config', 'customsearch_results')
        customsearch_id = config.get('bot_config', 'customsearch_id')
        customsearch_developerKey = config.get(
            'bot_config', 'customsearch_developerKey')

        if not ".json" in os.environ["GOOGLE_APPLICATION_CREDENTIALS"] and not ":" in customsearch_id and not "_" in customsearch_developerKey:
            print(bad + "API keys incorrectly configured")
            exit(1)

        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--verbose",
                            help="increase output verbosity", action="store_true")
        parser.add_argument("-s", "--sample",
                            help="use sample images", action="store_true")
        parser.add_argument("-i", "--input_file",
                            help="use specific images")
        args = parser.parse_args()


        if args.input_file:
            find_answer(os.path.join(
                os.path.dirname(__file__), args.input_file))

        elif args.sample:
            sample_file_names = [
                'test_question.jpeg', 'test_question2.png', 'test_question3.jpg']
            for file_name in sample_file_names:
                find_answer(os.path.join(os.path.dirname(__file__), file_name))
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print(hardreturn + bad + 'Exiting...')
        exit(0)
    except Exception as e:
        print(bad + '%s: %s' % (type(e).__name__, str(e)))
        pass
