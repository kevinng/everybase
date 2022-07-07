def sort_users(user_x, user_y):
    """Return users sorted by their IDs
    
    Parameters
    ----------
    user_x
        User to sort.
    user_y
        User to sort.

    Returns
    -------
    (user_one, user_two)
        user_one
            User with small ID.
        user_two
            User with larger ID.
    """
    if user_x.id > user_y.id:
        return (user_y, user_x)
    
    return (user_x, user_y)