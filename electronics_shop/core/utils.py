from electronics_shop.accounts.models import Profile


def get_account():
    return Profile.objects.first()

