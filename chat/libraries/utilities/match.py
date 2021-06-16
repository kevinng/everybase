import editdistance

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