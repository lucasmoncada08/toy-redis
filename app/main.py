from pydoc import cli
import socket 

def main():
  print("In main logging")

  server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
  client_connection, _ = server_socket.accept() # wait for client

  client_connection.recv(1024)
  client_connection.send(b"+PONG\r\n")

if __name__ == "__main__":
  main()