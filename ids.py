import pandas as pd
import numpy as np
from keras.preprocessing.text import Tokenizer
import tensorflow as tf
import socket
from tkinter import *
import tkinter.ttk
import tkinter.messagebox
from datetime import datetime


# 소켓 통신 정보/학습 모델 로드
HOST = ''
PORT = 1825
dos_model = tf.keras.models.load_model('model/dos_model.h5')    # Dos 공격 학습 모델 로드
fuzzy_model = tf.keras.models.load_model('model/fuzzy_model.h5')    # Fuzzy 공격 학습 모델 로드
root = Tk()

# 전역변수 선언
score = ''
attack = ''
d_file = ''

# UI 구성 함수
def ui():

    # 스크롤바 생성
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Treeview(packet) - 패킷 리스트 출력
    packet = tkinter.ttk.Treeview(root, columns=['#1', '#2', '#3', '#4'], displaycolumns=['#1', '#2', '#3', '#4'],
                                  height=25, yscrollcommand=scrollbar.set)  # 컬럼 4개 추가(기본 1개)
    packet.pack(side='left', padx=10, pady=10)  # 왼쪽 정렬, 가로 세로 각 10 여백
    scrollbar.config(command=packet.yview)

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

    # state 트리 노드 값 삽입
    state.insert('', 'end', text='Host', values='127.0.0.1', iid='id_0')    # 호스트 IP
    state.insert('', 'end', text='Port', values=PORT, iid='id_1')           # 포트 번호
    state.insert('', 'end', text='Connection', values='OK', iid='id_2')     # 연결 상태
    state.insert('', 'end', text='Packet inflow', values=0, iid='id_3')     # 패킷 유입량
    state.insert('', 'end', text='Normal packet', values=0, iid='id_4')     # 정상 패킷
    state.insert('', 'end', text='Abnormal packet', values=0, iid='id_5')   # 비정상 패킷
    state.insert('', 'end', text='Degree of risk', values=0, iid='id_6')    # 위험도

    # 탐지 모드 실행 함수
    def connect():

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # IPv4/TCP 기반 통신
        server_socket.bind((HOST, PORT))    # 호스트, 포트 바인드
        server_socket.listen(5)     # 통신 대기
        client_socket, address = server_socket.accept()     # 클라이언트 정보 수신

        # 패킷 수신 함수
        def receive():
            file_size = int(client_socket.recv(1024).decode())  # 파일 사이즈 수신
            rec_file = client_socket.recv(file_size).decode()   # 파일 수신

            # 수신 파일 쓰기
            with open('rec_file.csv', 'w') as f:
                f.write(rec_file)
                f.close()

            # 수신된 패킷 검사
            def detect():
                global d_file
                global score
                global attack

                d_file = pd.read_csv('rec_file.csv', header=None)
                d_file.columns = ['TIME', 'ID', 'DLC', 'DATA']

                x = list()  # 빈 리스트 생성
                for i in range(0, len(d_file)):
                    tmp = d_file.loc[i].tolist()  # 데이터 프레임을 리스트로 변경
                    tmp.pop(0)  # TIME 제거
                    tmp.pop(1)  # DLC 제거
                    x.append(tmp)  # tmp 리스트 [ID, DATA] 를 x 리스트에 하나씩 저장

                if ['0', '0 0 0 0 0 0 0 0'] in x:

                    tokenizer = Tokenizer()
                    tokenizer.fit_on_texts(x)  # X 리스트에 저장된 데이터(str)를 int 타입으로 변경
                    sequences = tokenizer.texts_to_sequences(x)  # 변경된 X 데이터를 sequences 변수에 저장
                    X = np.array(sequences)
                    word_index = tokenizer.word_index  # 토큰화된 데이터를 사전에 저장

                    # 비정상 패킷 탐지
                    score = dos_model.predict(X)  # 테스트 데이터에 대해서 정확도 평가
                    attack = 'Dos attack was detected.'

                    record()

                else:

                    tokenizer = Tokenizer()
                    tokenizer.fit_on_texts(x)  # X 리스트에 저장된 데이터(str)를 int 타입으로 변경
                    sequences = tokenizer.texts_to_sequences(x)  # 변경된 X 데이터를 sequences 변수에 저장
                    X = np.array(sequences)
                    word_index = tokenizer.word_index  # 토큰화된 데이터를 사전에 저장

                    # 비정상 패킷 탐지
                    score = fuzzy_model.predict(X)  # 테스트 데이터에 대해서 정확도 평가
                    attack = 'Fuzzy attack was detected.'

                    record()

            detect()

        receive()

    # Button 생성
    start = tkinter.Button(root, text='Detect Mode', overrelief='raised', width=20, repeatdelay=1000,
                               repeatinterval=100, command=connect)
    start.pack(side='left', padx=10)

    close = tkinter.Button(root, text='Close', overrelief='raised', width=20, repeatdelay=1000, repeatinterval=100,
                               command=root.quit)
    close.pack(side='left', padx=10)

    # 탐지 결과 기록 함수
    def record():

        # Array -> List
        result = sum(score.tolist(), [])

        # 비어있는 변수 선언
        tree = list()
        outcome = list()
        count_a = 0
        count_n = 0

        # 탐지 결과를 리스트에 튜플 형태로 저장
        for k in range(0, len(d_file)):
            if result[k] >= 0.5:    # 예측값 0.5 이상시 비정상 패킷으로 판단
                outcome.append('Attack')
                count_a += 1
            else:   # 예측값 0.5 미만시 정상 패킷으로 판단
                outcome.append('Normal')
                count_n += 1

            tree_packet = (d_file['ID'][k], d_file['DLC'][k], d_file['DATA'][k], outcome[k])    # 탐지결과 -> 튜플
            tree.append(tree_packet)    # 튜플 -> 리스트

        # 탐지 결과 출력
        if attack == 'Dos attack was detected.':    # Dos 공격 출력
            for l in range(0, len(d_file)):
                packet.insert('', 'end', text=datetime.now(), values=tree[l])

        else:
            for m in range(0, len(d_file)):     # Fuzzy 공격 출력
                packet.insert('', 'end', text=(m+1, '/', datetime.now()), values=tree[m])

        # 탐지 결과 수치화
        state.item('id_3', values=len(d_file))  # 패킷 유입량
        state.item('id_4', values=count_n)      # 정상 패킷량
        state.item('id_5', values=count_a)      # 비정상 패킷량
        state.item('id_6', values=(count_a/len(d_file)))    # 위험도(비정상 패킷량/패킷 유입량)
        tkinter.messagebox.showwarning('Notice', attack)    # 공격 탐지 팝업 메시지

# 메인 함수
def main():
    root.title('CAR - IDS (ver 1.0)')  # GUI 타이틀 설정
    root.geometry('1000x500')  # UI 사이즈 설정
    root.resizable(FALSE, FALSE)  # 사이즈 변경 불가
    root.iconbitmap('icon.ico')     # UI 아이콘 설정
    root.mainloop()

if __name__ == '__main__':
    ui()
    main()
