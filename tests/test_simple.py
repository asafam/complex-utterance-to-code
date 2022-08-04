from collections import deque
import re
from main import sample, load_grammar
from key import Key


GRAMMAR = load_grammar("config")
ROOT_KEY = Key("utterance")


def test_contact():
    grammar = GRAMMAR.copy()
    grammar["utterance"] = ["${contact}"]
    results = sample(key=ROOT_KEY, program_stack=deque(), grammar=grammar)
    regexp = rf"contact = Contact\.resolve_from_text\(\".*\"\)"
    result = bool(re.match(regexp, results.to_code()))
    assert result


def test_messages_command_simple():
    grammar = GRAMMAR.copy()
    grammar["utterance"] = ["${simple_message_command}"]
    results = sample(key=ROOT_KEY, program_stack=deque(), grammar=grammar)
    regexp = rf"contact = Contact.resolve_from_text\(.*\)\nrecipient = contact\nexact_content = Content.resolve_from_text\(.*\)\nMessagesCommand.send_message\(recipient=recipient, exact_content=exact_content\)"
    code = results.to_code()
    result = bool(re.match(regexp, code))
    assert result


def test_messages_command_loop():
    grammar = GRAMMAR.copy()
    grammar["utterance"] = ["${loop_message_command}"]
    results = sample(key=ROOT_KEY, program_stack=deque(), grammar=grammar)
    regexp = rf"contact1 = .*\ncontact2 = .*\ncontact3 = .*\nfor recipient in \[contact1, contact2, contact3\]\:\n.*exact_content = .*\n.*send_message\(recipient=recipient, exact_content=exact_content\)"
    result = bool(re.match(regexp, results.to_code()))
    assert result
