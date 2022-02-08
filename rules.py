from abc import ABC, abstractmethod


class Rule(ABC):
    @abstractmethod
    def evaluate(self, word: str):
        pass


class PositionalRule(Rule):
    def __init__(self, position: int, letter: str):
        self.position = position
        self.letter = letter.lower()

    @abstractmethod
    def evaluate(self, word: str):
        pass

    def __eq__(self, other: Rule):
        if isinstance(other, NonPositionalRule):
            return False
        elif isinstance(other, PositionalRule):
            return other.position == self.position and other.letter == self.letter
        else:
            raise NotImplemented

    def __hash__(self):
        return id(f"{self.position}, {self.letter}")


class LetterNotInThatPosition(PositionalRule):
    def evaluate(self, word: str) -> bool:
        return word[self.position] != self.letter


class LetterInThatPosition(PositionalRule):
    def evaluate(self, word: str) -> bool:
        return word[self.position] == self.letter


class NonPositionalRule(Rule):
    def __init__(self, letter: str, times: int = 1):
        self.letter = letter.lower()
        self.times = times

    @abstractmethod
    def evaluate(self, word: str):
        pass

    def __eq__(self, other):
        if isinstance(other, PositionalRule):
            return False
        elif isinstance(other, NonPositionalRule):
            return other.times == self.times and other.letter == self.letter
        else:
            raise NotImplemented

    def __hash__(self):
        return id(f"{self.times}, {self.letter}")


class LetterInWord(NonPositionalRule):
    def evaluate(self, word: str) -> bool:
        return word.count(self.letter) >= self.times


class LetterNotInWord(NonPositionalRule):
    def evaluate(self, word: str) -> bool:
        return self.letter not in word
