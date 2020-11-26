import socket
import threading

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
    
    # Lê o arquivo
    with open(arquivo, "rb") as file:
        while(f := file.read(1024)):
            tcp.send(f)
    
    tcp.close()

# Getting user
msg = input("Nome de usuário: ")
msg = "USER:" + msg

# Socket TCP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.sendto(msg.encode(), destination)
print("\nConexão estabelecida. Para sair digite /bye\n")

# Dispara thread para escutar o servidor
t = threading.Thread(target=listen, args=[udp], daemon = True)
t.start()

while msg!="/bye":

    msg = input()
    
    # Conferindo se o cliente quer enviar um arquivo
    args = msg.split()
    if args[0] == "/file":
        udp.sendto(msg.encode(), destination)
        sendFile(args[1])
    elif args[0] == "/get":
        print("oi")
    else:
        udp.sendto(msg.encode(), destination)

udp.close()
