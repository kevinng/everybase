def sort_users(user_x, user_y):
    """Return users sorted by their IDs"""
    if user_x.id > user_y.id:
        return (user_y, user_x)
    
    return (user_x, user_y)
