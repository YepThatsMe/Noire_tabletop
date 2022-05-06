import socket
from time import sleep
from PyQt5.QtCore import QThread, pyqtSignal
import pandas as pd

class Server(QThread):

    signal = pyqtSignal(object)

    def __init__(self, ip, port):
        QThread.__init__(self)
        self.ip = ip
        self.port = port
        self.connections = []

    def run(self) -> None:
        

        try:
            self.socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_instance.bind((self.ip, self.port))
            self.socket_instance.listen(6)

            print('Server started!')
            
            while True:

                # Принять соединение клиента
                conn, address = self.socket_instance.accept()
                self.connections.append(conn)
                # Запуск потока для обработки сообщений

                thr = Handle_User_Connection_Thread(conn, address, self.connections)
                thr.signal.connect(self.emitt)
                thr.start()
                # Thread(target=self.handle_user_connection, args=[conn, address]).start()

        except Exception as e:
            print(f'An error has occurred when instancing socket: {e}')
        finally:
            
            if len(self.connections) > 0:
                for conn in self.connections:
                    self.remove_connection(conn)

            self.socket_instance.close()

    def emitt(self, a):
        self.signal.emit(a)

class Handle_User_Connection_Thread(QThread):

    signal = pyqtSignal(object)

    def __init__(self, connection: socket.socket, address: str, connections) -> None:
        QThread.__init__(self)
        print('INITIATING HANDE USER CONNECTION THREAD')
        self.connection = connection
        self.address = address
        self.connections = connections
        self.PLAYERS = Players()

    
    def run(self):
        '''
            Get user connection in order to keep receiving their messages and
            sent to others users/connections.
        '''
        while True:
            try:
                # Get client message
                msg = self.connection.recv(1024)





                if msg:
                    # Лог сообщений
                    print(f'{self.address[0]}:{self.address[1]} - {msg.decode()}')
                    msg_to_send = f'From {self.address[0]}:{self.address[1]} - {msg.decode()}'
                else:
                    self.remove_connection(self.connection)
                    break


                cmd = msg.decode()
                # print('emitting cmd..')
                # self.signal.emit(cmd)
                if cmd.startswith('#APPEND'):
                    a = cmd.split('::')[1].split(',')
                    self.PLAYERS.new_player(a[0], a[1], a[2])


                    self.broadcast(f'#CAST_APPEND::{self.PLAYERS.data}', self.connection)
                    continue
                elif cmd.startswith('#TURN'):
                    a = cmd.split('::')[1].split(',')
                    self.PLAYERS.new_turn(a[0], a[1]+str(a[2]))

                    self.broadcast(f'#CAST_TURN::{a[0]},{a[1]},{a[2]}', self.connection)
                    continue
                else:

                    self.broadcast(msg_to_send, self.connection)


            except Exception as e:
                print(f'Error to handle user connection: {e}')
                self.remove_connection(self.connection)
                break

    def broadcast(self, message: str, connection: socket.socket) -> None:
        '''
            Broadcast message to all users connected to the server
        '''

        for client_conn in self.connections:
            #print(client_conn, connection)
            # if client_conn != connection:
            try:

                client_conn.send(message.encode())


            except Exception as e:
                print('Error broadcasting message: {e}')
                self.remove_connection(client_conn)


    def remove_connection(self, conn: socket.socket) -> None:
        '''
            Remove specified connection from connections list
        '''


        if conn in self.connections:
            # 
            conn.close()
            self.connections.remove(conn)


class Players:
    def __init__(self) -> None:

        self.db = pd.DataFrame(columns=['ID', 'Name', 'Colour', 'Ip', 'Port'])
        self.colours = ['red', 'blue', 'cyan', 'purple']
        self.ids = [1,2,3,4]

        self.db_turns = pd.DataFrame(columns=['Name', 'Turn'])

    def new_player(self, pname, ip, port):

        colour = self.colours.pop(0)
        ids = self.ids.pop(0)

        # Пополнить серверную базу
        self.db.loc[len(self.db)] = [ids, pname, colour, ip, port]

        # Отправить данные в виджет "лобби"
        self.data = []
        for i in range(len(self.db)):
            self.data.append(list(self.db.iloc[i].values))
        self.data = ';'.join(['_'.join([str(elem) for elem in sublist]) for sublist in self.data])
        print(self.db)
    
    def new_turn(self, pname, turn):

        self.db_turns.loc[len(self.db_turns)] = [pname, turn]
        print(self.db_turns)

