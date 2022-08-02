from main import sample, load_grammar
import re


GRAMMAR = load_grammar("config")
ROOT_KEY = "utterance"


def test_contact():
    grammar = GRAMMAR.copy()
    grammar["utterance"] = ["${contact}"]
    results = sample(key=ROOT_KEY, program_stack=dict(), grammar=grammar)
    regexp = rf"contact = Contact\.resolve_from_text\(\".*\"\)"
    result = bool(re.match(regexp, results["code"]))
    assert result


def test_messages_command_simple():
    grammar = GRAMMAR.copy()
    grammar["utterance"] = ["${simple_message_command}"]
    results = sample(key=ROOT_KEY, program_stack=dict(), grammar=grammar)
    regexp = rf"contact = .*\nrecipient = contact\n.*exact_content = .*\nsend_message\(recipient=recipient, exact_content=exact_content\)"
    result = bool(re.match(regexp, results["code"]))
    assert result


def test_messages_command_loop():
    grammar = GRAMMAR.copy()
    grammar["utterance"] = ["${loop_message_command}"]
    results = sample(key=ROOT_KEY, program_stack=dict(), grammar=grammar)
    regexp = rf"contact1 = .*\ncontact2 = .*\ncontact3 = .*\nfor recipient in \[contact1, contact2, contact3\]\:\n.*exact_content = .*\n.*send_message\(recipient=recipient, exact_content=exact_content\)"
    result = bool(re.match(regexp, results["code"]))
    assert result
