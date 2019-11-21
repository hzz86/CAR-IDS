from tkinter import *
import tkinter.ttk

# GUI 설정
root = Tk()
root.title('CAR - IDS (ver 1.0)')     # GUI 타이틀 설정
root.geometry('1000x500')   # GUI 사이즈 설정
root.resizable(FALSE, FALSE)    # 사이즈 변경 불가
root.iconbitmap('icon.ico')

# Treeview(packet) - 수신된 CAN 패킷 리스트 생성
packet = tkinter.ttk.Treeview(root, columns=['#1', '#2', '#3', '#4'], displaycolumns=['#1', '#2', '#3', '#4'], height=25) # 컬럼 4개 추가(기본 1개)
packet.pack(side='left', padx=10, pady=10)    # 왼쪽 정렬, 가로 세로 각 10 여백

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

state.column('#0', width=150)
state.heading('#0', text='ELEMENT')
state.insert('', 'end', text='Operation', values='normal')
state.insert('', 'end', text='Packet inflow', values=9223)
state.insert('', 'end', text='Abnormal packet', values=2342)
state.insert('', 'end', text='Degree of risk', values=0.2539)

state.column('#1', width=150)
state.heading('#1', text='STATE')

# Button 생성
clear = tkinter.Button(root, text='Clear', overrelief='raised', width=20, repeatdelay=1000, repeatinterval=100)
clear.pack(side='left', padx=10)

exit = tkinter.Button(root, text='Exit', overrelief='raised', width=20, repeatdelay=1000, repeatinterval=100)
exit.pack(side='left', padx=10)


root.mainloop()
