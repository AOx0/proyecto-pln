from cleaner import _cleaner
from typing import List, Tuple


def lang(language: str) -> Tuple[List[Tuple[str, str]], List[str]]:
    """
    Return the known multiline delimiters and single line
    comment delimiters for the given language
    """

    return _cleaner.lang(language)


def string(
    language: str, multis: List[Tuple[str, str]] = [], singles: List[str] = []
) -> str:
    """
    Remove all multiline comment blocks on multi: [(str, str)] and
    single line comment blocks starting with the delimiters inside
    single: [str] from the source code string
    """

    return _cleaner.string(language, multis, singles)
