from socket import create_server
from threading import Thread
from resp_decoder import RESPDecoder

def main():
  print("In main logging")

  server_socket = create_server(("localhost", 6379), reuse_port=True)

  store = {}
  print('reset store')
  
  while True:
    
    client_connection, _ = server_socket.accept() # wait for client
    Thread(target=handle_connection, args=(client_connection, store,)).start()
  
def handle_connection(client_connection, store):

  while True:
    try:

      decoded = RESPDecoder(client_connection).decode()

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
        store[args[0]] = args[1]
        client_connection.send(b"+OK\r\n")
      elif command == b"get":
        # print(args[0])
        # print(store)
        # print(store[b'name'])
        if args[0] not in store:
          client_connection.send(b"-Invalid Key\r\n")
        else:
          value = store[args[0]]
          client_connection.send(f"${len(value)}\r\n{value.decode('utf-8')}\r\n".encode())
      else:
        client_connection.send(b"-ERR unknown command\r\n")
      
      print(f'store: {store}')
      # print(f'store[b"name"]: {store[b"name"]}')

    except ConnectionError:
      break

if __name__ == "__main__":
  main()