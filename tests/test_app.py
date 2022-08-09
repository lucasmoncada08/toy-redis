import unittest

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

    # test set without expire
    test_invalid_commands = (
        ("set friend john", "OK"),
        ("get friend john", "john")
    )


    # test set with expire from set
    # test expire

    def test_client_simple_commands(self):
        for test, expected in self.simple_commands_data:
            actual = run_client(test)
            self.assertEqual(expected, actual)
    


if __name__ == "__main__":
    unittest.main()