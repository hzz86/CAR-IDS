import socket
import time
import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd
from scapy.layers.can import *


HOST = ''
PORT = 1825

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

client_socket, address = server_socket.accept()

print('### Ready to transmit ###')
while 1:

    root = tk.Tk()
    root.withdraw()
    send_file_path = filedialog.askopenfilename()
    send_file = pd.read_csv(send_file_path, header=None)

    for i in range(0, 10):
        s_packet = send_file.loc[i].tolist()
        s_packet.pop(0)   # TIME 제거
        s_packet.pop(1)   # DLC 제거
        s_packet = '/'.join(s_packet)
        print(i, s_packet)
        client_socket.sendall(s_packet.encode())
        time.sleep(0.005)

    break
