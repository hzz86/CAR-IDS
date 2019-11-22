import pandas as pd
import numpy as np
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
import tkinter as tk
from tkinter import filedialog
import tensorflow as tf
import socket
import time
from tkinter import *
import tkinter.ttk


HOST = 'localhost'
PORT = 1825

root = Tk()
root.title('CAR - IDS (ver 1.0)')  # GUI 타이틀 설정
root.geometry('1000x500')  # GUI 사이즈 설정
root.resizable(FALSE, FALSE)  # 사이즈 변경 불가
root.iconbitmap('icon.ico')

def detect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))  # 서버 - 클라이언트 연결

    x = list()
    for i in range(0, 10):
        r_frame = client_socket.recv(512).decode()
        print(i, r_frame)
        r_frame = r_frame.split('/')
        x.append(r_frame)

    print(x)
    print(len(x))

    for j in range(0, 10):
        if x[j][0] == '0' and x[j][1] == '0 0 0 0 0 0 0 0':
            print('Dos Attack Detected')

        elif x[j] == '':
            pass

        else:
            tokenizer = Tokenizer()
            tokenizer.fit_on_texts(x)  # X 리스트에 저장된 데이터(str)를 int 타입으로 변경
            sequences = tokenizer.texts_to_sequences(x)  # 변경된 X 데이터를 sequences 변수에 저장
            X = np.array(sequences)
            word_index = tokenizer.word_index  # 토큰화된 데이터를 사전에 저장
            model = tf.keras.models.load_model('model/fuzzy_model.h5')
            result = model.predict(X)
            print('Working well')

packet = tkinter.ttk.Treeview(root, columns=['#1', '#2', '#3', '#4'], displaycolumns=['#1', '#2', '#3', '#4'],
                                       height=25)  # 컬럼 4개 추가(기본 1개)
packet.pack(side='left', padx=10, pady=10)  # 왼쪽 정렬, 가로 세로 각 10 여백

# Treeview(packet) 컬럼명 설정
packet.column('#0', width=130)
packet.heading('#0', text='TIME')

packet.column('#1', width=130)
packet.heading('#1', text='ID')

packet.column('#2', width=130)
packet.heading('#2', text='DLC')

packet.column('#3', width=130)
packet.heading('#3', text='DATA')

packet.column('#4', width=130)
packet.heading('#4', text='RESULT')

# Treeview(state) - IDS 상태 표시 리스트 생성
state = tkinter.ttk.Treeview(root, columns=['#1'], displaycolumns=['#1'], height=20)
state.pack(pady=10)

# Treeview(state) 컬럼명 설정
state.column('#0', width=150)
state.heading('#0', text='ELEMENT')

state.column('#1', width=150)
state.heading('#1', text='STATE')

# 노드 값 삽입
state.insert('', 'end', text='Operation', iid='id_0')
state.insert('', 'end', text='Packet inflow', iid='id_1')
state.insert('', 'end', text='Abnormal packet', iid='id_2')
state.insert('', 'end', text='Degree of risk', iid='id_3')

# Button 생성
start = tkinter.Button(root, text='Start to Detect', overrelief='raised', width=20, repeatdelay=1000, repeatinterval=100, command=detect)
start.pack(side='left', padx=10)

exit = tkinter.Button(root, text='exit', overrelief='raised', width=20, repeatdelay=1000, repeatinterval=100, command=root.quit)
exit.pack(side='left', padx=10)

if __name__ == '__main__':
    root.mainloop()
