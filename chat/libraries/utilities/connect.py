from relationships import models

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
    if user_x.id < user_y.id:
        user_1 = user_x
        user_2 = user_y
    else:
        user_1 = user_x
        user_2 = user_y

    return models.Connection.objects.create(
        user_1=user_1,
        user_2=user_2
    )