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
  path = '/'
  method = "POST"

  request_msg = f"{method} {path} HTTP/1.1\r\nHost: {serverName}\r\n\r\n{sentence}"
  
  # 전송
  clientSocket.send(request_msg.encode())

  # 받기
  response = clientSocket.recv(1024).decode()

  # application
  header, body = response.split("\r\n\r\n", 1)

  lines = header.split("\r\n")
  response_line = lines[0]
  version, status_code, *status_phrase = response_line.split(" ")
  status_phrase = " ".join(status_phrase)

  if status_code == '200':
    message = body
  elif status_code == '404':
    message = 'path is wrong'
  elif status_code == '405':
    message = 'method is wrong'
  else:
    message = 'sth is wrong'

  output = f"output: {message}"
  print(output)

clientSocket.close()