from socket import *
import sqlite3

serverName = '127.0.0.1'
serverPort = 8081

# 서버 소켓 생성
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)
print('the server is ready to receive')

# DB 준비
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
  connectionSocket, addr = serverSocket.accept()
  try:
    request = connectionSocket.recv(1024).decode()
    if not request:
      connectionSocket.close()
      continue
  except ConnectionResetError:
    connectionSocket.close()
    continue

  print(f"\r\n{request}")

  # http 메시지 파싱
  if "\r\n\r\n" in request:
    header, body = request.split("\r\n\r\n", 1)
  else:
    header, body = request, ""

  lines = header.split("\r\n")
  method, path, version = lines[0].split(" ")

  status_code = "200"
  status_phrase = "OK"
  response_body = ""

  # 
  if method in ('POST', 'PUT'):
    if not body or "said:" not in body:
      status_code = '400'
      status_phrase = 'Bad Request'
      response_body = "invalid body"

  if method == 'POST':
    if path == '/':
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