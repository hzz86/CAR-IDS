import socket
from tkinter import filedialog
import os
from tkinter import *
import tkinter.ttk

# 소켓 통신 정보
HOST = 'localhost'
PORT = 1825
root = Tk()

# UI 구성 함수
def ui():
    # 안내 문구 출력
    label = tkinter.Label(root, text='This program is a tool for sending packets.', fg='blue')
    label.pack(side='top', pady=20)

    # 패킷 전송 버튼 생성
    send = tkinter.Button(root, text='Packet Transmission', overrelief='raised', width=20, repeatdelay=1000,
                          repeatinterval=100, command=connect)
    send.pack(side='left', padx=10)

    # 종료 버튼
    close = tkinter.Button(root, text='Close', overrelief='raised', width=20, repeatdelay=1000, repeatinterval=100,
                           command=root.quit)
    close.pack(side='left', padx=10)

# 소켓 통신 함수
def connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # IPv4/TCP 기반 통신
    client_socket.connect((HOST, PORT))  # 서버 - 클라이언트 연결

    # 전송 함수
    def transmit():
        send_file_path = filedialog.askopenfilename()   # 파일 다이얼로그 실행

        # 선택한 파일 불러오기
        with open(send_file_path, 'r') as f:
            send_file = f.read()

        file_size = str(os.path.getsize(send_file_path))    # 파일 사이즈 추출
        client_socket.send(file_size.encode())  # 파일 사이즈 전송
        client_socket.send(send_file.encode())  # 파일 전송

    transmit()

# 메인 함수
def main():
    root.title('Attack Tool')  # UI 타이틀 설정
    root.geometry('300x100')  # UI 사이즈 설정
    root.resizable(FALSE, FALSE)  # 사이즈 변경 불가
    root.iconbitmap('swords.ico')     # UI 아이콘 설정
    root.mainloop()

if __name__ == '__main__':
    ui()
    main()

