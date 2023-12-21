import socket
import threading

HOST = "10.0.2.15"
PORT = 9998
def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    server.listen(5)
    print(f'[*] Listening on {HOST}:{PORT}')

    while True:
        client,addr = server.accept()
        print(f'[*] Accepted Connection Established {addr[0]}:{addr[1]}')
        client_thread = threading.Thread(target=client_handler,args=(client,))
        client_thread.start()

def client_handler(client):
    with client as sock:
        request = sock.recv(1024)
        print(f"[*] Received: {request.decode('utf-8')}")
        sock.send(b"ACK")

if __name__=="__main__":
    main()
    