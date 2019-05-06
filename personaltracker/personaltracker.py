"""
    Personal Tracker 
"""

import logging
import os
import re
import datetime

import personaltracker.dataIO as dataIO

##### Globals
#####
PARAGRAPH={
    'input_type': 'paragraph',
    'characters': '[0-9a-zA-Z :.!?]',
}
ANSWER={
    'input_type': 'answer',
    'characters': '[a-zA-Z]',
    'actions': ['list','exit', 'add', 'remove', 'today', 'yesterday', 'save'],
    'binary': ['yes', 'affirmative', 'no', 'negative' ]
}
NUMBER={
    'input_type': 'number'
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
class PersonalTracker:
    """
    """
    def __init__(self):
        self.goals = Container('Habit')
        self.goals.load()
        self.view = CMDView()
        self.controller = Controller(self.goals, self.view)
        self.action = 'title'

    def run(self):
        self.controller.run()
        
class Controller():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.action = 'title'

    def run(self):
        """
            Entry point into the program.
        """
        output = None
        while output is None:
            self.read_input()
            output = self.process_action()
        
    def process_action(self):
        """
            The action string as provided by the user.
        """
        if self.action == 'title':
            self.view.title()
        elif self.action == 'list':
            if self.model.list:
                self.view.model_list(self.model)
            else:
                output_string = [self.model.name + '\'s are empty.']
                self.view.output(output_string)
        elif self.action == 'add':
            addition = self.view.model_add(self.model)
            self.model.add(addition)
        elif self.action == 'remove':
            if self.model.list:
                removal = self.view.model_remove(self.model)
                self.model.remove(removal)
            else:
                output_string = [self.model.name + '\'s are empty.']
                self.view.output(output_string)
        elif self.action == 'today':
            progress = self.view.model_progress(self.model, 'today')
            self.model.progress(progress, 'today')
        elif self.action == 'yesterday':
            progress = self.view.model_progress(self.model, 'yesterday')
            self.model.progress(progress, 'yesterday')
        elif self.action == 'save':
            self.model.save()
        elif self.action == 'exit':
            self.model.save()
            return 1
        logging.debug('Action Complete')

    def read_input(self):
        self.action = self.view.action()
        logging.debug('Action: ' + self.action)

class CMDIO:

    def input(self, input_type, characters=None, words=None):
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
                print(user_data)
                if user_data in possible_answers:
                    return user_data
        return None

    def output(self, formatted_string, clear=None):
        """
            Print to commandline a pre-formatted string 
        """
        if clear:
            os.system('clear')
        assert isinstance(formatted_string, list)
        for line in formatted_string:
            print(line)
        return []

class CMDView:
    """
        Interaction with the command line interface.
        Consists of:
        * printing to screen
        * reading in user inputs
    """
    def __init__(self):
        self.cmdio = CMDIO()

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

    def model_list(self, container):
        """
            Lists contents of the container
        """
        assert isinstance(container, Container)
        print(container.name + '\'s' + ' found:')
        for item in container.list:
            print(item)

    def model_add(self, model):
        """
            Display for adding to the model.
        """
        output_string = []
        output_string.append('What ' + model.name + ' do you wish to add?')
        output_string = self.cmdio.output(output_string)
        new_model_item = self.cmdio.input(PARAGRAPH['input_type'], 
                                          PARAGRAPH['characters'])
        output_string.append('Added: ' + model.name)
        self.cmdio.output(output_string)
        return new_model_item

    def model_remove(self, model):
        """
            Display for removing from the model.
        """        
        output_string = []
        output_string.append('What ' + model.name + ' do you wish to remove?')
        for i in range(0, len(model.list)):
            output_string.append( str(i+1) + '. ' + str(model.list[i]))
        output_string = self.cmdio.output(output_string)
        model_number = int(self.cmdio.input(NUMBER['input_type']))
        output_string.append('Removing: ' + str(model.list[model_number-1]))
        self.cmdio.output(output_string)
        return model.list[model_number-1]
    
    def model_progress(self, model, day): 
        """
            Asking for progress for each item in the model.
        """
        output_string = []
        output = []
        output_string.append('Did you complete your ' + model.name + '\'s ' + day+ '?')
        for i in range(0,len(model.list)):
            output_string = []
            output_string.append(model.list[i])
            self.cmdio.output(output_string)
            response = self.cmdio.input(
                ANSWER['input_type'],
                ANSWER['characters'],
                ANSWER['binary'])
            output.append(response)
        print(output)
        return output

    def output(self, output_string):
        """ Outputs string to command line """
        self.cmdio.output(output_string)

class Container:
    """
        A container could be a list of habits, vices or goals.
    """
    id_count = 0
    def __init__(self, name, items_list=None):
        self.id = self.id_count
        self.name = name
        self.id_count += 1
        if items_list:
            self.list = items_list
        else:
            self.list = []
        self.csvfile = dataIO.CSVFileIO(self.name, 
                                        f"{self.name}.csv", 
                                        Item.fieldnames())
        self.progressfile = dataIO.FileIO(self.name, 'progress.csv')

    def load(self):
        data = self.csvfile.read_dict()
        if data:
            del(data[0])
            for item in data:
                self.list.append(Item(item['label'], 
                                      item['version'], 
                                      item['ID']))

    def add(self, item):
        self.list.append(Item(item))

    def remove(self, item):
        self.list.remove(item)

    def progress(self, progress, date):
        """ save progress to file """
        # convert date into date object
        print("progress: " + str(type(progress)))
        print(progress)
        if date is 'today':
            day = datetime.date.today()
        else:
            day = datetime.date.today() - datetime.timedelta(1)
        # convert to dictionary (id)
        ids = []
        # output_string
        for item in self.list:
            ids.append(item.id)
        ids.insert(0, 'date')
        progress.insert(0, day)
        rows = [ids, progress]
        self.progressfile.write_file(rows)

    def save(self):
        """
            Save all data to file.

            Folder name is derived from container name.
            The container list data is saved to one file.
            The progress data is saved in two file ways organised by:
            * per container item
            * per date
        """
        # Save current container
        # data = dict(zip(fieldnames, self.list))
        # print(data['Goal'])
        # print('roar')
        data = []
        if len(self.list) is 0:
            self.csvfile.write_dict(None)
        else:
            for item in self.list:
                data.append(item.save())
            # format data into, csv line items
            self.csvfile.write_dict(data)
        # steps
        # filename
        # filedata

class Item:
    """ A single item stored by a container. """
    id_count = 0

    def __init__(self, label, version=None, id=None):
        if id is None:
            self.id = Item.id_count
        else:
            id = int(id)
            self.id = id
            if max(id, Item.id_count) == id:
                Item.id_count = id
        Item.id_count += 1
        self.label = label
        if version:
            self.version = int(version)
        else:
            self.version = 1

    def __repr__(self):
        return f"ID: {self.id}, version: {self.version}, {self.label}"

    def __str__(self):
        return f"{self.label}"

    def save(self):
        return {'ID': self.id, 'label': self.label, 'version': self.version}

    @staticmethod
    def fieldnames():
        return ['ID', 'label', 'version']
    
    # The following  are necessary when updating to use id's more prominently
    # def __setattr__(self, data, new_data)
    # def __getitem__(self,)

