from socket import *
import sqlite3

serverName = '0.0.0.0'
serverPort = 8080

# 서버 소켓 생성, listen
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)
print('the server is ready to receive')

# DB 초기화
conn = sqlite3.connect("messages.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guest TEXT NOT NULL,
    guestbook TEXT NOT NULL
)
""")
conn.commit()
conn.close()

# DB 함수들
def add_message(guest, guestbook):
  conn = sqlite3.connect("messages.db")
  cur = conn.cursor()
  cur.execute(
    "INSERT INTO messages (guest, guestbook) VALUES (?, ?)",
    (guest, guestbook)
  )
  new_id = cur.lastrowid
  conn.commit()
  conn.close()
  return new_id

def get_all_messages():
  conn = sqlite3.connect("messages.db")
  cur = conn.cursor()
  cur.execute("SELECT id, guest, guestbook FROM messages ORDER BY id ASC")
  rows = cur.fetchall()
  conn.close()
  return rows

def get_one_message(msg_id):
  conn = sqlite3.connect("messages.db")
  cur = conn.cursor()
  cur.execute("SELECT id, guest, guestbook FROM messages WHERE id=?", (msg_id,))
  row = cur.fetchone()
  conn.close()
  return row

def update_message(msg_id, guest, guestbook):
  conn = sqlite3.connect("messages.db")
  cur = conn.cursor()
  cur.execute(
      "UPDATE messages SET guest=?, guestbook=? WHERE id=?",
      (guest, guestbook, msg_id)
  )
  conn.commit()
  changed = cur.rowcount
  conn.close()
  return changed > 0

# 메인 루프
while True:
  try:
    # 커넥션 소켓 생성
    connectionSocket, addr = serverSocket.accept()
  except Exception:
    continue

  connectionSocket.settimeout(5)

  # 소켓에서 데이터 받아오기
  try:
    data = connectionSocket.recv(1024)

    if not data or b"\r\n\r\n" not in data:
      connectionSocket.close()
      continue

    try:
      request = data.decode("utf-8")
    except UnicodeDecodeError:
      connectionSocket.close()
      continue
  except (ConnectionResetError, timeout):
    connectionSocket.close()
    continue

  print(f"\r\n{request}")

  # 헤더, 바디 파싱
  header, body = request.split("\r\n\r\n", 1)
  lines = header.split("\r\n")
  parts = lines[0].split()

  if len(parts) != 3:
    connectionSocket.close()
    continue

  method, path, version = parts

  status_code = "200"
  status_phrase = "OK"
  response_body = ""

  # response message 구성, db 조작
  if method == 'POST':
    if not body or "said:" not in body:
      status_code = '400'
      status_phrase = 'Bad Request'
      response_body = "invalid body"

    elif path == '/':
      guest, guestbook = body.split("said:", 1)
      new_id = add_message(guest, guestbook)
      status_code = '201'
      status_phrase = 'Created'
      response_body = f"[{new_id}] '{guestbook}' - {guest}"
    else:
      status_code = '404'
      status_phrase = 'Not Found'
      response_body = "POST에는 index를 사용할 수 없습니다."

  elif method == 'GET':
    if path == '/':
      rows = get_all_messages()
      
      response_body = "\r\n".join(
        f"[{id}] '{guestbook}' - {guest}" for (id, guest, guestbook) in rows
      )
    else:
      parts = path.strip("/").split("/")

      if parts[-1].isdigit():
        idx = int(parts[-1])
        row = get_one_message(idx)

        if row:
          id, guest, guestbook = row
          response_body = f"[{id}] '{guestbook}' - {guest}"
        else:
          status_code = "404"
          status_phrase = "Not Found"
          response_body = "존재하지 않는 index입니다."
      else:
        status_code = "400"
        status_phrase = "Bad Request"
        response_body = "index는 정수여야 합니다."

  elif method == 'HEAD':
    parts = path.strip("/").split("/")

    if path == "/":
      response_body = ""
    elif parts[-1].isdigit():
      idx = int(parts[-1])
      row = get_one_message(idx)

      if not row:
        status_code = "404"
        status_phrase = "Not Found"
    else:
      status_code = "400"
      status_phrase = "Bad Request"

    response_body = ""

  elif method == "PUT":
    if not body or "said:" not in body:
      status_code = '400'
      status_phrase = 'Bad Request'
      response_body = "invalid body"
    else:
      parts = path.strip("/").split("/")
      if path == "/":
        status_code = "405"
        status_phrase = "Method Not Allowed"
        response_body = "덮어쓰기할 index를 입력해 주세요."
      elif parts[-1].isdigit():
        idx = int(parts[-1])

        guest, guestbook = body.split("said:", 1)
        guest = guest.strip()
        guestbook = guestbook.strip()

        ok = update_message(idx, guest, guestbook)
        
        if ok:
          response_body = f"성공적으로 {idx}를 덮어쓰기했습니다."
        else:
          status_code = "404"
          status_phrase = "Not Found"
          response_body = "존재하지 않는 index입니다."
      else:
        status_code = "400"
        status_phrase = "Bad Request"
        response_body = "index는 정수여야 합니다."
  else:
    status_code = '405'
    status_phrase = 'Method Not Allowed'
    response_body = "잘못된 method입니다."
  
  response = (
    f"{version} {status_code} {status_phrase}\r\n"
    f"Server: MyHTTP/1.0\r\n"
    f"Content-Type: text/plain; charset=utf-8\r\n"
    f"Content-Length: {str(len(response_body.encode()))}\r\n"
    f"\r\n"
    f"{response_body}"
  )

  # response request 전송
  try:
    connectionSocket.sendall(response.encode())
  except ConnectionResetError:
    pass

  # 커넥션 소켓 닫기
  connectionSocket.close()