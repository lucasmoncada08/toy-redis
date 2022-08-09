import unittest

from app.client import run_client
# from app.client.resp_encoder import encode

class TestClient(unittest.TestCase):
  def test_handle_client(self):
    val = run_client()
    self.assertEqual(val, b"+PONG\r\n")

if __name__ == "__main__":
  unittest.main()

