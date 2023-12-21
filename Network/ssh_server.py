import os
import paramiko
import socket
import sys
import threading

CMD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CMD,'test_rsa.key'))


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
    
    def check_channel_request(self,kind,chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self,username,password):
        if(username=='tim' and password=='ssh'):
            return paramiko.AUTH_SUCCESSFUL

if __name__=="__main__":
    server = '0.0.0.0'
    port = 9998
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind((server,port))
        sock.listen(5)
        print('[+] Listening For connection...')
        client, addr = sock.accept()
    except Exception as e:
        print('[+] Listen Failed: '+str(e))
        sys.exit(0)
    else:
        print('[+] Got a connection ',client,addr)
    
    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTKEY)
    server = Server()
    bhSession.start_server(server=server)

    chan = bhSession.accept(20)
    if chan is None:
        print("***No Channel")
        sys.exit(1)
    
    print('[+] Authenication')
    print(chan.recv(1024))
    chan.send('Welcome to bh_sssh')

    try:
        while True:
            command = input("Enter command:")
            if command!='exit':
                chan.send(command)
                r = chan.recv(8192)
                print(r.decode())
            else:
                chan.send('exit')
                print("Existing")
                bhSession.close()
                break
    except Exception as e:
        bhSession.close()
        
