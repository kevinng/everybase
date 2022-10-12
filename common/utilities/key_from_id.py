def key_from_id(id):
    """A key is a dense representation of a numeric id. This function translates
    a numeric ID to a key."""
    
    # Dictionary, representing numeric values in sequence. E.g., the symbol in
    # position 0 represents the number 0 and the symbol in position 23
    # represents the number 23.
    d = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd',
        'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
        's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
        'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
        'U', 'V', 'W', 'X', 'Y', 'Z']

    key = ''
    quotient = id
    while quotient > 0:
        remainder = quotient % len(d)
        key = d[remainder] + key
        quotient = int(quotient / len(d))

    print(key)
    return key