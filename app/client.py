import socket

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Client started")

    with socket.socket() as s:
      s.connect(("localhost", 6379))
      s.sendall(b"hello world")
      data = s.recv(1024)
    
    print(f'data recieved: {repr(data)}')

    # server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    # client_connection, _ = server_socket.accept() # wait for client

    # client_connection.recv(1024)
    # client_connection.send(b"+PONG\r\n")

if __name__ == "__main__":
    main()