from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class EmailAuthBackend(BaseAuthentication):
    def authenticate(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return None

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise AuthenticationFailed('No such user')

        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password')

        return (user, None)
