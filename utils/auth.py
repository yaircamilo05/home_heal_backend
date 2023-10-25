from crypt import crypt
from hashlib import scrypt


class Auth:

    def encript_password(self, password) -> str:
        return crypt.hashpw(password.encode('utf-8'), scrypt.gensalt())