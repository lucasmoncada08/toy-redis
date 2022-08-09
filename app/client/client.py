import sys
import os
# import logging
import warnings
import time

# ignoring import warning due to multiple same imports
warnings.filterwarnings("ignore")

# getting cwd to use when running client as a module
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(SCRIPT_DIR) not in sys.path:
  sys.path.append(os.path.dirname(SCRIPT_DIR))

import socket
from client.resp_encoder import RESPEncoder

def run_client():

  print("<  Client Started\n")

  re = RESPEncoder()

  with socket.socket() as s:
    s.connect(("localhost", 6379))
    print("<  Client Connected")
    # s.sendall(b"*3\r\n$3\r\nSET\r\n$4\r\nname\r\n$5\r\nlucas\r\n")
    # s.sendall(b"*3\r\n$3\r\nSET\r\n$5\r\nlucas\r\n$7\r\nmoncada\r\n")
    # s.sendall(b"*2\r\n$3\r\nGET\r\n$4\r\nname\r\n")
    # s.sendall(b"*2\r\n$3\r\nGET\r\n$5\r\nlucas\r\n")

    # s.sendall(b"*4\r\n$3\r\nSET\r\n$5\r\nlucas\r\n$7\r\nmoncada\r\n$2\r\n10\r\n")
    while True:
      inp = input(">  ")

      if inp == "exit":
        print("<  Exiting")
        break

      if len(inp) == 0 or len(inp) >= 500:
        print(f'Invalid length: {len(inp)}. Length range: (0, 500)')
        continue

      enc_inp = re.encode(inp)

      s.sendall(enc_inp)

      # time.sleep(1)
      
      data = s.recv(1024)

      print(f'<  {repr(data)}\n')

    return data

if __name__ == "__main__":
  run_client()
