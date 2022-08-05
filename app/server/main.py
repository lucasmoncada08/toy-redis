from socket import create_server
from threading import Thread
from resp_decoder import RESPDecoder
from time import time

def main():
  print("In main logging")

  server_socket = create_server(("localhost", 6379), reuse_port=True)

  store = {}
  
  while True:
    
    client_connection, _ = server_socket.accept() # wait for client
    Thread(target=handle_connection, args=(client_connection, store,)).start()
  
def handle_connection(client_connection, store):

  while True:
    try:

      decoded = RESPDecoder(client_connection).decode()

      print(decoded)

      if decoded is None:
        break

      if isinstance(decoded, bytes):
        command = decoded.lower()
      else:
        command = decoded[0].lower()
        args = decoded[1:]

      if command == b"ping":
        client_connection.send(b"+PONG\r\n")
      elif command == b"echo":
        client_connection.send(f"${len(args[0])}\r\n{args[0].decode('utf-8')}\r\n".encode())
      elif command == b"set":
        if len(args) == 2:
          store[args[0]] = (args[1], -1)
        elif len(args) == 4:
          store[args[0]] = (args[1], time()+(int(args[3])/1000))
        client_connection.send(b"+OK\r\n")
      elif command == b"get":
        if args[0] not in store:
          client_connection.send(b"$-1\r\n")
        elif store[args[0]][1] != -1 and store[args[0]][1] < time():
          store.pop(args[0])
          client_connection.send(b"$-1\r\n")
        else:
          value = store[args[0]][0]
          client_connection.send(f"${len(value)}\r\n{value.decode('utf-8')}\r\n".encode())
      else:
        client_connection.send(b"-ERR unknown command\r\n")

      print(store)

    except ConnectionError:
      break

if __name__ == "__main__":
  main()