def is_space(c: str):
    """Returns True if c is a space.

    Returns False otherwise.

    A space may be a ' ' or '\\t' or '\\n'.

    Last updated/tested: 29 April 2021, 8:51 PM

    Parameters
    ----------
    c
        Character to test
    """

    return c is ' ' or c is '\t' or c is '\n'