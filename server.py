import socket
import threading

HOST = ""
PORT = 20000
origin = (HOST, PORT)

def connected(connection, client):
    print(client, "connected")
    
    while True:
        msg = connection.recv(1024).decode()
        if msg == "/bye" or not msg:
            break
        print(client, msg)
    
    print("Closing connection with client", client)
    connection.close()

    return


tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcp.bind(origin)
tcp.listen(1)

try:
    while True:
        connection, client = tcp.accept()
        t = threading.Thread(target=connected, args=(connection, client))
        t.start()

    tcp.close()
finally:
    connection.close()
