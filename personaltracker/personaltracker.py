"""

"""

import logging
import os
import re

##### Globals
#####
PARAGRAPH={
    'input_type': 'paragraph',
    'characters': '[a-zA-Z .!?]',
}
ANSWER={
    'input_type': 'answer',
    'characters': '[a-zA-Z]',
    'actions': ['list','exit','answer', 'add', 'remove', 'edit'],
    'binary': ['yes', 'affirmative', 'no', 'negative' ]
}

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
    elif input_type is 'answer' \
            and characters is not None \
            and words is not None:
        found = re.findall(characters, user_data)
        if len(user_data) == len(found):
            possible_answers = set([string[0] for string in words])
            possible_answers.update(words)
            if user_data in possible_answers:
                return user_data
    return None

##### Classes
#####
class CMDView:
    """
        Interaction with the command line interface.
        Consists of:
        * printing to screen
        * reading in user inputs
    """
    def action(self, container=None):
        """ 
            User input capture.
        """
        result = None
        # TODO: Change while loop to for loop
        while result is None:
            result = sanitise_input(
                "What task do you wish to perform?",
                ANSWER['input_type'],
                ANSWER['characters'],
                ANSWER['actions'])
        return result

    def title(self):
        """
            Entry into applcation.
        """
        os.system('clear')
        print('Personal Tracker!')

    def home(self, container):
        """
            Displays the home screen of a container.
        """
        assert isinstance(container, Container)
        os.system('clear')
        print(container.name + '!')

    def container(self, container):
        """
            Lists contents of the container
        """
        assert isinstance(container, Container)
        for item in container.list:
            print(item)
    
    def questions(self, container):
        """
            Ask's questions to the user with each question requiring a
            response.
        """
        assert isinstance(container, Container)
        output = []
        result = None
        for item in container.list:
            # TODO: Change while loop to for loop
            while result is None:
                result = sanitise_input(
                                        item, 
                                        ANSWER['input_type'], 
                                        ANSWER['characters'],
                                        ANSWER['binary'])
            output.append(result)
            result = None
        # debugging
        for i in range(len(output)):
            logging.debug("question: " + container.list[i])
            logging.debug("answer: " + output[i])
        return output

class Container:
    """
        A container could be a list of habits, vices or goals.
    """
    id_count = 0
    def __init__(self, name, items = None):
        self.id = self.id_count
        self.name = name
        self.id_count += 1
        self.list = []
        if items:
            self.list = items

    def add(self, item):
        self.list.append(item)

    def remove(self, item):
        self.list.remove(item)
