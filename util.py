from sqlparse.sql import IdentifierList, Identifier, Comment


def read_query(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


def strip_spaces_and_comments(tokens: list) -> list:
    return [token for token in tokens if not token.is_whitespace and not isinstance(token, Comment)]


def _extract_identifiers(tokens: list):
    identifiers = []

    for token in tokens:
        if isinstance(token, IdentifierList):
            for identifier in token.get_identifiers():
                identifiers.append(identifier)
        elif isinstance(token, Identifier):
            identifiers.append(token)

    return identifiers
