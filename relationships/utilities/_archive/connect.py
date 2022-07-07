from relationships import models
from relationships.utilities._archive import sort_users

def connect(
        user_x : models.User,
        user_y : models.User
    ):
    """Connect two users - bearing in mind to set the one with the smaller ID
    as Connection.user_one and the other as Connection.user_two.

    Parameters
    ----------
    user_x
        User to connect.
    user_y
        User to connect.

    Returns
    -------
    connection
        Connection model reference between user_x and user_y.
    """
    user_one, user_two = sort_users(user_x, user_y)
    return models.Connection.objects.create(
        user_one=user_one,
        user_two=user_two
    )