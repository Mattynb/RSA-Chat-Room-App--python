import rsa
import socket
import threading
from time import time, sleep
import PySimpleGUI as sg

class Client:
    def __init__(self, ip, port, name):
        self.msg = ''
        self.name = name
    
        # rsa setup
        self.n, self.e, self.d = rsa.keygen(2048)
        
        # connect to server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

        self.setup()
        
        # Start thread to receive messages asyncronously I believe        
        threading.Thread(target=self.receive).start()
        
        # Create GUI
        sg.theme('DarkAmber')
        self.layout = [
            [sg.Multiline(size=(50, 20), key='-MSG-', disabled=True, autoscroll=True)],
            [sg.Input(key='-IN-', size=(50, 1)), sg.Button('Send')]
        ]
        self.window = sg.Window('Chat App - ' + name, self.layout)

        # Main loop
        while True:
            event, values = self.window.read(timeout=0)
            
            if event == sg.WIN_CLOSED:
                # closes the connection
                self.sock.send(bytes(self.encrypt('quit'), 'utf-8'))
                break
                        
            if self.msg != '':
                # updates window when self.receive() modifies self.msg
                self.window['-MSG-'].print(self.msg)
                self.msg = ''

            if event == 'Send':
                message = values['-IN-']

                if message != '':    
                    self.window['-IN-'].update('')
                    self.sock.send(bytes(self.encrypt(message), 'utf-8'))
        
        self.sock.close()
        self.window.close()

    def setup(self):
        # send setup info to server
        # send clients public key n,e as string
        self.sock.send(bytes(str(self.n), 'utf-8')); sleep(.2)
        self.sock.send(bytes(str(self.e), 'utf-8'))
        
        # receive servers public key n_server, es. Then send encrypted name
        self.n_server = int(self.sock.recv(1024).decode('utf-8')); sleep(.2);
        self.e_server = int(self.sock.recv(1024).decode('utf-8'))
        self.sock.send(bytes(str(self.encrypt(f'{self.name}')), 'utf-8'))
        #print(f'ns:{self.n_server}, es:{self.e_server}')
    
    def receive(self):
        while True:
            try:
                self.msg = self.decrypt(self.sock.recv(1024).decode('utf-8'))
                #print(self.msg)
                
            except OSError:
                break
            
    def encrypt(self, message):
        strr = ''
        width = rsa.bitLength(self.n_server)        
        for c in message:
            strr += rsa.dec2bin(rsa.encrypt(ord(c), self.n_server, self.e_server), width)
        return(strr)
    
    def decrypt(self, message):
        width = rsa.bitLength(self.n)
        strr = ''
        for i in range(0, len(message) - 1, width):
            # Sub-stringing the string
            s = message[i: i + width]
            y = rsa.bin2dec(s)
            y = rsa.decrypt(y, self.n, self.d)
            strr += chr(y)
        return strr
