class Subscriber:
    def __init__(self, name, email):
        self._name = name
        self._email = email

    def get_name(self):
        return self._name

    def change_name(self, name):
        self._name = name

    def get_email(self):
        return self._email

    def change_email(self, email):
        self._email = email
