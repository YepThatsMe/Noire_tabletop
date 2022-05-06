from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QSizePolicy, QSpacerItem, QTableWidget, QVBoxLayout, QWidget, QStackedWidget

import os, sys
from functools import partial

from glob import glob
import numpy as np
from numpy.core.numeric import _correlate_dispatcher

class Noire_UI(QWidget):

    def setup_UI(self):
        
        ### SETTINGS ###
        self.setWindowTitle("Noire")
        self.setWindowIcon(QIcon('assets/icon.jpg'))
        # self.move(600,100)
        # self.setFixedSize(1080,720)

        ### WIDGETS ###
        self.stack = QStackedWidget(self)

        
        self.host_btn = QPushButton('Host game')
        self.host_btn.clicked.connect(self.host_game2)

        self.connect_btn = QPushButton('Connect to')
        self.connect_btn.clicked.connect(self.connect_to2)

        self.line_name = QLineEdit('Arthas')
        self.line_name.setPlaceholderText('Артес')

        self.line_ip = QLineEdit('25.51.201.118')
        self.line_ip.setPlaceholderText('128.0.0.1')
        
        self.line_port = QLineEdit('2620')
        self.line_port.setPlaceholderText('8080')

        self.table_players = QTableWidget()
        self.table_players.setColumnCount(5)

        self.start_game_btn = QPushButton('Start game')
        self.start_game_btn.setEnabled(False)

        self.label2 = QLabel()
        self.label2.setFont(QFont('Elephant', 14))
        self.label2.setText('Ожидание подключения...')

        self.label1 = QLabel()
        self.label1.setFont(QFont('Elephant', 18))
        #self.label1.setStyleSheet("font-weight: bold; color: red")


        # Cards
        card_count = 25
        self.cards = [i for i in range(card_count)]
        self.icons = [i for i in range(card_count)]

        self.paths = glob('assets\\cards\\*.png', recursive=True)
        
        for i in range(card_count):
            # try:
            self.icons[i] = QIcon(self.paths[i])
            # except IndexError:
            #     self.icons[i] = QIcon(self.paths[card_count - i])
        
        self.cards_dict = {}
        self.height = 150
        for i in range(card_count):
            self.cards[i] = QPushButton()
            self.cards[i].setIcon(QIcon(self.icons[i]))
            self.cards[i].setFixedSize(QSize(0.6*self.height, self.height))
            self.cards[i].setIconSize(QSize(0.6*self.height, self.height))
            self.cards[i].setObjectName('Alive')
            self.cards[i].setFlat(1)
            self.cards[i].clicked.connect(partial(self.clc, self.cards[i]))
            self.cards_dict[self.cards[i]] = self.paths[i]

        # Buttons
        self.btn_up1 = QPushButton()
        self.btn_up1.setFixedHeight(30)
        self.btn_up1.clicked.connect(partial(self.moveup, 0))

        self.btn_up2 = QPushButton()
        self.btn_up2.setFixedHeight(30)
        self.btn_up2.clicked.connect(partial(self.moveup, 1))

        self.btn_up3 = QPushButton()
        self.btn_up3.setFixedHeight(30)
        self.btn_up3.clicked.connect(partial(self.moveup, 2))

        self.btn_up4 = QPushButton()
        self.btn_up4.setFixedHeight(30)
        self.btn_up4.clicked.connect(partial(self.moveup, 3))

        self.btn_up5 = QPushButton()
        self.btn_up5.setFixedHeight(30)
        self.btn_up5.clicked.connect(partial(self.moveup, 4))

        self.btn_down1 = QPushButton()
        self.btn_down1.setFixedHeight(30)
        self.btn_down1.clicked.connect(partial(self.movedown, 0))

        self.btn_down2 = QPushButton()
        self.btn_down2.setFixedHeight(30)
        self.btn_down2.clicked.connect(partial(self.movedown, 1))

        self.btn_down3 = QPushButton()
        self.btn_down3.setFixedHeight(30)
        self.btn_down3.clicked.connect(partial(self.movedown, 2))

        self.btn_down4 = QPushButton()
        self.btn_down4.setFixedHeight(30)
        self.btn_down4.clicked.connect(partial(self.movedown, 3))

        self.btn_down5 = QPushButton()
        self.btn_down5.setFixedHeight(30)
        self.btn_down5.clicked.connect(partial(self.movedown, 4))

        self.btn_left1 = QPushButton()
        self.btn_left1.setFixedSize(30, self.height)
        self.btn_left1.clicked.connect(partial(self.moveleft, 0))

        self.btn_left2 = QPushButton()
        self.btn_left2.setFixedSize(30, self.height)
        self.btn_left2.clicked.connect(partial(self.moveleft, 1))

        self.btn_left3 = QPushButton()
        self.btn_left3.setFixedSize(30, self.height)
        self.btn_left3.clicked.connect(partial(self.moveleft, 2))

        self.btn_left4 = QPushButton()
        self.btn_left4.setFixedSize(30, self.height)
        self.btn_left4.clicked.connect(partial(self.moveleft, 3))

        self.btn_left5 = QPushButton()
        self.btn_left5.setFixedSize(30, self.height)
        self.btn_left5.clicked.connect(partial(self.moveleft, 4))

        self.btn_right1 = QPushButton()
        self.btn_right1.setFixedSize(30, self.height)
        self.btn_right1.clicked.connect(partial(self.moveright, 0))

        self.btn_right2 = QPushButton()
        self.btn_right2.setFixedSize(30, self.height)
        self.btn_right2.clicked.connect(partial(self.moveright, 1))

        self.btn_right3 = QPushButton()
        self.btn_right3.setFixedSize(30, self.height)
        self.btn_right3.clicked.connect(partial(self.moveright, 2))

        self.btn_right4 = QPushButton()
        self.btn_right4.setFixedSize(30, self.height)
        self.btn_right4.clicked.connect(partial(self.moveright, 3))

        self.btn_right5 = QPushButton()
        self.btn_right5.setFixedSize(30, self.height)
        self.btn_right5.clicked.connect(partial(self.moveright, 4))



        ########### GRID SETUP ###########
        self.grid = QGridLayout()

        positions = [(i,j) for i in range(5) for j in range(5)]

        for i in range(len(positions)):
            self.grid.addWidget(self.cards[i], *positions[i])
        #self.grid.setColumnStretch(5,1)

        ### LAYOUT SETUP ###
        
        self.lo1 = QHBoxLayout()
        self.lo1.addWidget(self.line_name)

        self.lo2 = QHBoxLayout()
        self.lo2.addWidget(self.line_ip)
        self.lo2.addWidget(self.line_port)

        self.lo3 = QHBoxLayout()
        self.lo3.addWidget(self.host_btn)

        self.gen_lo1 = QVBoxLayout()
        self.gen_lo1.addLayout(self.lo1)
        self.gen_lo1.addLayout(self.lo2)
        self.gen_lo1.addWidget(self.connect_btn)
        self.gen_lo1.addLayout(self.lo3)




        self.loy1 = QHBoxLayout()
        self.loy1.setSpacing(10)
        self.loy1.setContentsMargins(38,0,38,0)
        self.loy1.addWidget(self.btn_up1)
        self.loy1.addWidget(self.btn_up2)
        self.loy1.addWidget(self.btn_up3)
        self.loy1.addWidget(self.btn_up4)
        self.loy1.addWidget(self.btn_up5)

        self.loy2 = QHBoxLayout()
        self.loy2.setSpacing(10)
        self.loy2.setContentsMargins(38,0,38,0)
        self.loy2.addWidget(self.btn_down1)
        self.loy2.addWidget(self.btn_down2)
        self.loy2.addWidget(self.btn_down3)
        self.loy2.addWidget(self.btn_down4)
        self.loy2.addWidget(self.btn_down5)

        self.loy3 = QVBoxLayout()
        self.loy3.addWidget(self.btn_left1)
        self.loy3.addWidget(self.btn_left2)
        self.loy3.addWidget(self.btn_left3)
        self.loy3.addWidget(self.btn_left4)
        self.loy3.addWidget(self.btn_left5)

        self.loy4 = QVBoxLayout()
        self.loy4.addWidget(self.btn_right1)
        self.loy4.addWidget(self.btn_right2)
        self.loy4.addWidget(self.btn_right3)
        self.loy4.addWidget(self.btn_right4)
        self.loy4.addWidget(self.btn_right5)

        self.gridnbuttons = QHBoxLayout()
        self.gridnbuttons.addLayout(self.loy3)
        self.gridnbuttons.addLayout(self.grid)
        self.gridnbuttons.addLayout(self.loy4)

        self.loy5 = QHBoxLayout()
        self.loy5.addWidget(self.label1)

        self.gen_lo2 = QVBoxLayout()
        self.gen_lo2.addLayout(self.loy1)
        self.gen_lo2.addLayout(self.gridnbuttons)
        self.gen_lo2.addLayout(self.loy2)
        self.gen_lo2.addLayout(self.loy5)



        self.loyo1 = QHBoxLayout()
        self.loyo1.addWidget(self.table_players)
        self.loyo1.addWidget(self.start_game_btn)
        self.loyo1.addWidget(self.label2)


        self.gen_lo3 = QVBoxLayout()
        self.gen_lo3.addLayout(self.loyo1)


        ########### CENTRAL WIDGETS ###########
        self.widget1 = QWidget()
        self.widget1.setLayout(self.gen_lo1)

        self.widget2 = QWidget()
        self.widget2.setLayout(self.gen_lo2)

        self.widget3 = QWidget()
        self.widget3.setLayout(self.gen_lo3)

        self.stack.addWidget(self.widget1)
        self.stack.addWidget(self.widget2)
        self.stack.addWidget(self.widget3)

        self.setCentralWidget(self.stack)
        self.stack.setCurrentWidget(self.widget1)

        self.hide_widgets()


    def hide_widgets(self):
        for i in range(self.grid.count()):
            a = self.grid.itemAt(i).widget()
            if type(a) == type(QPushButton()):
                a.hide()
        for i in range(self.loy3.count()):
            a = self.loy3.itemAt(i).widget()
            if type(a) == type(QPushButton()):
                a.hide()
        for i in range(self.loy4.count()):
            a = self.loy4.itemAt(i).widget()
            if type(a) == type(QPushButton()):
                a.hide()

    def unhide_widgets(self):
        for i in range(self.grid.count()):
            a = self.grid.itemAt(i).widget()
            if type(a) == type(QPushButton()):
                a.show()
        for i in range(self.loy3.count()):
            a = self.loy3.itemAt(i).widget()
            if type(a) == type(QPushButton()):
                a.show()
        for i in range(self.loy4.count()):
            a = self.loy4.itemAt(i).widget()
            if type(a) == type(QPushButton()):
                a.show()

    def disable_widgets(self):
        for i in range(self.grid.count()):
            a = self.grid.itemAt(i).widget()
            if type(a) == type(QPushButton()):
                a.setDisabled(True)