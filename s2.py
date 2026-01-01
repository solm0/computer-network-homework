from socket import *

serverName = '127.0.0.1'
serverPort = 8080

# 서버 소켓 생성, 바인드
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind((serverName, serverPort))

# 서버 소켓 listen
serverSocket.listen(1)
print('the server is ready to receive')

while True:
  # request -> 커넥션 소켓 생성
  connectionSocket, addr = serverSocket.accept()

  while True:
    # 받기
    sentence = connectionSocket.recv(1024).decode()

    if not sentence:
      break

    # application
    print('received:', sentence)
    capitalizedSentence = sentence.upper()

    # 답 전송
    connectionSocket.send(capitalizedSentence.encode())
  
  connectionSocket.close()