import hashlib


class User:

    def __init__(self, username, password):
        """The password will be encrypted before storing"""

        self.username = username
        self.password = self._encrypt_pw(password)
        self.is_logged_in = False

    def _encrypt_pw(self, password):
        """Encryt the password with the user name and return the sha digest"""

        hash_string = (self.username + password)
        hash_string = hash_string.encode("utf8")
        return hashlib.sha256(hash_string).hexdigest()

    def cheack_password(self, password):
        """Return True if the password is valid for this
         user, false otherwise."""

        encrypted = self._encrypt_pw(password)
        return encrypted == self.password


class AuthExceptions(Exception):

    def __init__(self, username, user=None):
        super().__init__(username, user)
        self.username = username
        self.user = user


class UserNameAlreadyExists(AuthExceptions):
    pass


class PasswordTooShort(AuthExceptions):
    pass


class InvalidUsername(AuthExceptions):
    pass


class InvalidPassword(AuthExceptions):
    pass


class PermissionError(Exception):
    pass


class NotLoggedInError(AuthExceptions):
    pass


class NotPermittedError(AuthExceptions):
    pass


class Authenticator:
    def __init__(self):
        """Cunstruct an authentiactor to mange the in and out of the User"""
        self.users = {}

    def add_user(self, username, password):
        if username in self.users:
            raise UserNameAlreadyExists(username)
        if len(password) < 6:
            raise PasswordTooShort(username)

        self.users[username] = User(username, password)

    def login(self, username, password):
        try:
            user = self.users[username]

        except KeyError:
            raise InvalidUsername(username)

        if not user.cheack_password(password):
            raise InvalidPassword(password, user)

        user.is_logged_in = True
        return True

    def is_logged_in(self, username):
        if username in self.users:
            return self.users[username].is_logged_in

        return False


authenticator = Authenticator()


class Authorizor:
    def __init__(self, authenticator):
        self.authenticator = authenticator
        self.permissions = {}

    def add_permissions(self, perm_name):
        """Create a new permission that user can add to"""

        try:
            perm_set = self.permissions[perm_name]

        except KeyError:
            self.permissions[perm_name] = set()

        else:
            raise PermissionError("Permission exists")

    def permit_user(self, perm_name, username):

        try:
            perm_set  = self.permissions[perm_name]

        except KeyError:
            raise PermissionError("Permission Does not exist")

        else:
            if username not in self.authenticator.users:
                raise InvalidUsername
            perm_set.add(username)

    def check_permission(self, perm_name, username):
        if not self.authenticator.is_logged_in(username):
            raise NotLoggedInError(username)

        try:
            perm_set = self.permissions[perm_name]

        except KeyError:
            raise PermissionError("Permission Does not Exist")

        else:
            if username not in perm_set:
                raise NotPermittedError(username)
            else:
                return True

authorizor = Authorizor(authenticator)
