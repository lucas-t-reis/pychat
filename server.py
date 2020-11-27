import socket
import threading

HOST = ""
PORT = 20000
origin = (HOST, PORT)

clients = dict()
cache_lock = threading.Lock()
FILE_CACHE = "null"

# Configuração inicial do servidor e reaproveitando 
# as portas ocupadas (previne problemas com interrupção de execução)
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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

    # Imprimindo Log na tela do servidor (Feedback)
    print("BYE (" + clients[client] + ")")

    name = clients[client]
    del clients[client]


    broadcast = name + " saiu."
    for address in clients:
        udp.sendto(broadcast.encode(), address)
    
# Lista clientes conectados
def list_users(msg, client):

	# Imprimindo Log na tela do servidor (Feedback)
    print("LIST (" + clients[client] + ")")

    msg = "Clientes conectados:\n"
    for address,name in clients.items():
        msg += name + ", "
    
    udp.sendto(msg[:-2].encode(), client) 

# Método assíncrono para leitura dos arquivos enviados pelo cliente.
# Instancia uma thread para gerenciar cada conexão requisitada.
def readFile(connection, client, udp_address, fileName):
    
    global FILE_CACHE 
    temp = bytearray()
    
	# Imprimindo Log na tela do servidor (Feedback)
    print("FILE:" + fileName + " (" + clients[udp_address] + ")")
    
    while True:
        
        data = connection.recv(1024)
        
        if not data:
            break
    
        # Write data to cache
        temp += data
    
    # Guardando os dados na cache do servidor
    with cache_lock:
        FILE_CACHE = fileName
        msg = clients[udp_address] + " enviou " + fileName

        for address in clients:
            if address == udp_address:
                continue
            udp.sendto(msg.encode(), address)

    with open(fileName, "wb") as file:
        file.write(temp)


def getClientFile(msg, client):
    
    udp_address = client
    connection, client = tcp.accept()
    t = threading.Thread(target=readFile, args=(connection, client, udp_address, msg))
    t.start()

def sendFile(connection, client, udp_address, msg):

	# Imprimindo Log na tela do servidor (Feedback)
    print("GET: " + FILE_CACHE + " (" + clients[udp_address] + ")")

    with open(FILE_CACHE, "rb") as file:
        while(payload := file.read(1024)):
            connection.send(payload)
    udp.sendto("Arquivo enviado\n".encode(), udp_address)

def processFileRequest(msg, client):
    
    if FILE_CACHE != msg:
        error_msg = "Arquivo inexistente.\n"
        udp.sendto(error_msg.encode(), client)
        
        return

    udp_address = client
    connection, client = tcp.accept()
    t = threading.Thread(target=sendFile, args=(connection, client, udp_address, msg), daemon=True)
    t.start()

def chat(msg, client):

    name = clients[client]
    print("MSG:<" + name + ">:" + msg)
    msg = name + ":" + msg
    
    for address in clients:
        if clients[address] == name:
            continue
        udp.sendto(msg.encode(), address)


def PROTOCOL(msg, client):
    
    args = msg.split()
    cmd = args[0]
    
    # Se o primeiro comando digitado não for nenhum dos 
    # três casos abaixo, o comportamento padrão é assumir
    # mensagem de texto a.k.a chat
    switcher = {
            "/bye":logout,
            "/list":list_users,
            "/file":getClientFile,
            "/get":processFileRequest
    }
    
    # Assumindo tudo que não seja uma mensagem válida
    # na definição do protocolo como MSG:<usuário>:<texto>
    func = switcher.get(cmd, chat) 
    if args[0] == "/file" or args[0] == "/get":
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
            name = msg.replace("USER:","") 
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
