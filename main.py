from collections import Counter
from pathlib import Path
import re
from typing import Tuple, Union
from typing import Counter as CounterType


class MadLibsFile:
    """ A class to interact with .madlibs files """
    def __init__(self):
        pass

    @staticmethod
    def parse(madlibs: str) -> Tuple[str, CounterType[str]]:
        """
        Parses a string in Mad Libs format
        :param madlibs: A string in Mad Libs format, where some words are replaced by category names in curly braces.

        :return: The original string and a Counter containing categories as keys and their count as value.
        """
        categories = re.findall(r"{(.*?)}", madlibs, flags=re.MULTILINE)
        return madlibs, Counter(categories)

    @staticmethod
    def read(path: Union[str, Path]):
        """ Read a .madlibs file and return its parsed content """
        with open(path, 'r') as mlf:
            return MadLibsFile.parse(mlf.read())


class Game:
    """ A game of Mad Libs """

    def __init__(self, madlibs_folder="Stories"):
        """
        Initialize the game
        """
        self.text = None
        self.count_of_categories = None
        self.current_round = None
        self.folder = Path(madlibs_folder)

    def choose_madlib(self):
        inventory = list(self.folder.glob('*.madlibs'))
        print("Choose one of the following files by entering the number in parentheses:")
        for idx, file in enumerate(inventory):
            print(f"({idx}) {file.name}")
        selection = inventory[int(input("> "))]
        self.text, self.count_of_categories = MadLibsFile().read(selection)

    def choose_madlib_and_play(self):
        self.choose_madlib()
        self.play()

    def play(self):
        """
        Play rounds of Mad Libs until the user ends the game
        """
        if not self.text:
            self.choose_madlib()
        Round(self.text, self.count_of_categories).play()
        self.show_menu()

    def show_menu(self):
        print("Do you want to play another round? Enter the number in parentheses to select an option.")
        print("(1) Yes!")
        print("(2) Choose a different Mad Lib")
        print("(3) Quit game")
        choice = int(input("> "))
        choices = {1: self.play, 2: self.choose_madlib_and_play, 3: self.quit}
        choices[choice]()

    @staticmethod
    def quit():
        print("Thanks for playing!")
        quit()


class Round:
    """ A round of Mad Libs """
    def __init__(self, text, count_of_categories):
        self.text = text
        self.count_of_categories = count_of_categories
        self.words = dict()

    def get_user_input(self):
        """
        Prompts the user for the required number of words for each category and returns the lists
        """
        def sanitize_category_name(name: str):
            """ Cleans up the category name to make it more human-readable """
            return name.replace("-", " ").strip()

        self.words = dict()
        prompt_string = "Please enter a "
        for category in self.count_of_categories.elements():
            if self.words.get(category):
                self.words[category].append(input(prompt_string + sanitize_category_name(category) + ": ").strip().lower())
            else:
                self.words[category] = [input(prompt_string + sanitize_category_name(category) + ": ").strip().lower()]
        print("Thank you!")

    def fill_in_words(self):
        """
        Fill in the gaps of a string in Mad Libs format using the provided words.
        """
        try:
            for category, word_list in self.words.items():
                while word_list:
                    self.text, gap_found = re.subn(fr"{{{category}}}", word_list[0], self.text, count=1)
                    if not gap_found:
                        raise ValueError
                    word_list.pop(0)
        except ValueError:
            print("Error: Cannot find enough gaps to fill in all the supplied words!")
            return ""

        """ Check if all gaps have been filled """
        if re.search(r"{.*}", self.text, flags=re.MULTILINE):
            print("Error: Could not find enough words to fill every gap!")
            return ""

    def print_madlib(self):
        """ Print the string with the words filled in """
        print("And here is the whole story: \n\n")
        print(self.text)
        print("\n\n")

    def play(self):
        """ Play a round of Mad Libs """
        self.get_user_input()
        self.fill_in_words()
        self.print_madlib()


if __name__ == '__main__':
    Game().play()
