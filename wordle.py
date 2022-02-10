import time
from rules import *
from helpers import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def derive_rules(css_class: str, letter: str, position: int, hits: dict) -> list[Rule]:
    if "bg-absent" in css_class:
        return [LetterNotInWord(letter)]
    elif "bg-correct" in css_class:
        return [LetterInThatPosition(position, letter)]
    elif "bg-present" in css_class:
        return [LetterNotInThatPosition(position, letter),
            LetterInWord(letter, times=hits[letter])]
    else:
        raise Exception(f"Unexpected css_class: {css_class}")

if __name__ == '__main__':
    achieved_convergence = False

    t0 = time.time()
    words = load_dictionary_with_frequencies()
    print(f"Elapsed {time.time() - t0} seconds [loading dictionary]")

    driver = webdriver.Chrome()
    driver.get("https://wordle.danielfrg.com/")
    time.sleep(1)
    driver.find_element_by_css_selector("button.bg-correct").click()

    guess = "olear"
    for iteration in range(6):
        if achieved_convergence:
            print("That's all folks")
            time.sleep(20)
            driver.close()
            exit()

        # Empiezo con un random guess => olear
        send_word_to_chrome(driver, guess)

        letters_hit = defaultdict(int)
        for letter_position in range(5):
            outcome_element = driver.find_element_by_css_selector(f".grid.grid-cols-5.gap-1.w-full:nth-of-type({iteration+1}) > div:nth-of-type({letter_position + 1}) > div > div.react-card-back > div")
            outcome_classes = outcome_element.get_attribute('class')
            letters_hit[guess[letter_position]] += 1
            derived_rules = derive_rules(outcome_classes, guess[letter_position], letter_position, letters_hit)
            for derived_rule in derived_rules:
                words = filter_dictionary_with_rule(words, derived_rule)

        if len(words) == 1:
            achieved_convergence = True

        words_score = {}
        for w in words:
            words_score[w] = value_of_word_alt(w, words)
        # words_score = {w: value_of_word_alt(w, words) for w in words}
        guess = max(words_score, key=words_score.get)

    print("Sorry, I failed you :[")
    exit()