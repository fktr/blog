from itsdangerous import URLSafeSerializer
import base64
from django.conf import settings

class Token:

    def __init__(self,security_key):
        self.security_key=security_key
        self.salt=base64.encodebytes(bytes(security_key,encoding='utf-8'))

    def generate_validate_token(self,username):
        serializer=URLSafeSerializer(self.security_key)
        return serializer.dumps(username,self.salt)

    def confirm_validate_token(self,token,expiration=3600):
        serializer=URLSafeSerializer(self.security_key)
        return serializer.loads(token,self.salt)

    def remove_validate_token(self,token):
        serializer=URLSafeSerializer(self.security_key)
        return serializer.loads(token,self.salt)

token_confirm=Token(settings.SECRET_KEY)
