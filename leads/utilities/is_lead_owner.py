def is_lead_owner(user, lead):
    if isinstance(user, str):
        # User is not authenticated
        return False
        
    return lead.author.id == user.id