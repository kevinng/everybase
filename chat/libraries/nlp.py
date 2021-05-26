import editdistance

def match_each_token(tokens, match_str, tolerance, no_case=True):
    """Match each token in tokens via the match function (with edit distance
    tolerance and case-sensitivity no_case). If a token match, return True.
    If no token match, return False.

    Parameters
    ----------
    tokens : string
        List of tokens to match against
    match_str : string
        String to match each token
    tolerance : integer
        Edit distance threshold for matching match_str
    no_case : boolean
        True if match is case-sensitive

    Returns
    -------
    True if a token matches. False otherwise.
    """
    for token in tokens:
        if match(token, match_str, tolerance, no_case):
            return True
    return False

def match(a, b, t, no_case=True):
    """
    Parameters
    ----------
    a : string
        String A
    b : string
        String B
    t : integer
        Edit distance threshold integer. Edit distance must be less than or
        equals to t for string A to match string B.
    no_case : boolean
        True if match is case-sensitive

    Returns
    -------
    True if the edit distance between input string a and input string b is less
    than or equals to integer t - accounting for case if no_case is False.
    """
    _a = a.lower() if no_case else a
    _b = b.lower() if no_case else b
    return editdistance.eval(_a, _b) <= t