import socket

cliente = socket.socket()
host = socket.gethostname()
ip = socket.gethostbyname(host)
puerto = 12345
cliente.connect((ip, puerto))

while True:
    mensaje = cliente.recv(1024).decode()
    print(mensaje)

    if "cerró la conexion" in mensaje.lower():
        break

    entrada = input("> ")
    cliente.send(entrada.encode())

cliente.close()
