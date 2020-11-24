import socket
import threading

HOST = ""
PORT = 20000
origin = (HOST, PORT)

clients = set()
clients_lock = threading.Lock()
"""
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
"""

# Configuração inicial do servidor
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Reaproveitando portas ocupadas (previne problemas com interrupção de execução)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp.bind(origin)

try:
    while True:
        
        # Recebendo mensagem do cliente
        msg, client = udp.recvfrom(1024)
        msg = msg.decode()
        
        if msg.find("USER") != -1:
            new_client = msg.split(":")[1]
            for (name, address) in clients:
                broadcastMsg = new_client + " acabou de entrar"
                udp.sendto(broadcastMsg.encode(), address)
            if (new_client,client) not in clients:
                print(client, msg)
                clients.add((new_client,client))

        # Lista clientes conectados
        if msg == "/list":
            
            msg = "Clientes conectados:\n"
            for (name, address) in clients:
                msg += name + ", "
            
            udp.sendto(msg[:-2].encode(), client) 

        if msg == "BYE":
            qual = ""
            for (name, address) in clients:
                if address == client:
                    qual = name
                    break
            clients.remove((qual, client))
            for (name, address) in clients:
                msg = qual + " saiu."
                udp.sendto(msg.encode(), address)



    udp.close()

finally:
    print("oi")
