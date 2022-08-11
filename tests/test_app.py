import unittest
from time import sleep

from app.client import run_client

class TestApp(unittest.TestCase):

    """
    To run these integration tests, one must run the server (see readme)
    """

    # test data for client input encoding
    simple_commands_data = (
        ("PING", "PONG"),
        ("ping", "PONG"),

        ("Echo Hello", "Hello"),
        ("set friend john", "OK"),
        ("get friend", "john"),
    )

    # test invalid commands
    invalid_commands = (
        ("set friend", "-ERR invalid number of args"),
        ("get friend john", "-ERR invalid number of args"),
        ("expire name", "-ERR invalid number of args"),
        ("expire name px or ex 10000", "-ERR invalid number of args"),
        ("get", "-ERR invalid number of args"),
        
        ("set name friend", "OK"),
        ("expire name bx 1", "-ERR invalid unit"),
        ("set name friend", "-ERR invalid unit"),

        ("name friend", "-ERR unknown command"),
        ("getset name friend", "-ERR unknown command"),
    )

    # testing functionality that relies on expiring items
    expire_test_data = (
        ("set hello world 2000", 0, "OK"),
        ("get hello", 3, "world"),
        ("get hello", 0, "-1"),
        ("set world hello ex 1", 0, "OK"),
        ("get world", 2, "hello"),
        ("get world", 0, "-1"),

        ("set hello world", 0, "OK"),
        ("expire hello 2000", 0, "1"),
        ("get hello", 3, "world"),
        ("get hello", 0, "-1"),
        ("set world hello px 1000", 0, "OK"),
        ("expire world px 5000", 2, "1"),
        ("get world", 4, "hello"),
        ("get world", 0, "-1"),
    )

    # testing the simple commands without expiration
    def test_client_simple_commands(self):
        for test, expected in self.simple_commands_data:
            actual = run_client(test)
            self.assertEqual(expected, actual)
    
    # testing the invalid commands
    def test_invalid_commands(self):
        for test, expected in self.invalid_commands:
            actual = run_client(test)
            self.assertEqual(expected, actual)

    # testing commands that use expiration functionality
    def test_expire_commands(self):
        for test, sleep_time, expected in self.expire_test_data:
            actual = run_client(test)
            self.assertEqual(expected, actual)
            sleep(sleep_time)

if __name__ == "__main__":
    unittest.main()