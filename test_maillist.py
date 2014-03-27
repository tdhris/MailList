import unittest
from maillist import MailList
from subscriber import Subscriber

class MailListTest(unittest.TestCase):
    """docstring for MailListTest"""

    def setUp(self):
        # fuck static
        self.m = MailList("Hack Bulgaria")

    def test_create_mail_list_get_name(self):
        self.assertEqual("Hack Bulgaria", self.m.get_name())

    def test_add_subscriber(self):
        subscriber = Subscriber("Rado", "radorado@hackbulgaria.com")
        self.m.add_subscriber(subscriber)

        self.assertEqual(1, self.m.count())

    def test_get_subscribers(self):
        subscriber = Subscriber("Rado", "radorado@hackbulgaria.com")
        self.m.add_subscriber(subscriber)

        expected = [("Rado", "radorado@hackbulgaria.com")]
        self.assertEqual(expected, self.m.get_subscribers())


    def test_add_subscriber_with_same_email_address(self):
        subscriber_email = "radorado@hackbulgaria.com"
        subscriber_1 = Subscriber("Rado", subscriber_email)
        subscriber_2 = Subscriber("Rado Rado", subscriber_email)

        add1 = self.m.add_subscriber(subscriber_1)
        add2 = self.m.add_subscriber(subscriber_2)

        self.assertEqual(1, self.m.count())
        self.assertTrue(add1)
        self.assertFalse(add2)
        subscriber = self.m.get_subscriber_by_email(subscriber_email)
        self.assertEqual("Rado", subscriber.get_name())

    def test_add_get_subscriber_by_email(self):
        subscriber = Subscriber("Rado", "radorado@hackbulgaria.com")
        self.m.add_subscriber(subscriber)

        result = self.m.get_subscriber_by_email("radorado@hackbulgaria.com")
        self.assertEqual("Rado", result.get_name())

    def test_add_get_subscriber_by_email_when_not_there(self):
        self.assertIsNone(self.m.get_subscriber_by_email("asd@asd.com"))

    def test_update_subscriber_changing_name(self):
        subscriber = Subscriber("Rado", "rado@rado.com")
        self.m.add_subscriber(subscriber)
        self.m.update_subscriber("rado@rado.com",
                                 {"name": "Radoslav Georgiev"})

        sub = self.m.get_subscriber_by_email("rado@rado.com")
        self.assertEqual("Radoslav Georgiev",
                         sub.get_name())

    def test_update_subscriber_changing_email(self):
        subscriber = Subscriber("Rado", "rado@rado.com")
        self.m.add_subscriber(subscriber)
        self.m.update_subscriber("rado@rado.com",
                                 {"email": "radorado@rado.com"})

        self.assertEqual("radorado@rado.com",
                         self.m.get_subscriber_by_email("radorado@rado.com").get_email())

    def test_update_subscriber_changing_name_and_email(self):
        subscriber = Subscriber("Rado rado", "rado@rado.com")
        self.m.add_subscriber(subscriber)
        self.m.update_subscriber("rado@rado.com",
                                 {"name": "Radoslav Georgiev",
                                  "email": "radorado@rado.com"})

        self.assertEqual("Radoslav Georgiev",
                         self.m.get_subscriber_by_email("radorado@rado.com").get_name())

    def test_remove_subscriber(self):
        subscriber = Subscriber("Rado", "radorado@hackbulgaria.com")
        self.m.add_subscriber(subscriber)
        self.m.remove_subscriber("radorado@hackbulgaria.com")

        self.assertEqual(0, self.m.count())

    def test_remove_subscriber_when_not_there(self):
        self.assertIsNone(self.m.remove_subscriber("rado@radorado.com"))
