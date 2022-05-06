from PyQt5.QtWidgets import QListView, QListWidget, QMainWindow, QPushButton, QTableWidgetItem, QWidget, QApplication, QAction, QStackedWidget, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize

from Noire_UI import Noire_UI

from functools import partial
from PIL import Image, ImageQt
import sys, os
import numpy as np
from threading import Thread
import queue
import time
from socket_server import Server
from socket_client import Client
from threaddd import Threadd

class Player:
    def __init__(self, name, index, colour):
        self.name = name
        self.index = index
        self.colour = colour

    def start(self):
        # pass
        print(self.name, self.index, self.colour)

class Noire_Main(QMainWindow, Noire_UI):
    def __init__(self):
        super().__init__()
        self.setup_UI()

        self.image_cross = Image.open('assets/cross.png').convert("RGBA").resize((488,610))
        self.image_circle = Image.open('assets/circle.png').convert("RGBA").resize((488,610))

        # self.table_players_append([['a','b','c','d','e']])
        # print('appended')
    def table_players_append(self, data, client=False):
        #data = [['ID', 'Name','Colour', 'Ip', 'Port']]
        if client == False:
            for i in data:
                pos = self.table_players.rowCount()
                self.table_players.insertRow(pos)
                self.table_players.setItem(pos, 0, QTableWidgetItem(f'{data[0]}'))
                self.table_players.setItem(pos, 1, QTableWidgetItem(f'{data[1]}'))
                self.table_players.setItem(pos, 2, QTableWidgetItem(f'{data[2]}'))
                self.table_players.setItem(pos, 3, QTableWidgetItem(f'{data[3]}'))
                self.table_players.setItem(pos, 4, QTableWidgetItem(f'{data[4]}'))
        if client == True:
            data = data.split(';')
            for i in data:
                a = i.split('_')

                pos = self.table_players.rowCount()
                self.table_players.insertRow(pos)
                self.table_players.setItem(pos, 0, QTableWidgetItem(f'{a[0]}'))
                self.table_players.setItem(pos, 1, QTableWidgetItem(f'{a[1]}'))
                self.table_players.setItem(pos, 2, QTableWidgetItem(f'{a[2]}'))
                self.table_players.setItem(pos, 3, QTableWidgetItem(f'{a[3]}'))
                self.table_players.setItem(pos, 4, QTableWidgetItem(f'{a[4]}'))




    def host_game2(self):
        self.stack.setCurrentWidget(self.widget3)

        self.p_name = self.line_name.text()
        ip = self.line_ip.text()
        port = self.line_port.text()

        #self.table_players_append([[1, self.p_name, 'red', ip, port]])

        # self.thread = Threadd()
        # self.thread.signal.connect(self.on_data_ready)
        # self.thread.start()

        self.server = Server(ip, int(port))
        self.server.signal.connect(self.on_data_ready)
        self.server.start()

        self.client = Client(ip, int(port), self.p_name)
        self.client.signal.connect(self.on_data_ready_cl)
        self.client.start()


    def on_data_ready(self, data):
        print(data)

    def on_data_ready_cl(self, data):
        print(data, type(data))
        self.table_players_append(data, client=True)

    def connect_to2(self):
        self.stack.setCurrentWidget(self.widget3)

        # self.p_name = self.line_name.text()
        self.p_name = 'CLIENT'
        ip = self.line_ip.text()
        port = self.line_port.text()

        pos = self.table_players.rowCount()
        self.table_players.insertRow(pos)
        self.table_players.insertRow(pos+1)
        self.table_players.setItem(pos+1, 0, QTableWidgetItem(f'{self.p_name}'))
        self.table_players.setItem(pos+1, 1, QTableWidgetItem(f'{ip}:{port}'))
        

        self.client = Client(ip, int(port), self.p_name)
        self.client.signal.connect(self.on_data_ready_cl)
        self.client.start()


    def host_game(self):
        self.stack.setCurrentWidget(self.widget2)
        self.unhide_widgets()

        p_name = self.line_name.text()
        self.p1 = Player(p_name, 1, 'red')

        self.change_turn_label(self.p1.name)

        # Start server
        ip = self.line_ip.text()
        port = self.line_port.text()
        # self.server = Server(ip, int(port))
        # Thread(target=self.server.server, daemon=True).start()
        
        self.connect_to()

    def connect_to(self):
        self.stack.setCurrentWidget(self.widget2)
        self.unhide_widgets()

        # Client
        ip = self.line_ip.text()
        port = self.line_port.text()
        pname = self.line_name.text()
        self.client = Client(ip, int(port), pname)
        Thread(target=self.client.client, daemon=True).start()

        #Thread(target=self.wait_for_response, daemon=True).start()


    def change_turn_label(self, msg):
        
        self.label1.setText(f'<b><font color="black">Ход игрока</font><font color="red"> {msg}</font>')



    def clc(self, btn):
        
        #btn.setIcon(QIcon('assets/error_card.png'))
        # Как идея: в каждой ячейке матрицы свой lo а на 
        # ней карта
        # Порядковый номер карты в матрице
        p1 = self.grid.indexOf(btn)

        # Сам виджет кнопки по порядковому номеру
        p3 = self.grid.itemAt(p1).widget()

        # Позиция карты в матрице (x,y,1,1)
        p2 = self.grid.getItemPosition(p1)[:2]

        # Сам виджет кнопки по позиции в матрице (x,y,1,1)
        p4 = self.grid.itemAtPosition(*p2).widget()

        print(p1, p2, p4)
        if p4.objectName() == 'Alive':
            self.kill_card(p4)
        else:
            self.check_card(p4)




    def kill_card(self, p4):
        img = self.change_icon(self.cards_dict[p4], 'kill')
        pix = QPixmap.fromImage(ImageQt.ImageQt(img))
        icon = QIcon(pix)
        p4.setIcon(QIcon(icon))
        p4.setObjectName('Killed')
        print('killed!')

    def check_card(self, p4):
        img = self.change_icon(self.cards_dict[p4], 'check')
        pix = QPixmap.fromImage(ImageQt.ImageQt(img))
        icon = QIcon(pix)
        p4.setIcon(QIcon(icon))
        p4.setObjectName('Checked')
        print('checked!')
    
    def change_icon(self, picture_path, action):
        if action == 'kill':
            frontImage = self.image_cross
        elif action == 'check':
            frontImage = self.image_circle
        
        background = Image.open(picture_path)
        background = background.convert("LA").convert('RGBA')
        
        width = (background.width - frontImage.width) // 2
        height = (background.height - frontImage.height) // 2
        
        background.paste(frontImage, (width, height), frontImage)
        return background

    def moveup(self, num):
        a = np.arange(0)
        for i in range(5):
            p4 = self.grid.itemAtPosition(i,num).widget()
            a = np.append(a, p4)
            self.grid.removeWidget(p4)
        a = np.roll(a, -1)


        for i in range(len(a)):
            self.grid.addWidget(a[i], i,num)


        
        self.client.send_turn('moveup', num)

    def movedown(self, num):
        a = np.arange(0)
        for i in range(5):
            p4 = self.grid.itemAtPosition(i,num).widget()
            a = np.append(a, p4)
            self.grid.removeWidget(p4)
        a = np.roll(a, 1)


        for i in range(len(a)):
            self.grid.addWidget(a[i], i,num)

    def moveleft(self, num):
        a = np.arange(0)
        for i in range(5):
            p4 = self.grid.itemAtPosition(num,i).widget()
            a = np.append(a, p4)
            self.grid.removeWidget(p4)
        a = np.roll(a, -1)


        for i in range(len(a)):
            self.grid.addWidget(a[i], num,i)

    def moveright(self, num):
        a = np.arange(0)
        for i in range(5):
            p4 = self.grid.itemAtPosition(num,i).widget()
            a = np.append(a, p4)
            self.grid.removeWidget(p4)
        a = np.roll(a, 1)


        for i in range(len(a)):
            self.grid.addWidget(a[i], num,i)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Noire_Main()
    window.show()
    sys.exit(app.exec_())
