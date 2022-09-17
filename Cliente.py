from socket import*
import time
from _thread import*

class Cliente:
    def ini(self):
        host=input("Disreccion del servidor: ")
        port=int(input("Port: "))
        return host,port

    def crearSocket(self):
        s=socket(AF_INET, SOCK_STREAM)
        return s
    def conectarse ( self, host, port, s):
        s.connect((host,port))

    def intentoConexion(self,host, port, s):
        while True:
            print("\nIntentando conectar a :",host+":"+str(port))
            try:
                self.conectarse(host,port,s)
                break
            except:
                print("No hay ningun server en el:",host+":"+str(port))
                print("Intentando de nuevo en 5 seg\n")
                time.sleep(5)

    def enviar(self,s):
        while True:
            global exit
            try:
                msg =input("")
                msg=client +":"+msg
                if msg==client+":salir":
                    exit =True
                    msg="El"+client+"Cliente se ha ido"
                    s.send(msg.encode("UTF-8"))
                    s.close
                    break
                else:
                    s.send(msg.encode("UTF-8"))
                    start_new_thread(self.recibir,(s,))
            except:
                print("Algo sucedio\n")
                print("Intentando en 5 seg")
                time.sleep(5)

    def recibir(self,s):
        while True:
            try:
                reply=s.recv(2048)
                print(reply.decode("UTF-8"))
                break
            except:
                print("No se puede recibir respuestas\n")
                print("intentando en 5 segundos")
                time.sleep(5)

    def recibirEspecial(self, s):
        global client
        client=s.recv(2048).decode("UTF-8")

    exit=False  # si el cliente envia salir, exit se pone en true y el
                # el programa termina
    client=""

    def main(self):
        host,port=self.ini()
        s=self.crearSocket()
        self.intentoConexion(host,port,s)
        self.recibirEspecial(s)
        print("\Conexion con el servidor establecido!\nEl servidor es:",host+":"+str(port)+"\n")
        print("Escribe tu mensaje\n")
        start_new_thread(self.enviar,(s,))

        while exit!=True:  #Necesarios para que los hilos no mueran
            pass

        print("\nLo siento algo salio mal ! Ha perdido conexion con el servidor:(")
        print("Cerrando la ventana en 5 seg")
        time.sleep(10)


objCliente=Cliente()
objCliente.main()

















