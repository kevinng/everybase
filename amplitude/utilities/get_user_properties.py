import amplitude.constants.user as u

def get_user_properties(user):

# TODO: need to get this done
    return {
        u.COUNTRY_CODE: user.phone_number.country_code,
        u.NUM_UNIQUE_LEADS_VIEWED: '',
        u.REGISTER_DATE_TIME: '',
        u.LAST_SEEN_DATE_TIME: '',
        u.NUM_LEADS_CREATED: '',
        u.NUM_SESSIONS: '',
        u.NUM_CONTACT_REQUEST: ''
    }