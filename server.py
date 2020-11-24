import socket
import threading

HOST = ""
PORT = 20000
origin = (HOST, PORT)


clients = set()
clients_lock = threading.Lock()
def broadcast(msg):
    with clients_lock:
        for (connection) in clients:
            print(connection)
            connection.send(msg.encode())

def connected(connection, client):
    print(client, "connected")

    while True:
        msg = connection.recv(1024).decode()
        if msg == "/bye" or not msg:
            break
        elif msg == "/all":
            broadcast(msg)
        #print(client, msg)
    
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
       
        with clients_lock:
            clients.add(connection)
        
        t = threading.Thread(target=connected, args=(connection, client))
        t.start()

    tcp.close()
finally:
    connection.close()
