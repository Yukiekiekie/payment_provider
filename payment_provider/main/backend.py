from django.contrib.auth.backends import BaseBackend

from main.models import Payment_Account


class MyBackend(BaseBackend):
    def authenticate(self, request, user_phone=None, password=None, **kwargs):
        try:
            user = Payment_Account.objects.get(user_phone=user_phone)
        except Payment_Account.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return Payment_Account.objects.get(pk=user_id)
        except Payment_Account.DoesNotExist:
            return None
