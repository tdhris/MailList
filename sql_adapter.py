import os
from maillist import MailList
from subscriber import Subscriber
import sqlite3


class SQLAdapter:
    def __init__(self, db_path, mail_list=None):
        self.db_path = db_path
        self.database_name = "mailing_lists.db"
        self._ensure_db_path()
        self.connection = sqlite3.connect("mailing_lists.db")
        self.cursor = self.connection.cursor()

    def _ensure_db_path(self):
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)

    def _ensure_table(self, table_name, table_columns):
        sql_command = 'CREATE TABLE IF NOT EXISTS ' + self.table + table_columns
        self.cursor.execute(sql_command)


class SQLMailList(SQLAdapter):
    def __init__(self, db_path):
        super().__init__(db_path)
        self.table = 'mailing_lists'
        super()._ensure_table(self.table, '(list_id INTEGER PRIMARY KEY, list_name)')

    def save(self, list_name):
        self.cursor.execute("INSERT INTO {0} (list_name) VALUES (?)".format(self.table), (list_name,))
        self.connection.commit()

        return self.cursor.lastrowid

    def get_lists(self):
        unparsed_lists = self.cursor.execute("SELECT * FROM {0}".format(self.table))
        lists = [(unparsed_list[0], unparsed_list[1]) for unparsed_list in unparsed_lists]
        return lists


class SQLSubscriberList(SQLAdapter):
    def __init__(self, db_path):
        super().__init__(db_path)
        self.table = 'subscribers'
        super()._ensure_table(self.table, '(subscriber_id INTEGER PRIMARY KEY, name, email)')

    def save(self, subscriber):
        self.cursor.execute("INSERT INTO {0} (name, email) VALUES (?, ?)".format(self.table),
                           (subscriber.get_name(), subscriber.get_email()))
        self.connection.commit()

        # subscriber_id = self.cursor.execute("SELECT subscriber_id FROM {0} WHERE email = ?".format(self.table), (subscriber.get_email(),))
        return self.cursor.lastrowid

    def get_subscriber(self, subscriber_id):
        self.cursor.execute("SELECT name, email FROM {0} WHERE subscriber_id = ?".format(self.table),
                                           (int(subscriber_id),))
        unparsed_info = self.cursor.fetchone()
        name = unparsed_info[0]
        email = unparsed_info[1]
        subscriber = Subscriber(name, email)
        return subscriber


class SQLRelationList(SQLAdapter):
    def __init__(self, db_path):
        super().__init__(db_path)
        self.table = 'ralation_ids'
        super()._ensure_table(self.table, '(list_id, subscriber_id)')
        self.sql_mail = SQLMailList(db_path)
        self.sql_subscriber_table = SQLSubscriberList(db_path)

    def add_relation(self, list_id, subscriber_id):
        self.cursor.execute('INSERT INTO {0} VALUES (?, ?)'.format(self.table), (int(list_id), int(subscriber_id)))
        self.connection.commit()

#returns all the subscribers in a list
    def get_subscribers_in_list(self, m_list_id):
        self.cursor.execute("SELECT subscriber_id FROM {0} WHERE list_id = ?".format(self.table), (int(m_list_id),))
        ids = self.cursor.fetchone()
        subscribers = []
        if ids is not None:
            for subscriber_id in ids:
                subscriber = self.sql_subscriber_table.get_subscriber(subscriber_id)
                subscribers.append(subscriber)
        return subscribers

#returns a list of the names of all maillists that the subscriber is on
    def get_lists_of_subscriber(self, subscriber_id):
        mail_ids = self.cursor.execute("SELECT list_name")
