from socket import *

serverName = '127.0.0.1'
serverPort = 8080
messages = []

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
    print(f"\r\n{request}")

    if not request:
      break

    # application
    header, body = request.split("\r\n\r\n", 1)

    lines = header.split("\r\n")
    request_line = lines[0]
    method, path, version = request_line.split(" ")

    if method == 'POST':
      if path == '/':
        messages.append(body)
        status_code = '201'
        status_phrase = 'Created'
        response_body = body
      else:
        status_code = '404'
        status_phrase = 'Not Found'
        response_body = "POST에는 index를 사용할 수 없습니다."
    elif method == 'GET':
      if path == '/':
        status_code = '200'
        status_phrase = 'OK'
        
        response_body = (
          f"messages = ["
          f"{'' if len(messages) < 1 else f"\r\n{"\r\n".join(f"\t{i}: {msg}" for i, msg in enumerate(messages))}\r\n"}"
          f"]"
        )
      else:
        parts = path.strip("/").split("/")
        if parts[-1].isdigit():
          idx = int(parts[-1])
          if len(messages) > idx:
            status_code = '200'
            status_phrase = 'OK'
            response_body = f"{idx}: {messages[idx]}"
          else:
            status_code = '404'
            status_phrase = 'Not Found'
            response_body = "index의 범위가 잘못되었습니다."
        else:
          status_code = '400'
          status_phrase = 'Bad Request'
          response_body = "index는 정수여야 합니다."
    elif method == 'HEAD':
      if path == '/':
        status_code = '200'
        status_phrase = 'OK'
        response_body = ""
      else:
        parts = path.strip("/").split("/")
        if parts[-1].isdigit():
          idx = int(parts[-1])
          if len(messages) > idx:
            status_code = '200'
            status_phrase = 'OK'
            response_body = ""
          else:
            status_code = '404'
            status_phrase = 'Not Found'
            response_body = ""
        else:
          status_code = '400'
          status_phrase = 'Bad Request'
          response_body = ""
    elif method == "PUT":
      if path == '/':
        status_code = '405'
        status_phrase = 'Method Not Allowed'
        response_body = "덮어쓰기할 index를 입력하세요."
      else:
        parts = path.strip("/").split("/")
        if parts[-1].isdigit():
          idx = int(parts[-1])
          if len(messages) > idx:
            messages[idx] = body
            status_code = '200'
            status_phrase = 'OK'
            response_body = f"{idx}의 값을 성공적으로 덮어썼습니다."
          else:
            status_code = '404'
            status_phrase = 'Not Found'
            response_body = "index의 범위가 잘못되었습니다."
        else:
          status_code = '400'
          status_phrase = 'Bad Request'
          response_body = "index는 정수여야 합니다."
    else:
      status_code = '405'
      status_phrase = 'Method Not Allowed'
      response_body = "잘못된 method입니다."
    
    # 답 전송
    response = (
      f"{version} {status_code} {status_phrase}\r\n"
      f"Server: MyHTTP/1.0\r\n"
      f"Content-Type: text/plain; charset=utf-8\r\n"
      f"Content-Length: {str(len(response_body.encode()))}\r\n"
      f"\r\n"
      f"{response_body}"
    )
    connectionSocket.send(response.encode())
  
  connectionSocket.close()