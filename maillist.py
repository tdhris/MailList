from subscriber import Subscriber


class MailList():
    """docstring for MailList"""
    def __init__(self, name):
        self.__name = name
        self.subscribers = []

    def add_subscriber(self, subscriber):
        emails = [member.get_email() for member in self.subscribers]
        if subscriber.get_email() in emails:
            return False
        self.subscribers.append(subscriber)
        return True

    def get_name(self):
        return self.__name

    def count(self):
        return len(self.subscribers)

    def get_subscriber_by_email(self, email):
        for subscriber in self.subscribers:
            if subscriber.get_email() == email:
                return subscriber

        return None

#returns tuple (name, email)
    def get_subscribers(self):
        subscribers = []
        for subscriber in self.subscribers:
            subscribers.append((subscriber.get_name(), subscriber.get_email()))
        return subscribers


    def update_subscriber(self, email, update_hash):
        for subscriber in self.subscribers:
            if subscriber.get_email() == email:
                if "email" in update_hash:
                    new_email = update_hash["email"]
                    subscriber.change_email(new_email)
                if "name" in update_hash:
                    new_name = update_hash["name"]
                    subscriber.change_name(new_name)

    def remove_subscriber(self, email):
        for subscriber in self.subscribers:
            if subscriber.get_email() == email:
                self.subscribers.remove(subscriber)
                break
        return None
