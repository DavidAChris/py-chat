import socket
import threading


class Client:
    def __init__(self):
        self.__nickname = input("Choose your nickname: ")
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect(('127.0.0.1', 55554))

    def __receive(self):
        while True:
            try:
                message = self.__client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.__client.send(self.__nickname.encode('ascii'))
                else:
                    print(message)
            except:
                print("An error occurred!")
                self.__client.close()
                break

    def __write(self):
        while True:
            message = '{}: {}'.format(self.__nickname, input(''))
            self.__client.send(message.encode('ascii'))

    def run_client(self):
        receive_thread = threading.Thread(target=self.__receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.__write)
        write_thread.start()
