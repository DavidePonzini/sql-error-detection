from sqlparse.sql import IdentifierList, Identifier, Comment
from sqlparse import tokens as ttypes


# Sentinel object to distinguish uninitialized state
class Undefined:
    def __repr__(self):
        return 'UNDEFINED'
    
    def __str__(self):
        return 'UNDEFINED'

UNDEFINED = Undefined()


def read_file(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


def strip_spaces_and_comments(tokens: list) -> list:
    result = []

    for token in tokens:
        # whitespaces and newlines
        if token.is_whitespace:
            continue

        # regular comment in code
        if isinstance(token, Comment):
            continue

        # stray comments
        if token.ttype is ttypes.Comment or (token.ttype is not None and token.ttype.parent is ttypes.Comment):
            continue

        result.append(token)

    return result


def extract_identifiers(tokens: list) -> list:
    identifiers = []

    for token in tokens:
        if isinstance(token, IdentifierList):
            for identifier in token.get_identifiers():
                identifiers.append(identifier)
        elif isinstance(token, Identifier):
            identifiers.append(token)

    return identifiers


def merge_tokens(*tokens) -> list:
    result = []
    for token_list in tokens:
        result += token_list.tokens
    return result