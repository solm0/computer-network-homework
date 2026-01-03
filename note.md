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



# 8
- 서: sqlite만들기
- 클: 


# 9
vps에서 서버계속돌아가게하기

tmux 설치 `sudo apt install tmux`
세션생성 `tmux new -s 세션이름`
서버실행

tmux 세션 다시 들어가기
`tmux ls`
`tmux attach -t 세션이름`

서버 중지
Ctrl+b, `:`적고 `kill -t 세션이름`



# 10

ssh를 닫고 다음날 다시 tmux세션에 들어갔더니 이렇게 떴다
```bash
Accept-Encoding: gzip

Traceback (most recent call last):
  File "/root/projects/2026/computer-network-homework/s9.py", line 72, in <module>
    request = connectionSocket.recv(1024).decode()
ConnectionResetError: [Errno 104] Connection reset by peer
```

상대(peer)가 커넥션 종료: 클라이언트가 연결을 정상종료(FIN)이 아니라 강제로 끊었다(RST)?

내 클라이언트는 Accept-Encoding: gzip을 한 적이 없는데 스캐너

챗지피티가 이런 방어 코드를 쓰라고 했다.

방어 코드가 없는 서버에 같은 에러를 다시 내려고 해봤다. curl은 에러를 안냈다.
```bash
nc 127.0.0.1 8080
```
TCP연결만 하고 아무 HTTP요청도 안했다.


```bash
Traceback (most recent call last):
  File "/root/projects/2026/computer-network-homework/s9.py", line 86, in <module>
    method, path, version = lines[0].split(" ")
ValueError: not enough values to unpack
```

그랬더니 헤더 파싱에서 ValueError가 났다.

하지만 ConnectionResetError는 아니다.

그래서 이번에는 ConnectionResetError를 내기 위해 RST가일어나게 해봤다.(send-rst.py)

```py
import socket, struct, time

s = socket.socket()
s.connect(("127.0.0.1", 8080))

# linger on, timeout = 0 → RST
s.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_LINGER,
    struct.pack("ii", 1, 0)
)

s.send(b"GET / HTTP/1.1\r\n")
s.close()
```

그랬더니 거의 같은 에러를 볼 수 있었다.

```bash
Traceback (most recent call last):
  File "/root/projects/2026/computer-network-homework/s9.py", line 183, in <module>
    connectionSocket.send(response.encode())
ConnectionResetError: [Errno 104] Connection reset by peer
```

근데 다른점은 recv가 아니라 send에서 났다는것.. 근데 그건 타이밍 문제라고 한다.

아니 근데? 서버를 재시작하고 다시 했더니 이번에는 에러가 안 났다. 그래서 이렇게 (아무것도 안 보내고 close)고쳤더니

```py
import socket, struct, time

s = socket.socket()
s.connect(("127.0.0.1", 8080))
s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
s.close()
```
이제 100% 에러가 난다.


그리고
try:
    request = connectionSocket.recv(1024).decode()
    if not request:
      connectionSocket.close()
      continue
  except ConnectionResetError:
    connectionSocket.close()
    continue

를 추가한 s10.py에서는 rst를 보내도 에러가 나지 않는다.




그리고 하는동안 이런 요청들이 서버에 찍혔다.
```bash
GET http://api.ipify.org/?format=json HTTP/1.1
Host: api.ipify.org
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36

CONNECT www.shadowserver.org:443 HTTP/1.1
Host: www.shadowserver.org
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36
Connection: Keep-Alive
Pragma: no-cache
Proxy-Connection: Keep-Alive

GET /geoserver/web/ HTTP/1.1
Host: 158.247.200.157:8080
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36
Accept: */*
Accept-Encoding: gzip

GET http://httpbin.org/ip HTTP/1.1
Host: httpbin.org
User-Agent: ProxyPool-Scanner/2.0
Connection: close
Accept-Encoding: gzip

GET http://proxychecker.vultr.com/ HTTP/1.1
Host: proxychecker.vultr.com
User-Agent: Mozilla/5.0 zgrab/0.x
Accept: */*
Accept-Encoding: gzip
```

순서대로 프록시 테스트, 프록시 테스트, 취약 서버 스캔이라고 한다.
vps ip는 이미 전세계 스캐너 db에 있어서 포트 8080 열리는 순간 프록시테스트,봇 등등이 접근 시도한다고.