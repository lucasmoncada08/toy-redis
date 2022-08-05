import socket

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Client started")

    with socket.socket() as s:
      s.connect(("localhost", 6379))
      # s.sendall(b"*3\r\n$3\r\nSET\r\n$4\r\nname\r\n$5\r\nlucas\r\n")
      # s.sendall(b"*3\r\n$3\r\nSET\r\n$5\r\nlucas\r\n$7\r\nmoncada\r\n")
      s.sendall(b"*2\r\n$3\r\nGET\r\n$4\r\nnaml\r\n")

      # s.sendall(b"+PING\r\n")
      data = s.recv(1024)
    
    print(f'data recieved: {repr(data)}')

if __name__ == "__main__":
    main()