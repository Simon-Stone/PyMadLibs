from collections import Counter
from pathlib import Path
import re
from typing import Dict, List, Tuple, Union
from typing import Counter as CounterType


def parse_madlibs_string(madlibs: str) -> Tuple[str, CounterType[str]]:
    """
    Parses a string in Mad Libs format
    :param madlibs: A string in Mad Libs format, where some words are replaced by category names in curly braces.

    :return: The original string and a Counter containing categories as keys and their count as value.
    Example: { 'noun' : 2, 'verb-in-ing-form' : 1 }

    Example:
    >>> madlibs_string =  'A {noun} was {verb-in-ing-form} to the {noun}.'
    >>> parse_madlibs_string(madlibs_string)
    ('A {noun} was {verb-in-ing-form} to the {noun}.', Counter({'noun': 2, 'verb-in-ing-form': 1}))
    """
    categories = re.findall(r"{(.*?)}", madlibs, flags=re.MULTILINE)
    return madlibs, Counter(categories)


def read_madlibs_file(path: Union[str, Path]):
    """ Read a .madlibs_string file and return its parsed content """
    with open(path, 'r') as mlf:
        return parse_madlibs_string(mlf.read())


def get_user_input(categories: CounterType[str]) -> Dict[str, List[str]]:
    """
    Prompts the user for the required number of words for each category and returns the lists
    :param categories: Counter object where each key is a category name.
    :return: A dictionary where each key is the category name and each value is a list of user-provided words fitting that category.
    """
    def sanitize_category_name(name: str):
        """ Cleans up the category name to make it more human-readable """
        return name.replace("-", " ").strip()

    words = dict()
    prompt_string = "Please enter a "
    for category in categories.elements():
        if words.get(category):
            words[category].append(input(prompt_string + sanitize_category_name(category) + ": ").strip().lower())
        else:
            words[category] = [input(prompt_string + sanitize_category_name(category) + ": ").strip().lower()]
    print("Thank you!")
    return words


def fill_in_words(madlibs: str, words: Dict[str, List[str]]) -> str:
    """
    Fill in the gaps of a string in Mad Libs format using the provided words.
    :param madlibs:
    :param words:
    :return: The text with the words filled in
    """
    try:
        for category, word_list in words.items():
            while word_list:
                madlibs, gap_found = re.subn(fr"{{{category}}}", word_list[0], madlibs, count=1)
                if not gap_found:
                    raise ValueError
                word_list.pop(0)
    except ValueError:
        print("Error: Cannot find enough gaps to fill in all the supplied words!")
        return ""

    """ Check if all gaps have been filled """
    if re.search(r"{.**}", madlibs, flags=re.MULTILINE):
        print("Error: Could not find enough words to fill every gap!")
        return ""

    return madlibs


def print_text(text: str):
    print("And here is the whole story: \n\n")
    print(text)
    print("\n\nThank you for playing Mad Libs!")


def play_madlibs():
    text, categories = read_madlibs_file('Stories/TheZoo.madlibs')
    words = get_user_input(categories)
    print_text(fill_in_words(text, words))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    play_madlibs()





