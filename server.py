import rsa
import socket
import threading
from random import randint
from datetime import datetime

class Server:
    def __init__(self, ip, port):
        self.date = datetime.now().strftime("%d/%m/%Y")
        
        #rsa
        self.n, self.e, self.d = rsa.keygen(124)

        # TCP connection setup
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.clients = {} 

        while True:
            #listen for incoming connection (up to 5)
            self.sock.listen(5)
            conn, addr = self.sock.accept()
            threading.Thread(target=self.handle_client, args=[conn]).start()

    def handle_client(self, conn):
        "When used as a target in thread, this method will deal with connection instances individually"
        
        name = self.setup(conn)
        
        # Main loop
        while True:
            try:
                if self.date != datetime.now().strftime("%d/%m/%Y"):
                    self.date = datetime.now().strftime("%d/%m/%Y")
                    self.broadcast(f'\n{self.date}\n')

                message = self.decrypt(conn.recv(1024).decode('utf-8'))

                if message == 'quit':
                    # for some reason it only works properly if i close() before broadcast()
                    self.clients.pop(name)
                    conn.close()
                    self.broadcast(f'{name} has left the chat')
                    print(f'{name} disconnected')
                    return
        
                self.broadcast(f'({datetime.now().strftime("%H:%M")}) {name}: {message}')
                
            except OSError:
                print('OSError')
                break

    def setup(self, conn):
        # receive clients public key
        n = int(conn.recv(1024).decode('utf-8'))
        e = int(conn.recv(1024).decode('utf-8'))
        
        # send server public key then receive and decrypt name
        conn.send(bytes(str(self.n), 'utf-8'))
        conn.send(bytes(str(self.e), 'utf-8'))
        name = self.decrypt(conn.recv(1024).decode('utf-8'))

        # checking for duplicates
        if name in self.clients.keys():
            name = f"{name}{randint(0, 1000)}"    
        self.clients[f"{name}"] = (conn, n, e)
        
        #print(f'n:{n}, e:{e}')
        
        # finished setup and welcome message
        self.broadcast(f'{name} has joined the chat!')
        conn.send(bytes(self.encrypt(f'{self.date}\nWelcome to the chat room!', n, e), 'utf-8'))
        print(f'{name} connected')  
        return name      
        
    def broadcast(self, message:str):
        for key in self.clients:
            comm, n, e = self.clients[key]
            comm.send(bytes(self.encrypt(message, n, e), 'utf-8'))
            
    def encrypt(self, message:str, n:int, e:int):
        strr = ''
        width = rsa.bitLength(n)        
        for c in message:
            strr += rsa.dec2bin(rsa.encrypt(ord(c), n, e), width)
        return(strr)
    
    def decrypt(self, message:str):
        width = rsa.bitLength(self.n)
        strr = ''
        for i in range(0, len(message) - 1, width):
            # Sub-stringing the string
            s = message[i: i + width]
            y = rsa.bin2dec(s)
            y = rsa.decrypt(y, self.n, self.d)
            strr += chr(y)
        return strr


if __name__ == '__main__':
    s = Server(ip="localhost", port=9999)