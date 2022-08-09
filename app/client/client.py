import sys
import os
import warnings
import socket

# ignoring import warning due to multiple same imports
warnings.filterwarnings("ignore")

# getting cwd to use when running client as a module
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(SCRIPT_DIR) not in sys.path:
  sys.path.append(os.path.dirname(SCRIPT_DIR))

from client.resp_encoder import RESPEncoder
from utils.resp_decoder import RESPDecoder

def run_client(test: str=None):

  print("<  Client Started")

  re_encode = RESPEncoder()

  with socket.socket() as s:
    s.connect(("localhost", 6379))
    print("<  Client Connected\n")
    # s.sendall(b"*3\r\n$3\r\nSET\r\n$4\r\nname\r\n$5\r\nlucas\r\n")
    # s.sendall(b"*3\r\n$3\r\nSET\r\n$5\r\nlucas\r\n$7\r\nmoncada\r\n")
    # s.sendall(b"*2\r\n$3\r\nGET\r\n$4\r\nname\r\n")
    # s.sendall(b"*2\r\n$3\r\nGET\r\n$5\r\nlucas\r\n")

    # s.sendall(b"*4\r\n$3\r\nSET\r\n$5\r\nlucas\r\n$7\r\nmoncada\r\n$2\r\n10\r\n")
    data = None
    test_flag = False # to check if the test has been run
    while True:
      
      # if tests are provided, use them, else get user input
      if test is not None:
        if test_flag:
          break
        inp = test
        test_flag = True
      else:
        inp = input(">  ")

      if inp == "exit":
        print("<  Exiting")
        break

      if len(inp) == 0 or len(inp) >= 500:
        print(f'Invalid length: {len(inp)}. Length range: (0, 500)')
        continue

      enc_inp = re_encode.encode(inp)

      # print(f'enc_inp: {enc_inp}')

      s.sendall(enc_inp)
      
      # first decode is custom decode and second if from bytes to string
      data = RESPDecoder(s).decode().decode("utf-8")

      print(f'<  {data}\n')

    return data

if __name__ == "__main__":
  run_client()
