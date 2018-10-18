import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65433        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(b'Client connected.')
data = s.recv(1024)

print('Received', repr(data))

while(True):
    inp = input()

    
    if inp != '':
        if inp == 'quit':
            s.close()
            break
        s.sendall(inp.encode())
