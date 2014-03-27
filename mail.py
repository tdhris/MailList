from commandparser import CommandParser
from maillist import MailList
from subscriber import Subscriber
from sql_adapter import SQLRelationList
import sys


class MailListProgram():
    """docstring for MailListProgram"""
    def __init__(self):
        self.cp = CommandParser()
        self.lists = {}
        self.db_path = "lists/"
        self.adapter = SQLRelationList(self.db_path)

        self._load_initial_state()
        self._init_callbacks()
        self._loop()

    def create_list_callback(self, arguments):
        name = " ".join(arguments)
        maillist = MailList(name)
        list_id = self.adapter.sql_mail.save(name)
        self.lists[list_id] = maillist

    def add_subscriber_callback(self, arguments):
        list_id = int("".join(arguments))
        name = input("name>")
        email = input("email>")
        subscriber = Subscriber(name, email)

        if self.lists[list_id].add_subscriber(subscriber):
        #add subscriber to the database and get subscriber id
            subscriber_id = self.adapter.sql_subscriber_table.save(subscriber)
        #add the list_id<->subscriber_id relation to the relation table
            self.adapter.add_relation(list_id, subscriber_id)
        # self._notify_save(list_id)

    def show_lists_callback(self, arguments):
        for list_id in self.lists:
            current_list = self.lists[list_id]
            print("[{}] {}".format(list_id,
                                   current_list.get_name()))

    def show_list_callback(self, arguments):
        list_id = int("".join(arguments))

        if list_id in self.lists:
            subscribers = self.lists[list_id].get_subscribers()
            for s in subscribers:
                print("{} - {}".format(s[0], s[1]))
        else:
            print("List with id <{}> was not found".format(list_id))

    def exit_callback(self, arguments):
        sys.exit(0)

#load all lists in the database into self.lists
    def _load_initial_state(self):
        lists = self.adapter.sql_mail.get_lists()
        for unparsed_list in lists:
            list_id = unparsed_list[0]
            list_name = unparsed_list[1]
            maillist = MailList(list_name)
            #load list subscribers
            subscribers = self.adapter.get_subscribers_in_list(list_id)
            for subscriber in subscribers:
                maillist.subscribers.append(subscriber)
            self.lists[list_id] = maillist

    def _init_callbacks(self):
        self.cp.on("create", self.create_list_callback)
        self.cp.on("add", self.add_subscriber_callback)
        self.cp.on("show_lists", self.show_lists_callback)
        self.cp.on("show_list", self.show_list_callback)
        self.cp.on("exit", self.exit_callback)
        # TODO - implement the rest of the callbacks

    # def _notify_save(self, list_id):
    #     self.lists[list_id].save()

    def _loop(self):
        while True:
            command = input(">")
            self.cp.take_command(command)


if __name__ == '__main__':
    MailListProgram()
