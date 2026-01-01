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
    request = connectionSocket.recv(1024).decode()

    if not request:
      break

    # application
    header, body = request.split("\r\n\r\n", 1)

    lines = header.split("\r\n")
    request_line = lines[0]
    method, path, version = request_line.split(" ")

    if method == 'POST':
      if path == '/':
        status_code = '200'
        status_phrase = 'OK'
        body = body
      else:
        status_code = '404'
        status_phrase = 'Not Found'
        body = ""
    else:
      status_code = '405'
      status_phrase = 'Method Not Allowed'
      body = ""
    
    response = f"{version} {status_code} {status_phrase}\r\nContent-Type: text/plain\r\n\r\n{body}"
    # 답 전송
    connectionSocket.send(response.encode())
  
  connectionSocket.close()