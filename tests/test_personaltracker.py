import mock
import pytest

from .context import personaltracker


##### Function Tests
#####

@pytest.mark.parametrize("input_type, user_input, result, characters, words", [
    ('number',    100,  100, None, None),    # testing correct number
    ('number', '3.44', 3.4, None, None),    # testing  float number
    ('number', '3.46', 3.5, None, None),    # testing  float number
    ('number', 'a340', None, None, None),    # failure incorrect number
    ('number', '340h', None, None, None),    # failure incorrect number
    ('paragraph', 'hello. there!?', 'hello. there!?',  '[a-zA-Z !?.]', None),   # testing correct characters allowed
    ('paragraph',   'hello!there',            None,    '[a-zA-Z?]', None),   # failure incorrect character, special
    ('paragraph',         'zebra',            None,    '[a-yA-Y?]', None),   # failure incorrect character, normal
    ('answer',  'green', 'green', '[a-zA-Z]', ('green', 'blue')),   # testing correct word
    ('answer',      'b',     'b', '[a-zA-Z]', ('green', 'blue')),   # testing correct word, first character
    ('answer',    'red',    None, '[a-zA-Z]', ('green', 'blue')),   # failure incorrect word
    ('answer',      'r',    None, '[a-zA-Z]', ('green', 'blue')),   # failure incorrect character
    ('answer', 'gre en',    None, '[a-zA-Z]', ('green', 'blue')),   # failure special character
    ('wrong',  '3d40', None, None,              None),    # failure incorrect input_type
    ('answer',   'word', None, None,              None),    # failure missing characters
    ('answer',   'word', None, None, ('green', 'blue')),    # failure missing characters
    ('number', 'word', None, None, None),    # failure incorrect number

])

def test_sanitise_input(input_type, user_input, result, characters, words):
    """
        Testing the sanitise_input function which takes information from 
        the user and returns th is data if it is acceptable.
    """
    with mock.patch('builtins.input', return_value=user_input):
        output = personaltracker.sanitise_input('not important', input_type, characters, words)
        print('printing output: ', output)
        assert output == result
