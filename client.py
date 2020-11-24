import socket

# Server IP
HOST = "127.0.0.1"
PORT = 20000
destination = (HOST, PORT)

# Getting user
usr = input("Nome de usuário: ")

# Socket TCP
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect(destination)
tcp.send(("USER:"+usr).encode())

print(  "\nConexão estabelecida. Para sair digite /bye\n")
while True:
    
    msg = input()
    tcp.send(msg.encode())
    
    if msg=="/bye":
        break

tcp.close()

