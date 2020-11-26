import socket
import threading

HOST = ""
PORT = 20000
origin = (HOST, PORT)

clients = dict()
cache_lock = threading.Lock()
FILE_CACHE = ("", bytearray())

# Configuração inicial do servidor
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Reaproveitando portas ocupadas (previne problemas com interrupção de execução)
udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp.bind(origin)


# Cria uma nova conexão TCP que é utilizada para transferência de arquivos
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp.bind(origin)
tcp.listen(1)

# Encerra a comunicação cliente x servidor e notifica
# outros usuários
def logout(msg, client):
    name = clients[client]
    del clients[client]
    
    broadcast = name + " saiu."
    for address in clients:
        udp.sendto(broadcast.encode(), address)
    
# Lista clientes conectados
def list_users(msg, client):
    msg = "Clientes conectados:\n"
    for address,name in clients.items():
        msg += name + ", "
    
    udp.sendto(msg[:-2].encode(), client) 


def readFile(connection, client, fileName):
    
    temp = bytearray()
    while True:
        
        print("Recieving")
        data = connection.recv(1024)
        
        if not data:
            break
        print("data=%s", data)
    
        # Write data to cache
        temp += data
    
    # Guardando os dados na cache do servidor
    with cache_lock:
        FILE_CACHE = (fileName, temp)


def getClientFile(msg, client):
    
    
    address = client
    connection, client = tcp.accept()
    t = threading.Thread(target=readFile, args=(connection, client, msg))
    t.start()
    print("Acabou")
    print(clients[address] + "enviou" + msg)


def chat(msg, client):

    name = clients[client]
    msg = name + ":" + msg
    
    for address in clients:
        if clients[address] == name:
            continue
        udp.sendto(msg.encode(), address)

    print("MSG:" + msg)
    return



def PROTOCOL(msg, client):
    
    args = msg.split()
    msg = args[0]
    
    switcher = {
            "/bye":logout,
            "/list":list_users,
            "/file":getClientFile
    }
    
    # Assumindo tudo que não seja uma mensagem válida
    # na definição do protocolo como MSG:<usuário>:<texto>
    func = switcher.get(msg, chat) 
    if args[0] == "/file":
        func(args[1], client)
    else:
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
