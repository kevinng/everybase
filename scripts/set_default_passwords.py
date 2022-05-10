from relationships import models

# Give every user that does not have a usable password a default password
def run():
    # Default password base will be combined with user ID to form the default password
    pwd_base = '%5g8jh'

    users = models.User.objects.all()
    for user in users:
        if user.django_user is not None:
            if not user.django_user.has_usable_password():
                password = pwd_base + str(user.id)
                user.django_user.set_password(password)
                user.django_user.save()
                print('Set user ' + str(user) + ' password to ' + password)