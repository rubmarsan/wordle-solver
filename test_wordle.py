from rules import *
from helpers import *


to_test_words = ['niego', 'rojal', 'catey', 'cojez', 'torno', 'anexa', 'globo', 'tupin', 'tuyas', 'cacao']


def test_letter_not_in_that_position():
    expected_results = [True, True, True, True, False, True, True, False, False, True]
    lnitp = LetterNotInThatPosition(0, "t")
    for ttw_i, ttw in enumerate(to_test_words):
        assert lnitp.evaluate(ttw) == expected_results[ttw_i], f"Failed for word {ttw}"


def test_letter_in_that_position():
    expected_results = [False, False, True, False, False, False, False, False, False, True]
    litp = LetterInThatPosition(1, "a")
    for ttw_i, ttw in enumerate(to_test_words):
        assert litp.evaluate(ttw) == expected_results[ttw_i], f"Failed for word {ttw}"


def test_letter_in_word():
    expected_results = [True, False, True, True, False, True, False, False, False, False]
    liw = LetterInWord("e")
    for ttw_i, ttw in enumerate(to_test_words):
        assert liw.evaluate(ttw) == expected_results[ttw_i], f"Failed for word {ttw}"


def test_letter_not_in_word():
    expected_results = [True, False, True, False, True, True, True, True, True, True]
    liw = LetterNotInWord("j")
    for ttw_i, ttw in enumerate(to_test_words):
        assert liw.evaluate(ttw) == expected_results[ttw_i], f"Failed for word {ttw}"


def test_load_dictionary():
    d = load_dictionary()
    d_l = len(d)
    assert d_l == 4754, f"Retrieved length of dictionary {d_l} when expected 4748"

