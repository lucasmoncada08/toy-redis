from socket import create_server
from threading import Thread
from resp_decoder import RESPDecoder

def main():
  print("In main logging")

  server_socket = create_server(("localhost", 6379), reuse_port=True)
  
  while True:
    client_connection, _ = server_socket.accept() # wait for client
    Thread(target=handle_connection, args=(client_connection,)).start()
    # handle_connection(client_connection)
  
def handle_connection(client_connection):
  while True:
    try:

      decoded = RESPDecoder(client_connection).decode()

      # print(f'decoded: {decoded}')

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
      else:
        client_connection.send(b"-ERR unknown command\r\n")

    except ConnectionError:
      break

if __name__ == "__main__":
  main()