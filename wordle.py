import time
from rules import *
from helpers import *



if __name__ == '__main__':
    t0 = time.time()
    words = load_dictionary_with_frequencies()
    print(f"Elapsed {time.time() - t0} seconds [loading dictionary]")

    # Empiezo con un random guess => olear

    # olear
    words = filter_dictionary_with_rule(words, LetterNotInThatPosition(0, "o"))
    words = filter_dictionary_with_rule(words, LetterInWord("o"))

    words = filter_dictionary_with_rule(words, LetterNotInWord("r"))
    words = filter_dictionary_with_rule(words, LetterNotInWord("e"))
    words = filter_dictionary_with_rule(words, LetterNotInWord("a"))
    words = filter_dictionary_with_rule(words, LetterNotInWord("s"))


    # # canal
    # words = filter_dictionary_with_rule(words, LetterInThatPosition(1, "o"))
    # words = filter_dictionary_with_rule(words, LetterInThatPosition(3, "i"))
    #
    #
    # words = filter_dictionary_with_rule(words, LetterNotInThatPosition(4, "n"))
    # words = filter_dictionary_with_rule(words, LetterInWord("n"))
    #
    # words = filter_dictionary_with_rule(words, LetterNotInWord("c"))
    # words = filter_dictionary_with_rule(words, LetterNotInWord("l"))


    # # colin
    # words = filter_dictionary_with_rule(words, LetterNotInThatPosition(1, "o"))
    # words = filter_dictionary_with_rule(words, LetterNotInThatPosition(3, "i"))
    # words = filter_dictionary_with_rule(words, LetterNotInThatPosition(4, "n"))
    # words = filter_dictionary_with_rule(words, LetterInWord("i"))
    # words = filter_dictionary_with_rule(words, LetterInWord("n"))
    #
    # words = filter_dictionary_with_rule(words, LetterNotInWord("l"))
    # words = filter_dictionary_with_rule(words, LetterNotInWord("t"))

    # # hinco
    # words = filter_dictionary_with_rule(words, LetterInThatPosition(1, "i"))
    # words = filter_dictionary_with_rule(words, LetterInThatPosition(2, "n"))
    # words = filter_dictionary_with_rule(words, LetterInThatPosition(4, "o"))
    # words = filter_dictionary_with_rule(words, LetterNotInWord("h"))
    # words = filter_dictionary_with_rule(words, LetterNotInWord("c"))
    #
    # # mingo
    # words = filter_dictionary_with_rule(words, LetterInThatPosition(1, "i"))
    # words = filter_dictionary_with_rule(words, LetterInThatPosition(2, "n"))
    # words = filter_dictionary_with_rule(words, LetterInThatPosition(3, "g"))
    # words = filter_dictionary_with_rule(words, LetterInThatPosition(4, "o"))
    # words = filter_dictionary_with_rule(words, LetterNotInWord("m"))


    t0 = time.time()
    freqs_per_pos = [prevalence_character_in_position(i, words) for i in range(5)]
    letter_frequencies = get_letters_frequencies(words, duplicate_letters_allowed=False)
    words_score = {w: value_of_word(w, words, freqs_per_pos, letter_frequencies) for w in words}
    best_word = max(words_score, key=words_score.get)
    print(f"Best word to choose     {best_word}     among {len(words)} others")
    print(f"Elapsed {time.time() - t0} seconds [suggesting next word]")

    t0 = time.time()
    words_score = {}
    for w in words:
        words_score[w] = value_of_word_alt(w, words)
    # words_score = {w: value_of_word_alt(w, words) for w in words}
    best_word = max(words_score, key=words_score.get)
    print(f"Best word to choose     {best_word}     among {len(words)} others")
    print(f"Elapsed {time.time() - t0} seconds [suggesting next word - alt method]")
    exit()