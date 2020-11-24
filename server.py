import socket
import threading

HOST = ""
PORT = 20000
origin = (HOST, PORT)

clients = dict()
clients_lock = threading.Lock()

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
        
        # Cadastrando o login do usuário no servidor
        if client not in clients:
            name = msg.split(":")[1] 
            for address in clients:
                broadcast = name + " entrou"
                udp.sendto(broadcast.encode(), address)
            print("Adding ", client, name)
            clients[client] = name
        
        # Lista clientes conectados
        if msg == "/list":
            
            msg = "Clientes conectados:\n"
            for address,name in clients.items():
                msg += name + ", "
            
            udp.sendto(msg[:-2].encode(), client) 

        if msg == "/bye":    
            name = clients[client]
            del clients[client]
            
            for address in clients:
                broadcast = name + " saiu."
                udp.sendto(broadcast.encode(), address)


    udp.close()

finally:
    print("Servidor encerrado.")
