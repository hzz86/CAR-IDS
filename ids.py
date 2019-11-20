from tkinter import *

# 사용자 인터페이스 구현
root = Tk()
root.title('CAR - IDS')     # 타이틀 설정
root.geometry('700x500')    # 사이즈 설정
#root.resizable(width=False, height=False)   # 사이즈 고정

pk_window = Listbox(root, height=10)    # 패킷 리스트창 생성
pk_result = Listbox(root, height=10)    # 패킷 탐지 결과창 생성
pk_window.pack()
pk_result.pack()

root.mainloop()

