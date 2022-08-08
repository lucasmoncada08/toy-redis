from http import client
import socket

def main():
    run_client()

def run_client():

  print("Client started")

  with socket.socket() as s:
    s.connect(("localhost", 6379))
    # s.sendall(b"*3\r\n$3\r\nSET\r\n$4\r\nname\r\n$5\r\nlucas\r\n")
    # s.sendall(b"*3\r\n$3\r\nSET\r\n$5\r\nlucas\r\n$7\r\nmoncada\r\n")
    # s.sendall(b"*2\r\n$3\r\nGET\r\n$4\r\nname\r\n")
    # s.sendall(b"*2\r\n$3\r\nGET\r\n$5\r\nlucas\r\n")

    # s.sendall(b"*4\r\n$3\r\nSET\r\n$5\r\nlucas\r\n$7\r\nmoncada\r\n$2\r\n10\r\n")


    s.sendall(b"+PING\r\n")
    data = s.recv(1024)
    
    print(f'data recieved: {repr(data)}')
    return data

if __name__ == "__main__":
    main()