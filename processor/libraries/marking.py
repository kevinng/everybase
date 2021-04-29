def mark_string(string, start_pos, end_pos, start_tag, end_tag):
    """Mark string at positions start_pos and end_pos with start_tag and end_tag
    respectively. I.e., enclose the sub-string from start_pos and end_pos with
    start_tag and end_tag.

    Return marked string, and position one after the end of end_tag as a tuple
    in the format:
    
    (string, pos)

    Last updated/tested: 29 April 2021, 11:19 PM

    Parameters
    ----------
    string
        String to parse and return
    start_pos
        Start position to tag
    end_pos
        End position to tag
    start_tag
        Start text marker tag to use
    end_tag
        End text marker tag to use
    """

    new_string = string[:start_pos] + start_tag + string[start_pos:end_pos] + \
        end_tag + string[end_pos:]

    next_pos = len(string[:start_pos]) + len(start_tag) + \
        len(string[start_pos:end_pos]) + len(end_tag)

    return (new_string, next_pos)