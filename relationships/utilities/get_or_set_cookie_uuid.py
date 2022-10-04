import uuid

def get_or_create_cookie_uuid(request):
    """Get cookie UUID from request if available, or create it."""
    cookie_uuid = request.COOKIES.get('uuid')
    if cookie_uuid is None:
        cookie_uuid = uuid.uuid4()
        return cookie_uuid, True
    return cookie_uuid, False