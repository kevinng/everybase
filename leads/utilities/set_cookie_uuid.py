def set_cookie_uuid(response, cookie_uuid):
    """Set cookie_uuid in response."""
    response.set_cookie('uuid', cookie_uuid)
    return response