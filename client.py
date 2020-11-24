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

# Getting user
msg = input("Nome de usuário: ")

# Socket TCP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.sendto(("USER:"+msg).encode(), destination)

print("\nConexão estabelecida. Para sair digite /bye\n")
# Dispara thread para escutar o servidor
t = threading.Thread(target=listen, args=[udp])
t.start()

while msg !="/bye":

    msg = input()
    udp.sendto(msg.encode(), destination)

    

udp.close()

