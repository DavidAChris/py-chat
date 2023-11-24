import socket
import threading


class Server:
    def __init__(self):
        self.__host = '127.0.0.1'
        self.__port = 55554
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((self.__host, self.__port))
        self.__server.listen()
        self.__clients = []
        self.__nicknames = []

    def __broadcast(self, message):
        for client in self.__clients:
            client.send(message)

    def __handle(self, client):
        while True:
            try:
                # Broadcasting Messages
                message = client.recv(1024)
                self.__broadcast(message)
            except:
                # Removing And Closing Clients
                index = self.__clients.index(client)
                self.__clients.remove(client)
                client.close()
                nickname = self.__nicknames[index]
                self.__broadcast('{} left!'.format(nickname).encode('ascii'))
                self.__nicknames.remove(nickname)
                break

    def __receive(self):
        while True:
            # Accept Connection
            client, address = self.__server.accept()
            print("Connected with {}".format(str(address)))

            # Request And Store Nickname
            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            self.__nicknames.append(nickname)
            self.__clients.append(client)

            # Print And Broadcast Nickname
            print("Nickname is {}".format(nickname))
            self.__broadcast("{} joined!".format(nickname).encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))

            # Start Handling Thread For Client
            thread = threading.Thread(target=self.__handle, args=(client,))
            thread.start()

    def run_server(self):
        self.__receive()
