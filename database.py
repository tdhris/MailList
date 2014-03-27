import sqlite
import os


class DataBase:
    def __init__(self):
        self.database_name = "mailing_lists.db"
        self._ensure_db_file()
        self._ensure_table("mailing_lists", '(list_id, list_name)')
        self._ensure_table("subscribers", '(subscriber_id, name, email)')
        self._ensure_table("subscriber_list_ids", '(subscriber_id, list_id)')
        self.connection = sqlite.connect(self.database_name)
        self.cursor = self.connection.cursor()

    def get_subscribers(self):
        subscribers = self.cursor.execute("SELECT subscriber_id, name, email FROM subscribers")
        return subscribers

    def get_list_content(self, list_id):
        self.cursor.execute("SELECT subscriber_id FROM subscriber_list_ids WHERE list_id = ?", (list_id))

    def save_list(self, mail_list, subscribers):
        list_id = self.get_list_id(mail_list)
        #delete all subscribers previously in the list until now
        self.cursor.execute("DELETE FROM subscriber_list_ids WHERE list_id = ?", (int(list_id),))
        #insert current list
        for subscriber in subscribers:
            self.cursor.execute("INSERT INTO subscriber_list_ids VALUES (?, ?)", (int(list_id), int(subscriber)))

    def get_list_id(self, list_name):
        lists = self.cursor.execute("SELECT list_id, list_name FROM mailing_lists")
        for list in lists:
            if list_name == list[1]:
                return list[0]


    def _ensure_table(self, table_name, columns):
        sql_command = '''create table if not exists " + table_name + columns'''
        self.cursor.execute(sql_command)

    def _ensure_db_file(self):
        if not os.path.isfile(self.database_name):
            os.system(self.database_name)
