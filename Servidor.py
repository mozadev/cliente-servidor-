from socket import *
from _thread import *
import time
import sys
class Servidor:
    def ini(self):
        host=input("Host: ")
        port=int(input("Port: "))
        return host,port

    def crearSocket(self):
        s=socket(AF_INET,SOCK_STREAM)
        return s

    def ligarSocket(self,s,host,port):
        while True:
            try:
                s.bind((host,port))
                break

            except error as e:
                print("ERROR:",e)

    def conexiones(self,s):
        conn, addr=s.accept()
        print("\nConexiones establecida.\nEl cliente es: ",addr[0]+":"+str(addr[1])+"\n")
        return conn,addr

    def enviar(self,conn):
        msg=input("")
        msg="Servidor: "+msg
        try:
            conn.send(msg.encode("UTF-8"))
        except:
            print("\nAlgo sucedio")
            print("Intentando en 5 seg\n")
            time.sleep(5)

    def enviar2(self,conn):
        msg=input("")
        msg="Servidor: "+msg
        try:
            conn.send(msg.encode("UTF-8"))
        except:
            print("\Algo sucedio")
            print("Intentando en 5 seg\n")
            time.sleep(5)

    def recibir(self,conn):
        while True:
            global bandera
            try:
                reply=conn.recv(2048)
                reply=reply.decode("UTF-8")

                if reply[0]=="1":
                    print("Cliente",reply)
                    start_new_thread(self.enviar,(conn,))
                elif reply[0]=="2":
                    print("Cliente",reply)
                    start_new_thread(self.enviar2,(conn,))

                else:
                    lista_de_clientes.append(reply[4])
                    print("\nEl cliente "+reply[4]+"se ha ido")
                    bandera=True
                    break
            except:
                print("\nNo se puede recibir respuesta")
                print("Intentando en 5 seg\n")
                time.sleep(5)

    def enviarEspecial(self, conn):
        global lista_de_clientes,client
        client=self.lista_de_clientes.pop()
        conn.send(client.encode("UTF-8"))


    bandera=False #Utilizada en la desconexion/conexion de clientes
    lista_de_clientes=["2","1"]# el servidor le asigna un numero a clientes seguna esta lista
    client=""# Numero de cliente

    def main(self):
        global bandera
        host, port =self.ini()
        s=self.crearSocket()
        self.ligarSocket(s,host,port)
        s.listen(2)# espera 2 clientes

        print("\ADVERTENCIA: El servidor es un esclavo. No"
              "escribir si el servidor no tiene ningun mensaje de respuesta")
        print("\nA la espera de clientes")
        conn, addr = self.conexiones(s)
        self.enviarEspecial(conn)# espero conexion del cliente 1
        start_new_thread(self.recibir,(conn,))

        conn2, addr2 = self.conexiones(s)
        self.enviarEspecial(conn2)# espero conexion del cliente 1
        start_new_thread(self.recibir, (conn2,))

        while True: # Necesario para q los hilos no mueran
            if bandera !=True: #En caso de desconectarse un cliente, espera a que otro vuelve a conectarse

                conn3, addr3 = self.conexiones(s)
                self.enviarEspecial(conn3)  # espero conexion del cliente 1
                start_new_thread(self.recibir, (conn3,))
                bandera=False
objServidor=Servidor()
objServidor.main()

