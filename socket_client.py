import socket
from threading import Thread

from PyQt5.QtCore import QThread, Qt, pyqtSignal


class Client(QThread):

    signal = pyqtSignal(object)

    def __init__(self, ip, port, pname):
        QThread.__init__(self)
        self.ip = ip
        self.port = port
        self.pname = pname

        self.response = None


    def run(self) -> None:


        try:

            self.socket_instance = socket.socket()
            self.socket_instance.connect((self.ip, self.port))
            # Обработка сообщений в отдельный поток

            self.thr = Handle_Messages_thread(self.socket_instance)
            self.thr.signal.connect(self.emitt)
            self.thr.start()
            # Thread(target=self.handle_messages, args=[self.socket_instance]).start()

            print('Connected to chat!')

            self.database_append()

            # Читать ввод пользователя до тех пор пока он не отключится
            while True:
                msg = input()

                if msg == 'quit':
                    break

                # Перевести в utf-8
                self.socket_instance.send(msg.encode())

            # Закрыть соединение
            self.socket_instance.close()

        except Exception as e:
            print(f'Error connecting to server socket {e}')
            self.socket_instance.close()
        
    def database_append(self):
        cmd = f'#APPEND::{self.pname},{self.ip},{self.port}'
        self.socket_instance.send(cmd.encode())

    def send_turn(self, turn, num=None):
        cmd = f'#TURN::{self.pname},{turn},{num}'
        self.socket_instance.send(cmd.encode())
        
    def emitt(self, a):
        self.signal.emit(a)


class Handle_Messages_thread(QThread):

    signal = pyqtSignal(object)

    def __init__(self, connection: socket.socket):
        QThread.__init__(self)

        self.connection = connection

    
    def run(self):
        '''
            Receive messages sent by the server and display them to user
        '''
        while True:
            try:
                msg = self.connection.recv(1024)

                if msg:
                    print(msg.decode())
                else:
                    self.connection.close()
                    break

                cmd = msg.decode()
                # print('CMD received:', cmd)
                # self.signal.emit(cmd)
                # print('emitting CMD:', cmd)
                if cmd.startswith('#CAST_TURN'):
                    print('cast response received')
                elif cmd.startswith('#CAST_APPEND'):
                    a = cmd.split('::')[1]
                    self.signal.emit(a)


                    # self.app.apptest(a)
                    #self.app.table_players_append(a, client=True)


            except Exception as e:
                print(f'Error handling message from server: {e}')
                self.connection.close()
                break
