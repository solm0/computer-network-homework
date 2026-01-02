vscode에서 파이썬실행하기: 익스텐션에서 python 깔기, cmd+sft p > python:select interpreter

python3 main.py하면 실행되는데 py로 명령어 바꾸고싶으면

echo "alias py=python3" >> ~/.zshrc
source ~/.zshrc

# 1

예제에 있던대로 raw_input('') 했는데 python3에서 input('')으로 바뀌었다고한다.

클라이언트만 쓰고 실행하면 이렇게뜨.
clientSocket.connect((serverName, serverPort))
ConnectionRefusedError: [Errno 61] Connection refused

- 서
터미널 끄면 time_wait있는데 터미널 끌때 바로 닫으려면 serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


# 2
한 tcp커넥션에서 반복해서 보내기

- 클: if 추가
- 서: if 추가

# 3
http프로토콜얹기를 시작했다.
클라이언트에서 input을 http헤더에넣어 보내고, 서버에서 파싱해서 response를 만들어 보내고, 클라이언트에서 다시 파싱해서 output을 만들게했다.

- 근데 아직 클라이언트에서는 input밖에 설정을 못한다. method랑 path도 고를 수 있게 하고 싶다.
- 서버는 POST밖에 처리를안하고 status code가 200,404,405뿐이다.

알게된ㄷ것: 자바스크립트는 block scope지만
파이썬은 블록스코프가 없고 함수,클래스,모듈만 스코프를 만들어서 if안에서 만든 변수가 if밖에서도 보인다고한다.

# 4
echo
- 클라이언트에서 tkinter추가해서 입력,버튼누르면 서버로전송. 아웃풋 업데이트

# 5
- GET: 인풋 쌓기
  - 서버는 배열에 메세지 저장
  - 클라이언트 버튼누를때마다 배열가져와서 파싱해서 렌더 
    - 앞에 인덱스붙이기



# 6
- POST/HEAD/PUT 라디오버튼으로 선택하게 하기
- path 넣는 필드. 기본값 /
- ui
  - 전송됐으면 칸 비우기
  - 왼쪽정렬
  - PUT선택시 인덱스넣는필드도 렌더.



# 7
- PUT구현: 인덱스 하면 그인덱스 고쳐지게

.strip("/")은 없앰
int()는 인자가 정수여야함
.isdigit() 으로 정수인지 확인

status code 수정
- put에 식별자 없으면 405가 더 낫다고 함
- post 성공시 201이 낫다고함
- put range 벗어난경우 404가 낫다고함

- request, response 전문 터미널에 찍히게
- get,head with path

- 모든 method의 버튼 하나로통일


# 와이어샤크설치

맥 ip주소 찾기
- 로컬ip: `ipconfig getifaddr en0`
- 공인ip: `curl ifconfig.me`