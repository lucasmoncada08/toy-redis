from socket import create_server
from threading import Thread
from resp_decoder import RESPDecoder

def main():
  print("In main logging")

  server_socket = create_server(("localhost", 6379), reuse_port=True)
  
  while True:
    client_connection, _ = server_socket.accept() # wait for client
    Thread(target=handle_connection, args=(client_connection,)).start()
  
def handle_connection(client_connection):
  while True:
    try:
      # if len(data) < 1:
      #   break

      command = RESPDecoder(client_connection).decode()

      if command == b"ping":
        client_connection.send(b"+PONG\r\n")
      elif command == b"echo":
        client_connection.send(b"+ECHO\r\n")
      else:
        client_connection.send(b"-ERR unknown command\r\n")

    except ConnectionError:
      break
  
def handle_array(data):
  return b"+Array\r\n"

if __name__ == "__main__":
  main()