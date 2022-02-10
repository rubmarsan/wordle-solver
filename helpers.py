import time

from rules import Rule
import functools
import operator
from collections import Counter, defaultdict, OrderedDict
import math
import random
import numpy as np
from rules import *


def load_CREA(path: str = "CREA_total.TXT"):
    cleant = dict()
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines[1:]:
            order, word, freq_abs, freq_norm = line.split()
            if len(word) == 5:
                cleant[word] = freq_abs

    return cleant


def add_frequencies_to_dictionary(word_list, CREA_word_list):
    conjunction = OrderedDict()
    for word in word_list:
        if word not in CREA_word_list:
            print("Word", word, "not in CREA")
            continue

        conjunction[word] = float(CREA_word_list[word].replace(",", ""))

    # do not normalize, it will be done in latter steps
    # total_apparitions = sum(conjunction.values())
    # conjunction = {k: v / total_apparitions for k, v in conjunction.items()}
    return conjunction


def load_dictionary(path: str = "diccionario_5.lst") -> list:
    with open(path, "r") as f:
        return [l.strip() for l in f.readlines()]


def load_dictionary_with_frequencies(dictionary_path: str = "diccionario_5.lst", CREA_path: str = "CREA_total.TXT"):
    CREA_list = load_CREA(CREA_path)
    words = load_dictionary(dictionary_path)
    words_with_freq = add_frequencies_to_dictionary(words, CREA_list)
    return words_with_freq


def filter_dictionary_with_rule(words: dict, rule: Rule) -> dict[str, float]:
    # filtered: list[str] = []
    # for word in words:
    #     if rule.evaluate(word):
    #         filtered.append(word)
    #
    # return filtered
    return {word: freq for word, freq in words.items() if rule.evaluate(word)}


def get_letters_frequencies(words: dict, duplicate_letters_allowed=True) -> dict:
    """
    When :duplicate_letters_allowed: is True, this method obtains the prevalence of a letter C among the whole
    words list. That is, how likely is for a given random character in a word to be precisely C.
    When :duplicate_letters_allowed: is False, this method obtains the probability of a letter C to be in a random word
    at least once.
    That is, the average "yellow"-ness of a character C.
    :param words: The list of words
    :param duplicate_letters_allowed: boolean indicating which version of the method is to be run
    :return: The frequency of letters (note that statistically-wise the param :duplicate_letters_allowed: changes the
    returned value).
    """
    if duplicate_letters_allowed:
        splitted = list(map(list, words.keys()))
    else:
        splitted = list(map(set, words.keys()))

    flatten_list = functools.reduce(operator.iconcat, splitted, [])

    if duplicate_letters_allowed:
        L = len(flatten_list)
    else:
        L = len(words)

    c = Counter(flatten_list)
    most_common = c.most_common()
    d = {letter: occurrences / L for (letter, occurrences) in most_common}
    return defaultdict(int, d)


def score_partition(partition_1_size, partition_2_size):
    """
    Scores the goodness of the partition. Goes from 0 (if a partition is empty and its counterpart contains all words)
    and 1 (when both partitions contains exactly half of the words)
    :param partition_1: List/Set of words belonging to the first partition
    :param partition_2:  List/Set of words belonging to the second partition
    :return: The score of the partition
    """
    N1 = partition_1_size
    N2 = partition_2_size
    N = N1 + N2
    return math.log2(N / max(N1, N2))


def score_partition_alt(partition_1_size, partition_2_size):
    """
    Scores the goodness of the partition. Goes from 0 (if a partition is empty and its counterpart contains all words)
    and 1 (when both partitions contains exactly half of the words)
    :param partition_1: List/Set of words belonging to the first partition
    :param partition_2:  List/Set of words belonging to the second partition
    :return: The score of the partition
    """
    N1 = partition_1_size
    N2 = partition_2_size
    N = N1 + N2
    return 2 * (1 - (max(N1, N2) / N))


def derive_rules_of_word(word_chosen: str, word_groundtruth: str):
    """
    Given a word, derives the rules of a word.
    :param word:
    :return:
    """

    resulting_new_rules = []
    already_present_letters = defaultdict(int)
    for c_i in range(len(word_chosen)):
        candidate_letter = word_chosen[c_i]
        compared_letter = word_groundtruth[c_i]
        if candidate_letter == compared_letter:
            # green
            already_present_letters[candidate_letter] += 1
            resulting_new_rules.append(LetterInThatPosition(c_i, candidate_letter))
        elif candidate_letter in word_groundtruth:
            # gray (puede que c esté más de una vez

            # ya habíamos computado este gray antes, para que vuelva a ser gray la comparing word debe tener
            # más veces este caracter
            if word_groundtruth.count(candidate_letter) <= already_present_letters[candidate_letter]:
                continue

            already_present_letters[candidate_letter] += 1
            resulting_new_rules.append(LetterNotInThatPosition(c_i, candidate_letter))
            resulting_new_rules.append(LetterInWord(candidate_letter, times=already_present_letters[candidate_letter]))
        else:
            r = LetterNotInWord(candidate_letter)
            resulting_new_rules.append(r)

    resulting_new_rules = list(set(resulting_new_rules))    # filter posible duplicates
    return resulting_new_rules


def value_of_word_alt(candidate_word, words: dict):
    """
    Si aplico "abeja", tengo que ver cuánto biparticionaría (score) el word-set si fuera cada una de las OTRAS palabras
    candidatas. Dado que la palabra escogida (ej. abeja) no es, se me queda un tamaño del word list potencialmente distinto
    al inicial y mayor a 0.

    :param candidate_word:
    :param words:
    :param freqs_per_pos:
    :param letter_frequencies:
    :return:
    """
    L = len(words)
    total_expected_score = 0
    total_words_freq = sum(words.values())
    for groundtruth_word, groundtruth_word_freq in words.items():
        # if groundtruth_word == candidate_word:
        #     continue

        resulting_new_rules = derive_rules_of_word(candidate_word, groundtruth_word)
        
        subset_words = dict(words)
        for rule in resulting_new_rules:
            subset_words = filter_dictionary_with_rule(subset_words, rule)

        L_p = len(subset_words)
        # this_score = 1 - ((L_p - 1) / L)  # cuánto reduzco el set, dejar 1 es ganar
        this_score = -math.log2(L_p/L)  # information score
        weighted_score = this_score * groundtruth_word_freq / total_words_freq
        total_expected_score += weighted_score

    return total_expected_score


def value_of_word(candidate_word, words, freqs_per_pos, letter_frequencies):
    """
    The value of a word is computed by a score metric associated with the three potential outcomes of each letter (green,
    yellow, gray). The score these three outcomes is weighted by the probability of each of them.
    The score metric is related to how well the word partitions the space. That is, we follow a min-max strategy in the
    sense of penalizing words that may potentially result in small reductions of the word-candidate list.

    Also, note that, from a statistical point of view, this considers that the probability of an outcome at position i
    is independent of the outcome at position i'. That is, when computing the probability of a word containing a
    character C at position i (the P(green | C, i)) we do not condition that probability to other P(green | C', i').
    P(green | C, i, C', i') == P(green | C, i).

    This is, indeed, an error but greately simplifies computations.

    :param candidate_word:
    :param words:
    :param freqs_per_pos:
    :param letter_frequencies:
    :return:
    """
    L = len(words)
    total_expected_score = 0

    # for c_i, c in enumerate(list(candidate_word)):
    for c_i, c in enumerate(list(dict.fromkeys(candidate_word))): # <- tweak para no dar doble puntuación si se repite la letra
        P_green = freqs_per_pos[c_i][c]  # probability a word has character c in position c_i

        P_yellow = letter_frequencies[c] - P_green
        # P_yellow_alt = sum((c in word) and (word[c_i] != c) for word in words) / L  # probability a word has character c but not in position c_i
        # assert round(P_yellow, 4) == round(P_yellow_alt, 4)

        P_gray = 1 - P_green - P_yellow
        # P_gray_alt = sum(c not in word for word in words) / L
        # assert round(P_gray, 2) == round(P_gray_alt, 2)

        green_set_size = round(P_green * L)
        yellow_set_size = round(P_yellow * L)
        gray_set_size = round(P_gray * L)

        # score_green = score_partition(green_set_size, L - green_set_size)
        # score_yellow = score_partition(yellow_set_size, L - yellow_set_size)
        # score_gray = score_partition(gray_set_size, L - gray_set_size)

        score_green = score_partition_alt(green_set_size, L - green_set_size)
        score_yellow = score_partition_alt(yellow_set_size, L - yellow_set_size)
        score_gray = score_partition_alt(gray_set_size, L - gray_set_size)

        # esto no checks out por alguna razón y no se cuál
        # score_green_alt, score_yellow_alt, score_gray_alt = compute_score_letter(c, c_i, words)
        # assert round(score_green, 4) == round(score_green_alt, 4) and \
        #        round(score_yellow, 4) == round(score_yellow_alt, 4) and \
        #        round(score_gray, 4) == round(score_gray_alt, 4)

        expected_score = score_green * P_green + score_yellow * P_yellow + score_gray * P_gray
        total_expected_score += expected_score

    return total_expected_score


def compute_score_letter(letter: str, position: int, words: list):
    L = len(words)

    green_set = set(filter_dictionary_with_rule(words, LetterInThatPosition(position, letter)))
    letter_in_word_set = set(filter_dictionary_with_rule(words, LetterInWord(letter)))
    letter_not_in_word_set = set(words).difference(letter_in_word_set)

    green_set_size = len(green_set)
    yellow_set_size = len(letter_in_word_set.difference(green_set))  # la letra está en la palabra, pero no en la posición correcta
    gray_set_size = len(letter_not_in_word_set)

    score_green = score_partition(green_set_size, L - green_set_size)
    score_yellow = score_partition(yellow_set_size, L - yellow_set_size)
    score_gray = score_partition(gray_set_size, L - gray_set_size)

    return score_green, score_yellow, score_gray


def prevalence_character_in_position(position: int, words: dict):
    L = len(words)
    c = Counter(word[position] for word in words.keys())
    most_common = c.most_common()
    d = {letter: occurrences / L for (letter, occurrences) in most_common}
    return defaultdict(int, d)


def send_word_to_chrome(driver, word: str):
    body = driver.find_element_by_css_selector("body")
    for letter in word:
        body.send_keys(letter)
        time.sleep(0.2)

    body.send_keys("\n")

if __name__ == '__main__':
    CREA_list = load_CREA()
    words = load_dictionary()
    words_with_freq = add_frequencies_to_dictionary(words, CREA_list)
    print("Ok")