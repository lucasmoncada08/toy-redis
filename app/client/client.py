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

    data = None
    test_flag = False # to check if the test has been run

    # run until exit is input
    while True:
      
      # if tests are provided, use them, else get user input
      if test is not None:
        if test_flag:
          break
        inp = test
        test_flag = True
      else:
        inp = input(">  ") # client waits for user input

      if inp == "exit":
        print("<  Exiting")
        break

      if len(inp) == 0 or len(inp) >= 500:
        print(f'Invalid length: {len(inp)}. Length range: (0, 500)')
        continue

      enc_inp = re_encode.encode(inp)

      s.sendall(enc_inp) # send encoded input back to server
      
      # first decode is custom decode and second if from bytes to string
      data = RESPDecoder(s).decode().decode("utf-8")

      print(f'<  {data}\n')

    return data

if __name__ == "__main__":
  run_client()
