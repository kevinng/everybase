def is_lead_owner(user, lead):
    return lead.author.id == user.id