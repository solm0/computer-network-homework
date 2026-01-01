from socket import *

serverName = '127.0.0.1'
serverPort = 8080

# 클라이언트 소켓 생성, 연결
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
  # 인풋 받기
  sentence = input('input: ')
  if sentence == 'quit':
    break

  # application

  
  # 전송
  clientSocket.send(sentence.encode())

  # 받기
  modifiedSentence = clientSocket.recv(1024).decode()

  # application
  print('from server:', modifiedSentence)

clientSocket.close()