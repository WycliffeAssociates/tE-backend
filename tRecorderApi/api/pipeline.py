from django.contrib.auth.hashers import make_password


def user_created(strategy, details, user=None, *args, **kwargs):
    print(user.username)

    if user:
        # password = make_password("some_password")

        user.is_staff = True
        # user.password = password
        user.save()
