import socket
import threading
import os

# Server IP
HOST = "127.0.0.1"
PORT = 20000
destination = (HOST, PORT)

# Escuta respostas do servidor de forma assíncrona
def listen(udp):
   
    while True:
        msg, addr = udp.recvfrom(1024)
        print(msg.decode())

# Função que envia dados para o servidor
def sendFile(arquivo):
    
    # Primeiro criamos uma nova conexão TCP
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect(destination)
    
    # Envia o arquivo em pedaços de 1024 bytes
    with open(arquivo, "rb") as file:
        while(f := file.read(1024)):
            tcp.send(f)
    tcp.close()

def getFile(user, arquivo):

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect(destination)
    
    # Lê o arquivo recebido pela transmissão
    name = user + "_" + arquivo
    with open(name, "wb") as file:
        while(data := tcp.recv(1024)):
            file.write(data)
    
    tcp.close()
    
    # Caso o arquivo não exista no servidor, remover o
    # arquivo temporário criado.
    sanity_check = open(name, "rb")
    if len(sanity_check.readlines()) < 1:
        sanity_check.close()
        os.remove(name)

# Handle do usuário 
user = input("Nome de usuário: ")
msg = "USER:" + user 

# Socket TCP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.sendto(msg.encode(), destination)
print("\nConexão estabelecida. Para sair digite /bye\n")

# Dispara daemon para escutar o servidor
t = threading.Thread(target=listen, args=[udp], daemon = True)
t.start()

while msg!="/bye":
    
    msg = input()

    # Conferindo se o cliente quer enviar um arquivo
    udp.sendto(msg.encode(), destination)
    args = msg.split()
    
    if args[0] == "/file":
        sendFile(args[1])
    elif args[0] == "/get":
        getFile(user, args[1])

udp.close()
