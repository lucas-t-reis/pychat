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

# Encerra a comunicação cliente x servidor e notifica
# outros usuários
def logout(msg, client):
    name = clients[client]
    del clients[client]
    
    for address in clients:
        broadcast = name + " saiu."
        udp.sendto(broadcast.encode(), address)
    
# Lista clientes conectados
def list_users(msg, client):
    msg = "Clientes conectados:\n"
    for address,name in clients.items():
        msg += name + ", "
    
    udp.sendto(msg[:-2].encode(), client) 

def chat(msg, client):
    print(clients[client] + ":" + msg)
    return

def PROTOCOL(msg, client):
    
    switcher = {
            "/bye":logout,
            "/list":list_users,
    }
    
    # Assumindo tudo que não seja uma mensagem válida
    # na definição do protocolo como MSG:<usuário>:<texto>
    func = switcher.get(msg, chat) 
    func(msg, client)

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
            continue

        PROTOCOL(msg, client)
        
    udp.close()

finally:
    print("Servidor encerrado.")
