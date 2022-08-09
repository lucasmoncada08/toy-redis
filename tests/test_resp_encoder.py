import unittest

from app.client import RESPEncoder

class TestRESPEncoder(unittest.TestCase):

    # test data for client input encoding
    data = (
        ("PING", b"+PING\r\n"),
        ("ping", b"+ping\r\n"),
        ("test12345", b"+test12345\r\n"),

        ("Echo Hello", b"*2\r\n$4\r\nEcho\r\n$5\r\nHello\r\n"),
        ("get name", b"*2\r\n$3\r\nget\r\n$4\r\nname\r\n"),
        ("set friend john", b"*3\r\n$3\r\nset\r\n$6\r\nfriend\r\n$4\r\njohn\r\n"),

        (" incorrect", b"+Invalid\r\n"),
        ("", b"+Invalid\r\n")
    )

    re = RESPEncoder()

    def test_encode(self):
        for test, expected in self.data:
            actual = self.re.encode(test)
            self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()