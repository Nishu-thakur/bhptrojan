import socket

target_host = "10.0.2.15"
port = 9998

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect((target_host,port))

client.send(b'GET /HTTP/1.1\r\nHost: google.com\r\n\r\n')

response = client.recv(4096)

print(response.decode())

client.close()
