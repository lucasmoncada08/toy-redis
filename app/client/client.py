import sys
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(SCRIPT_DIR) not in sys.path:
  sys.path.append(os.path.dirname(SCRIPT_DIR))



import socket
from client.resp_encoder import RESPEncoder
# from resp_encoder import RESPEncoder


def run_client():
  print(f'sys.path in fn: {sys.path}')

  print("Client started")

  re = RESPEncoder()

  with socket.socket() as s:
    s.connect(("localhost", 6379))
    # s.sendall(b"*3\r\n$3\r\nSET\r\n$4\r\nname\r\n$5\r\nlucas\r\n")
    # s.sendall(b"*3\r\n$3\r\nSET\r\n$5\r\nlucas\r\n$7\r\nmoncada\r\n")
    # s.sendall(b"*2\r\n$3\r\nGET\r\n$4\r\nname\r\n")
    # s.sendall(b"*2\r\n$3\r\nGET\r\n$5\r\nlucas\r\n")

    # s.sendall(b"*4\r\n$3\r\nSET\r\n$5\r\nlucas\r\n$7\r\nmoncada\r\n$2\r\n10\r\n")
    while True:
      inp = input("Enter Command\n")

      if inp == "exit":
        break

      if len(inp) == 0 or len(inp) >= 500:
        print(f'Invalid length: {len(inp)}. Length range: (0, 500)')
        continue

      enc_inp = re.encode(inp)
      print(enc_inp)

      s.sendall(enc_inp)
      data = s.recv(1024)
      
      print(f'data recieved: {repr(data)}')

    # return data

if __name__ == "__main__":
  run_client()
  pass