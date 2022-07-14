from relationships import models as relmods

def is_connected(connectee, lead):
    if isinstance(connectee, str):
        # Connectee is not authenticated
        return False

    user_one = connectee.id if connectee.id < lead.author.id else lead.author.id

    if connectee.id < lead.author.id:
        user_one = connectee.id
        user_two = lead.author.id
    else:
        user_one = lead.author.id
        user_two = connectee.id
        
    return relmods.Connection.objects.filter(
        user_one=user_one,
        user_two=user_two
    ).count() > 0