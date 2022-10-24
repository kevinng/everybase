from relationships import models
from chat.libraries.utility_funcs.sort_users import sort_users

def connect(user_x, user_y):
    """Connect two users - bearing in mind to set the one with the smaller ID
    as Connection.user_1 and the other as Connection.user_2.

    Parameters
    ----------
    user_x : relationships.User
        User to connect
    user_y : relationships.User
        User to connect
    """
    user_1, user_2 = sort_users(user_x, user_y)
    return models.Connection.objects.create(
        user_1=user_1,
        user_2=user_2)