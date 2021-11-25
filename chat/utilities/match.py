import editdistance

def match(
        a : str,
        b : str,
        t : int,
        no_case : bool = True
    ):
    """
    Parameters
    ----------
    a
        String A.
    b
        String B.
    t
        Edit distance threshold integer. Edit distance must be less than or
        equals to t for string A to match string B.
    no_case
        True if match is case-sensitive. True by default.

    Returns
    -------
    is_match
        True if the edit distance between input string a and input string b is
        less than or equals to integer t - accounting for case if no_case is
        False.
    """
    _a = a.lower() if no_case else a
    _b = b.lower() if no_case else b
    return editdistance.eval(_a, _b) <= t