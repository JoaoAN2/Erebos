# EXECUTAR COM PYCHARM PARA VER OS NOMES COLORIDOS
import socket
import threading
from time import sleep
from random import randint
from cryptography.fernet import Fernet
# CMD Command: pip install cryptography
# Linux Terminal/MACOS: pip3 install cryptography


def crypto_tolls():
    key = b'n05rzNJNF-tU4H-oCneuEdDxR4_fCL_wAgsy9CmB7Jk='
    fernet = Fernet(key)
    return fernet


def getIP():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)  # IPv4
    return ip_address


def format(msg):
    return name + msg


def reciveMsg():
    global kill_bool
    while True:
        msgBytes, serverIP = client.recvfrom(BUFFSIZE)
        decryptedmsg = crypto.decrypt(msgBytes).decode(character)
        print(decryptedmsg)
        if kill_bool:
            break


def clientSide(address):
    global cont, kill_var, kill_bool, name
    while True:
        if cont == 0:
            name = input("Name: ")
            name = f'\033[1;3{randint(1, 6)}m{name}: \033[m'
            msg = f'\033[1;36m>>ENTROU \033[m'
            token = '0'
        else:
            sleep(0.0001) # Sincronizar
            msg = input()
            token = '1'
            if msg == kill_var:
                msg = f'\033[1;31m>>USUÁRIO SE DESCONECTOU \033[m'
                kill_bool = True
                token = '2'
        decryptedmsg = format(msg)
        encryptedmsg = crypto.encrypt(decryptedmsg.encode(character)).decode(character) # Mensagem criptografada
        msgsend = encryptedmsg + token
        client.sendto(msgsend.encode(character), address)
        cont += 1
        if kill_bool:
            break


name = ''
cont = 0
kill_var = '/exit'  # Encerramento
kill_bool = False
BUFFSIZE = 16384  # = 2^14
HOST = getIP() # IPv4
PORT = 12000  # Porta desejada
ADDR = (HOST, PORT) # Tupla IP/Porta
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
character = "utf-8"

crypto = crypto_tolls()  # Ferramentas de criptografia

ClientSideThread = threading.Thread(target=clientSide, args=(ADDR,))
ClientReciveThread = threading.Thread(target=reciveMsg)
ClientSideThread.start()
while True:
    if cont != 0:
        ClientReciveThread.start()
        break
ClientSideThread.join()
