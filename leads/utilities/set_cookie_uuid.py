def set_cookie_uuid(request, response, cookie_uuid):
    """Set cookie_uuid in response if user is authenticated. Return (response, is_set), where is_set is True if cookie_uuid is set."""
    if not request.user.is_authenticated:
        response.set_cookie('uuid', cookie_uuid)
        return response, True
    return response, False