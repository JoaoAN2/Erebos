import socket
import threading


def removeTokenandSendMessage(encryptedmsg):
    msg = encryptedmsg[0:-1]
    for i in range(0, len(ipA)):
        server.sendto(msg.encode('utf8'), (ipA[i], ipB[i]))


def serverSide():
    global ipA, ipB
    while True:
        while True:
            try:
                msgBytes, clientIP = server.recvfrom(BUFFSIZE)
                break
            except:
                pass
        msgAnswer = msgBytes.decode('utf8')
        token = msgAnswer[-1]
        if token == '0':
            ipA.append(clientIP[0])
            ipB.append(clientIP[1])
            removeTokenandSendMessage(msgAnswer)

        else:
            removeTokenandSendMessage(msgAnswer)
            if token == '2':
                for i in range(0, len(ipA)):
                    if ipA[i] == clientIP[0] and ipB[i] == clientIP[1]:
                        del ipA[i]
                        del ipB[i]
                        print('Usuário removido com sucesso')
                        break
        print(msgAnswer)

ipA = []
ipB = []
BUFFSIZE = 16384
HOST = ''
PORT = 12000
ADDR = (HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(ADDR)
print('Aguardando conexões...')
ServerSideThread = threading.Thread(target=serverSide())
ServerSideThread.start()
ServerSideThread.join()
