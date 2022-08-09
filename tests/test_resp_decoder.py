import unittest

from app.client import run_client

class TestClient(unittest.TestCase):

    """
    To run these integration tests, one must run the server (see readme)
    """

    # test data for client input encoding
    data = (
        ("PING", "PONG"),
        ("ping", "PONG"),

        ("Echo Hello", "Hello"),
        ("set friend john", "OK"),
        ("get friend", "john"),
    )

    def test_client_simple_commands(self):
        for test, expected in self.data:
            actual = run_client(test)
            self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()