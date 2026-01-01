import tkinter as tk
from socket import *

serverName = '127.0.0.1'
serverPort = 8080
message = ""

# 클라이언트 소켓 생성, 연결
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

def send_request():
  # 인풋 받기
  sentence = entry.get()

  method = "POST"
  path = '/'
  global message

  request_msg = (
    f"{method} {path} HTTP/1.1\r\n"
    f"Host: {serverName}\r\n"
    f"\r\n"
    f"{sentence}"
  )

  clientSocket.send(request_msg.encode())

  response = clientSocket.recv(1024).decode()
  header, body = response.split("\r\n\r\n", 1)

  lines = header.split("\r\n")
  response_line = lines[0]
  version, status_code, status_phrase = response_line.split(" ")

  if status_code == '200':
    message = body
  elif status_code == '404':
    message = 'path is wrong'
  elif status_code == '405':
    message = 'method is wrong'
  else:
    message = 'sth is wrong'
  
  output.config(text=message)

def on_close():
  clientSocket.close()
  root.destroy()

root = tk.Tk()
root.title("echo")

entry = tk.Entry(root, width=40)
entry.pack()

button = tk.Button(root, text="전송", command=send_request)
button.pack()

output = tk.Label(root, text=message)
output.pack()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()