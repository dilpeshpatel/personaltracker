"""

"""

import logging
import os
import re

##### Functions
#####

def sanitise_input(question, input_type, characters=None, words=None):
    """
        The keyboard input is only kept if the data abides by certain
        rules otherwise nothing is returned.

        If the expectation is a number an int or float is allowed.
        Free form text allows only a set of regex characters.
        If the user is answering a specific question the answer must
        contain only the allowed regex characters and then be contained
        in the set of possible answers (including first letter only).
    """
    user_data = input('--> ')
    if input_type is 'number':
        try:
            number = float(user_data)
            return round(number,1)
        except(ValueError):
            pass
        try:
            number = int(user_data)
            return number
        except(ValueError):
            pass
    elif input_type is 'paragraph' and characters is not None   :
        found = re.findall(characters, user_data)
        if len(user_data) == len(found):
            return user_data
    elif input_type is 'answer' and characters is not None and words is not None:
        print("Hi")
        found = re.findall(characters, user_data)
        if len(user_data) == len(found):
            possible_answers = set([string[0] for string in words])
            possible_answers.update(words)
            if user_data in possible_answers:
                return user_data
    return None
