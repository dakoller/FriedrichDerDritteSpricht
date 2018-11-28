# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the decorators approach in skill builder.
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

import os

from pprint import pprint
import csv
import random
import twitter

jahr_slot_key = "JAHR"
jahr_slot = "JAHR"

monat_slot_key = "MONAT"
monat_slot = "JAHR"

SKILL_NAME = "Friedrich der Dritte spricht"
WELCOME_MESSAGE = "Willkommen in meinem Hof!"
GET_FACT_MESSAGE = "Friedrich der Dritte sagt "
HELP_MESSAGE = "Was will er wissen?"
HELP_REPROMPT = "Wie können wir ihm helfen?"
STOP_MESSAGE = "Er entferne sich!"
FALLBACK_MESSAGE = "Das wissen wir nicht. Was will er sonst wissen? "
FALLBACK_REPROMPT = 'Was will er wissen?'
EXCEPTION_MESSAGE = "Entschuldigung. Drücke er sich besser aus!"

data = [
    'Ich bin der Kaiser'
]

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TWITTER_CONSUMER_KEY = 'NA'
TWITTER_CONSUMER_SECRET = 'NA'

TWITTER_ACCESS_TOKEN = 'NA'
TWITTER_TOKEN_SECRET = 'NA'

ENABLE_TWEETS = True

def tweet_answer(question, answer):
    try:
        logger.info(os.environ)
        api = twitter.Api(consumer_key=os.environ.get('TWITTER_CONSUMER_KEY','NA'),
                          consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET','NA'),
                          access_token_key=os.environ.get('TWITTER_ACCESS_TOKEN','NA'),
                          access_token_secret=os.environ.get('TWITTER_TOKEN_SECRET','NA'))

        message = 'Frau #Alexa aus Amazonien fragte: %s und wir anworteten %s #codingdavinci #friedrichIII' % (question,answer)
        status = api.PostUpdate(message)
    except Exception as e:
        logger.error('Tweeting error: %s' % str(e))

def where_have_you_been(jahr):
    if (jahr >= 1439) and (jahr <= 1494):

        with open('friedrich_wo.csv', 'r') as f:
            fcsv = csv.reader(f, delimiter=';')

            for row in fcsv:
                if row[0] == '%d' % jahr:
                    locations = row[1].split(',')

            L = 4
            if len(locations) > 4:
                start = random.randint(0, len(locations) - L);
                l2 = locations[start:start + L]

                speech = 'Im Jahr %d waren wir unter anderem in ' % jahr
                for i in range(0, len(l2) - 1):
                    speech = speech + l2[i] + ', '
                speech = speech + ' und ' + l2[-1] + '. '

            elif len(locations) == 2:
                speech = 'Im Jahr %d waren wir in %s und %s.' % (jahr, locations[0], locations[1])
            else:
                speech = 'Im Jahr %d waren wir in %s.' % (jahr, locations[0])

    elif (jahr >= 1415) and (jahr <= 1438):
        speech = 'Im Jahr %d waren wir noch zu klein, um etwas zu schreiben.' % jahr
    elif (jahr < 1415):
        speech = 'Im Jahr %d waren wir noch nicht geboren.' % jahr
    elif (jahr > 1494):
        speech = 'Im Jahr %d waren wir schon tot.' % jahr
    else:
        speech = 'Wir sind sprachlos.'

    return speech


def location_question_when(ort):
    jahre = []
    with open('friedrich_wann.csv', 'r') as f:
        fcsv = csv.reader(f, delimiter=';')

        for row in fcsv:
            if ort == (row[0].lower()):
                jahre = row[1].split(',')
                jahre = list(map(int, jahre))

    if len(jahre) == 0:
        # nicht hiergewesen
        return -1
    else:
        return jahre

def what_did_you_do_in(ort):

    strings = []
    logger.info('in %s' % (ort))
    with open('friedrich_was.csv', 'r') as f:
        fcsv = csv.reader(f, delimiter=';')


        for row in fcsv:
            #print(row[1])

            #if int(row[0]) == jahr and row[1].lower() == ort.lower():
            if row[1] is not None and row[1].lower() == ort.lower():
                strings.append((row[0],row[3]))

        logger.info(strings)

    if len(strings) == 0:
        return 0, 'Ich habe in %s nichts gemacht.' % (ort)
    else:
        rnd = random.choice(strings)
        return int(rnd[0]),rnd[1]

@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech_text = 'Ich bin Friedrich, der Dritte, Kaiser des Heiligen Römischen Reiches deutscher nation. Geboren 1415 und gestorben 1493. was will er wissen?'
    speech_text = SKILL_NAME + ' <voice name="Hans">' + speech_text + '</voice>'

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard(SKILL_NAME, speech_text)).set_should_end_session(
        False).response


@sb.request_handler(can_handle_func=is_intent_name("WhereHaveYouBeenIntent"))
def where_have_you_been_intent_handler(handler_input):
    """Handler for Hello World Intent."""
    # type: (HandlerInput) -> Response
    slots = handler_input.request_envelope.request.intent.slots
    logger.info(slots)
    #ry:
    #    jahr = int(slots[jahr_slot_key].value)
    # except:
    #    jahr = 1445
    jahr = int(os.environ.get('JAHR','1442'))

    speech = where_have_you_been(jahr)

    speech_text = SKILL_NAME + '<voice name="Hans">' + speech + '</voice>'

    try:
        if ENABLE_TWEETS:
            question = 'Wo waren Sie im Jahre %d ?' % jahr
            tweet_answer(question,speech )
    except:
        pass

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard(SKILL_NAME, where_have_you_been(jahr))).set_should_end_session(
        True).response

@sb.request_handler(can_handle_func=is_intent_name("WhatDidYouDoIntent"))
def where_have_you_been_intent_handler(handler_input):
    """Handler for Hello World Intent."""
    # type: (HandlerInput) -> Response
    slots = handler_input.request_envelope.request.intent.slots
    logger.info(slots)
    ort = slots["ORT"].value
    #jahr = slots["JAHR"].value#

    #if jahr == '?':
    #    jahr = 1441

    #jahr = 1445

    speech_jahr, speech_text = what_did_you_do_in(ort)

    if speech_jahr == 0:
        speech_text = speech_text
    else:
        speech_text = ' Im Jahre %d in %s ' % (speech_jahr, ort) + speech_text

    try:
        if ENABLE_TWEETS:
            question = 'Was haben Sie in %s gemacht?' % (ort)
            tweet_answer(question,speech_text)
    except Exception as e:
        pass

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard(SKILL_NAME, speech_text)).set_should_end_session(
        True).response

@sb.request_handler(can_handle_func=is_intent_name("ChildrenIntent"))
def children_intent_handler(handler_input):
    """Handler for Hello World Intent."""
    # type: (HandlerInput) -> Response
    speech_text = 'Aus meiner Ehe mit Eleonore gingen sechs Kinder hervor, wovon der 1459 geborene Maximilian und die 1465 geborene Kunigunde überlebten.'

    try:
        if ENABLE_TWEETS:
            question = 'Haben Sie Kinder? '
            tweet_answer(question,speech_text)
    except Exception as e:
        pass

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard(SKILL_NAME, speech_text)).set_should_end_session(
        True).response


@sb.request_handler(can_handle_func=is_intent_name("WifeIntent"))
def wife_intent_handler(handler_input):
    """Handler for Hello World Intent."""
    # type: (HandlerInput) -> Response
    speech_text = 'Ich bin mit der jungen portugiesischen Königstochter Eleonore verheiratet.'

    try:
        if ENABLE_TWEETS:
            question = 'Sind Sie verheiratet? '
            tweet_answer(question,speech_text)
    except Exception as e:
        pass

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard(SKILL_NAME, speech_text)).set_should_end_session(
        True).response

@sb.request_handler(can_handle_func=is_intent_name("HaveYouBeenAtIntent"))
def where_have_you_been_intent_handler(handler_input):
    """Handler for Hello World Intent."""
    # type: (HandlerInput) -> Response

    slots = handler_input.request_envelope.request.intent.slots
    logger.info(slots)
    ort = slots["ORT"].value

    # try:
    #    jahr = int(slots[jahr_slot_key].value)
    # except:
    #    jahr = 1445
    res = location_question_when(ort.lower())
    if res == -1:
        text = 'Nein, in %s sind wir nie gewesen.' % ort
    else:
        text = 'Ja, wir sind in %s gewesen, und zwar %d mal, zum ersten Mal %d und zum letzten Mal %d. ' % (
        ort, len(res), min(res), max(res))

    speech_text = SKILL_NAME + ' <voice name="Hans">' + text + '</voice>'

    try:
        if ENABLE_TWEETS:
            question = 'Sind Sie in %s gewesen?' % (ort)
            tweet_answer(question,text )
    except Exception as e:
        pass

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard(SKILL_NAME, text)).set_should_end_session(
        True).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    speech_text = HELP_MESSAGE
    speech_text = '<voice name="Hans">' + speech_text + '</voice>'

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).set_card(SimpleCard(
        "Hello World", speech_text)).response


@sb.request_handler(
    can_handle_func=lambda handler_input:
    is_intent_name("AMAZON.CancelIntent")(handler_input) or
    is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = SKILL_NAME + '<voice name="Hans">' + STOP_MESSAGE + '</voice>'

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard(SKILL_NAME, speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = (
        "The Hello World skill can't help you with that.  "
        "You can say hello!!")
    reprompt = "You can say hello!!"
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)

    speech_text = EXCEPTION_MESSAGE
    speech = SKILL_NAME + ' <voice name="Hans">' + speech_text + '</voice>'

    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


handler = sb.lambda_handler()

if __name__ == "__main__":
    #    print(where_have_you_been(1401))
    #    print(where_have_you_been(1416))
    print(where_have_you_been(1441))
    #    print(where_have_you_been(1493))
    #    print(where_have_you_been(1496))
    #print(what_did_you_do_in(1441,'Graz'))
    #tweet_answer('Das war die Frage','Das ist die Antwort')
