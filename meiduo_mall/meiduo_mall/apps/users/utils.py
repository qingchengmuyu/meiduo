from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
from django.conf import settings
from .models import User


def generate_verify_email_url(user):
    """拼接用户邮箱激活url"""
    serializer = Serializer(settings.SECRET_KEY, 60*60*24)
    data = {'user_id': user.id, 'user_email': user.email}
    token = serializer.dumps(data).decode()
    verify_url = settings.EMAIL_VERIFY_URL + '?token=' + token
    return verify_url


def check_verify_email_token(token):
    serializer = Serializer(settings.SECRET_KEY, 60*60*24)
    try:
        data = serializer.loads(token)
        user_id = data.get('user_id')
        user_email = data.get('user_email')

        try:
            user = User.objects.get(id=user_id, email=user_email)
            return user
        except User.DoesNotExist:
            return None

    except BadData:
        return None
