"""Defines a function for lexing a comment, `lex`."""

from typing import (
    Iterator,
    List,
)
from .peaker import Peaker
from .token import Token, TokenType


def _is_space(char: str) -> bool:
    return char == ' '


def _is_newline(char: str) -> bool:
    return char == '\n'


def _is_colon(char: str) -> bool:
    return char == ':'


def _is_separator(char: str) -> bool:
    """Return true if `char` is a separator other than newline or space."""
    return char.isspace() and not (_is_space(char) or _is_newline(char))


def _is_double_quotation(char: str) -> bool:
    return char == '"'


def _is_word(char: str) -> bool:
    return not any([
        _is_space(char),
        _is_newline(char),
        _is_colon(char),
        _is_separator(char),
        _is_double_quotation(char),
    ])


def lex(program: str) -> Iterator[List[Token]]:
    """Create a stream of tokens from the string."""
    extra = ''  # Extra characters which are pulled but unused from a check.
    peaker = Peaker((x for x in program))  # the stream
    while peaker.has_next():
        # Each of the following conditions must move the stream
        # forward and -- excepting separators -- yield a token.
        if _is_space(peaker.peak()):
            spaces = ''.join(peaker.take_while(_is_space))
            for _ in range(len(spaces) // 4):
                yield Token(' ' * 4, TokenType.INDENT)
        elif _is_newline(peaker.peak()):
            value = peaker.next()
            yield Token(value, TokenType.NEWLINE)
        elif _is_colon(peaker.peak()):
            value = peaker.next()
            yield Token(value, TokenType.COLON)
        elif _is_separator(peaker.peak()):
            peaker.take_while(_is_separator)
        elif _is_double_quotation(peaker.peak()):
            value = ''.join(peaker.take_while(_is_double_quotation))
            if len(value) >= 3:
                for _ in range(len(value) // 3):
                    yield Token('"""', TokenType.DOCTERM)
            else:
                extra = value
        else:
            value = ''.join(peaker.take_while(_is_word))
            if extra != '':
                value = extra + value
                extra = ''
            assert len(value) > 0, "There should be non-special characters."
            yield Token(value, TokenType.WORD)