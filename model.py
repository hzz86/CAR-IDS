import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
import tensorflow as tf


# 사용자 다이얼로그 - 학습할 파일 읽기
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()    # 선택된 파일 경로 저장
train_file = pd.read_csv(file_path, header=None)    # 선택된 .csv 파일을 읽어 train_file 변수에 저장
train_file.columns = ['TIME', 'ID', 'DLC', 'DATA', 'RESULT']  # 컬럼 이름 지정

# 데이터 전처리
train_file.RESULT = train_file.RESULT.replace(['R', 'T'], [0, 1])  # 이진분류를 위해 R, T를 0, 1로 변경
x = list()  # 빈 리스트 생성

for i in range(0, len(train_file)):
    tmp = train_file.loc[i].tolist()  # 데이터 프레임을 리스트로 변경
    tmp.pop(0)  # TIME 제거
    tmp.pop(1)  # DLC 제거
    tmp.pop(2)  # RESULT 제거
    x.append(tmp)  # tmp 리스트 [ID, DATA] 를 x 리스트에 하나씩 저장
    # 학습에 필요한 ID, DATA 컬럼을 제외하고 모두 제거

Y = train_file.RESULT.tolist()  # RESULT 컬럼 리스트로 변경

# 데이터 토큰화
tokenizer = Tokenizer()
tokenizer.fit_on_texts(x)  # X 리스트에 저장된 데이터(str)를 int 타입으로 변경
sequences = tokenizer.texts_to_sequences(x)  # 변경된 X 데이터를 sequences 변수에 저장

# 학습 데이터용 변수 선언
X = np.array(sequences)
y = np.array(Y)
word_index = tokenizer.word_index  # 토큰화된 데이터를 사전에 저장

# 데이터 분리(학습/검증)
n_of_train = int(len(X) * 0.8)  # 전체 데이터의 80%
X_test = X[n_of_train:]
y_test = np.array(y[n_of_train:])
X_train = X[:n_of_train]
y_train = np.array(y[:n_of_train])

# 모델링(LSTM 알고리즘 구현)
vocab_size = len(word_index) + 1  # 단어 집합 크기
model = Sequential()
model.add(Embedding(vocab_size, 64))  # 단어 집합의 크기: vacab_size/ 임베딩 후 벡터 크기: 64
model.add(LSTM(64))  # LSTM 셀 크기 64
model.add(Dense(1, input_dim=2, activation='sigmoid'))

# 학습 및 결과 출력
model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.001)
              , loss=tf.keras.losses.binary_crossentropy
              , metrics=[tf.keras.metrics.Precision(name='precision')
              , tf.keras.metrics.Recall(name='recall')
              , tf.keras.metrics.FalsePositives(name='false_positives')
              , tf.keras.metrics.FalseNegatives(name='false_negatives')])
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=4096)
scores = model.evaluate(X_test, y_test, verbose=0)  # 테스트 데이터에 대해서 정확도 평가
print('Accuracy: %.2f%%' % (scores[1] * 100))

# 학습 모델 저장
print('Enter a file(.h5) name to save.')
model_name = input()
model.save(model_name)
del model
print('\nSaved successfully!')



