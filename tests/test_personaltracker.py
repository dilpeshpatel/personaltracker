import mock
import pytest

from .context import personaltracker


##### Function Tests
#####
@pytest.mark.parametrize('input_type, user_input, result, characters, words', [
    ('number',    100,  100, None, None),    # testing correct number
    ('number', '3.44',  3.4, None, None),    # testing  float number
    ('number', '3.46',  3.5, None, None),    # testing  float number
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
    # TODO: add capsys and check print is showing the correct information
    with mock.patch('builtins.input', return_value=user_input):
        output = personaltracker.sanitise_input('not important', input_type, characters, words)
        print('printing output: ', output)
        assert output == result

#### Container Class
@pytest.fixture()
def setup_container_0():
    return personaltracker.Container('No initial items')

@pytest.mark.parametrize('adds, removes, compare_pos, compare_val, length', [
    (['first', 'second', 'third'], [], 1, 'second', 3),    # testing  adding basic items
    (['first', 'second', 'third'], ['third'], -1, 'second', 2),    # testing  adding and removing basic items
    (['first', 'second', 'third', 'second'], ['second'], 2, 'second', 3),    # testing  duplicate removal
    (['first', 'second', 'third'], ['first', 'second', 'third'], None, None, 0),    # empty list
])

def test_container_empty(setup_container_0, adds, removes, compare_pos, compare_val, length):
    """
        Testing adding and removing items from an empty container.
    """
    assert setup_container_0.name == 'No initial items'
    for item in adds:
        setup_container_0.add(item)

    for item in removes:
        setup_container_0.remove(item)

    if length == 0:
        assert len(setup_container_0.list) == length
    else:
        assert setup_container_0.list[compare_pos] == compare_val
        assert len(setup_container_0.list) == length

@pytest.fixture()
def setup_container_1():
    return personaltracker.Container('Has initial items', 
            [personaltracker.Item('one'), 
            personaltracker.Item('two'), 
            personaltracker.Item('three')])

@pytest.mark.parametrize("adds, removes, compare_pos, compare_val, length", [
    (['first', 'second', 'third'], [], -2, 'second', 6),    # testing  adding basic items
    (['first', 'second', 'third'], ['third'], 4, 'second', 5),    # testing  adding and removing basic items
    (['first', 'second', 'third', 'second'], ['second'], 5, 'second', 6),    # testing  duplicate removal
    (['first', 'second', 'third'], ['first', 'second', 'third', 'one', 'two', 'three'], None, None, 0),    # empty list
])

def test_container_notempty(setup_container_1, adds, removes, compare_pos, compare_val, length):
    """
        Testing adding and removing items from a container already containing items.
    """
    assert setup_container_1.name == 'Has initial items'
    for item in adds:
        setup_container_1.add(item)

    for item in removes:
        setup_container_1.remove(item)

    for item in setup_container_1.list:
        print(item)
    if length == 0:
        assert len(setup_container_1.list) == length
    else:
        assert setup_container_1.list[compare_pos] == compare_val
        assert len(setup_container_1.list) == length

#### CMDView Class
@pytest.fixture
def setup_view():
    return personaltracker.CMDView()

def test_view_action(setup_view):
    container = personaltracker.Container('Tester')
    answer = 'list'
    with mock.patch('personaltracker.personaltracker.sanitise_input', return_value = answer):
        output = setup_view.action(container)
        assert output == answer

def test_view_home(capsys, setup_view):
    container = personaltracker.Container('Tester')
    output = setup_view.home(container)
    captured = capsys.readouterr()
    assert captured.out == 'Tester!\n'
    assert output == None
    
def test_view_container_list(capsys, setup_view):
    # Cannot use print statement as it is automatically captured
    # by output, can be escaped using:     with capsys.disabled():
    items = [personaltracker.Item('This'), 
            personaltracker.Item('is'), 
            personaltracker.Item('a'), 
            personaltracker.Item('sentence.')]
    output = "".join([str(item+'\n') for item in items])
    output = 'Tester\'s found:\n' +output
    container = personaltracker.Container('Tester', items)
    setup_view.container_list(container)
    captured = capsys.readouterr()
    assert str(captured.out) == str(output)

def test_view_container_add(capsys, setup_view):
    container = personaltracker.Container('Tester')
    output = setup_view.container_add(container)
    captured = capsys.readouterr()
    assert captured.out == 'What Tester do you wish to add?\n'
    assert output == None

def test_view_container_remove(capsys, setup_view):
    container = personaltracker.Container('Tester')
    output = setup_view.container_remove(container)
    captured = capsys.readouterr()
    assert captured.out == 'What Tester do you wish to remove?\n'
    assert output == None

def test_view_questions(capsys, setup_view):
    questions = [personaltracker.Item('One'), 
                personaltracker.Item('two'), 
                personaltracker.Item('three'), 
                personaltracker.Item('four')]
    responses = ['Yes', 'No', 'Yes', 'Yes']
    container = personaltracker.Container('Tester', questions)
    def side_effect(arg):
        # side_effect allows response to be succussively returned
        return responses[arg]
    with mock.patch('personaltracker.personaltracker.sanitise_input', 
            side_effect=side_effect) as MockHelper:
        MockHelper.side_effect = responses
        output = setup_view.questions(container)
        assert responses == output
