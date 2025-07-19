import socket
import threading
import requests

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
ip = socket.gethostbyname(host)
puerto = 12345
servidor.bind((ip, puerto))
servidor.listen(5)
print("Servidor iniciado en:", ip, "puerto", puerto)

def atender(cliente, direccion):
    print("Se conectó:", direccion)
    cliente.send("Decime tu nombre de usuario: ".encode())
    nombre = cliente.recv(1024).decode().strip()

    while True:
        cliente.send("Escribí un comando (/repost o /adios): ".encode())
        entrada = cliente.recv(1024).decode().strip()

        if entrada == "/repost":
            try:
                r = requests.get("https://web.dragonball-api.com/api/characters")
                if r.status_code == 200:
                    data = r.json()
                    persos = data["items"][:5]
                    respuesta = f"Hola {nombre}, te paso algunos personajes:\n"
                    for p in persos:
                        raza = p.get("race", "desconocida")
                        origen = p.get("originPlanet", "desconocido")
                        respuesta += f"- {p['name']} ({raza}) | Origen: {origen}\n"
                else:
                    respuesta = "No se pudo traer info de la API"
            except:
                respuesta = "Ocurrió un error con la API"
            cliente.send(respuesta.encode())

        elif entrada == "/adios":
            cliente.send("Chau, se cerró la conexión.".encode())
            print(nombre, "se desconectó.")
            break
        else:
            cliente.send("No entendí ese comando.".encode())

    cliente.close()

while True:
    cli, dir = servidor.accept()
    hilo = threading.Thread(target=atender, args=(cli, dir))
    hilo.start()
