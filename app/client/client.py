import socket

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Client started")

    with socket.socket() as s:
      s.connect(("localhost", 6379))
      s.sendall(b"*2\r\n$4\r\nECHO\r\n$6\r\napples\r\n")
      # s.sendall(b"+PING\r\n")
      data = s.recv(1024)
    
    print(f'data recieved: {repr(data)}')

if __name__ == "__main__":
    main()