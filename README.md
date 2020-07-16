< 프로젝트 소개 >

차량 네트워크상으로 유입되는 외부 패킷이 정상인지 비정상인지 식별하는 AI기반 탐지 시스템.


< 사용 기술 >

- LSTM 딥러닝 알고리즘 사용

- 사용자의 편의를 위한 UI 구현

- 가상으로 구현된 해킹 시스템(TCP 통신)



< 파일 설명 >

- attack(폴더): 공격 패킷 파일 저장 폴더(파일 당 패킷 5000개)

- model(폴더): 학습 모델 저장 폴더

- attacker.py: 프로그램 상의 공격툴

- ids.py: 패킷 탐지 시스템

- model.py: 학습 모델 생성 파일

- rec_file.csv: 수신된 패킷 파일


< 동작 방법 >
※ 순서를 반드시 지킬 것

- ids.py 와 attacker.py 실행(CAR-IDS(ver 1.0), Attack Tool 각 2가지의 UI가 실행됨)

- CAR-IDS 에서 'Detect Mode' 버튼 클릭(외부에서 패킷을 받아들일 수 있는 상태로 전환)

- Attack Tool 에서 'Packet Transmission' 버튼 클릭 후 전송할 패킷 파일 선택(Dos 공격 4파일/Fuzzy 공격 4파일)

- CAR-IDS 에서 수신한 패킷을 분석하여 결과를 UI에 출력
