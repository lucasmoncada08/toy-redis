from socket import create_server
from threading import Thread, Timer
from time import time
import logging
import sys
import os

# getting cwd to use when running client as a module
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(SCRIPT_DIR) not in sys.path:
  sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.resp_decoder import RESPDecoder


def main():
  logging.basicConfig(level = logging.INFO)
  logging.info("Starting Server")

  server_socket = create_server(("localhost", 6379), reuse_port=True)
  logging.info("Server Started")

  store = {} # storage of all the keys

  ActiveKeyExpire(store).run_timer()

  while True:
    client_connection, _ = server_socket.accept() # wait for client
    logging.info("Client Connected")
    Thread(target=handle_connection, args=(client_connection, store,)).start() # open a thread for each client connection

class ActiveKeyExpire:
  """Use thread timer to actively search for expired keys"""
  def __init__(self, store):
    self.store = store
  
  # timer used for active expiring of stored keys
  def run_timer(self):
    Timer(10.0, self.run_timer, [self.store]).start()
    self.active_key_expire()

  def active_key_expire(self):
    sample_size = min(len(self.store), 10)

    expired = 0 # keeping track of number of expired keys
    for key in list(self.store.keys())[:sample_size]:
      # double check key in store, account for no expiry, check if expired
      if key in self.store and self.store[key][1] > 0 and self.store[key][1] < time():
        self.store.pop(key, None)
        expired += 1
  
    # if 25% of keys were expired, run the active key expire again
    if expired > sample_size*0.25:
      self.active_key_expire()


def handle_connection(client_connection, store):
  """
  Main function used for handling all the connections. Includes while loop to handle all client inputs.

  Consider modifying the below code for a more readable and modular structure for handling different commands.
  """
  while True:
    try:

      decoded = RESPDecoder(client_connection).decode() # run essential fxn to decode RESP to readable byte strings

      if decoded is None:
        break
      
      if isinstance(decoded, bytes): # just one input
        command = decoded.lower()
        args = None
      else:
        command = decoded[0].lower()
        args = decoded[1:]

      if command == b"ping":
        client_connection.send(b"+PONG\r\n")

      elif command == b"echo":
        client_connection.send(f"${len(args[0])}\r\n{args[0].decode('utf-8')}\r\n".encode())

      elif not args:
        client_connection.send(b"+-ERR invalid number of args\r\n")

      elif command == b"set":
        if len(args) < 2 or len(args) > 4:
          client_connection.send(b"+-ERR invalid number of args\r\n")
          continue

        if len(args) == 2:
          store[args[0]] = (args[1], -1)
        elif len(args) == 3:
          store[args[0]] = (args[1], time()+(int(args[2])/1000))
        else:
          if args[2].lower() == b"px":
            store[args[0]] = (args[1], time()+(int(args[3])/1000))
          elif args[2].lower() == b"ex":
            store[args[0]] = (args[1], time()+int(args[3]))
          else:
            client_connection.send(b"+-ERR invalid unit\r\n")
        client_connection.send(b"+OK\r\n")

      elif command == b"get":
        if len(args) != 1:
          client_connection.send(b"+-ERR invalid number of args\r\n")
          continue

        if args[0] not in store:
          client_connection.send(b"+-1\r\n")
        elif store[args[0]][1] != -1 and store[args[0]][1] < time():
          store.pop(args[0])
          client_connection.send(b"+-1\r\n")
        else:
          value = store[args[0]][0]
          client_connection.send(f"${len(value)}\r\n{value.decode('utf-8')}\r\n".encode())

      elif command == b"expire":
        if len(args) < 2 or len(args) > 3:
          client_connection.send(b"+-ERR invalid number of args\r\n")
          continue

        if args[0] not in store:
          client_connection.send(b"+0\r\n")
        elif store[args[0]][1] != -1 and store[args[0]][1] < time():
          store.pop(args[0])
          client_connection.send(b"+0\r\n")
        elif len(args) == 2:
          store[args[0]] = (store[args[0]][0], time()+(int(args[1])/1000))
          client_connection.send(b"+1\r\n")
        elif len(args) == 3:
          if args[1].lower() == b"px":
            store[args[0]] = (store[args[0]][0], time()+(int(args[2])/1000))
          elif args[1].lower() == b"ex":
            store[args[0]] = (store[args[0]][0], time()+int(args[2]))
          else:
            client_connection.send(b"+-ERR invalid unit\r\n")
            continue
          client_connection.send(b"+1\r\n")
          
      else:
        client_connection.send(b"+-ERR unknown command\r\n")

    except ConnectionError:
      break

if __name__ == "__main__":
  main()