import tkinter as tk
from tkinter import ttk
from socket import *

serverName = '158.247.200.157'
serverPort = 8080

root = tk.Tk()
root.title("v10")
root.geometry("500x650")

selected = tk.StringVar(value="POST")


def send_request():
  # 클라이언트 소켓 생성, 연결
  clientSocket = socket(AF_INET, SOCK_STREAM)
  clientSocket.connect((serverName, serverPort))

  # 인풋 받기
  method = selected.get()
  path_input = path_entry.get()
  path = f"/{path_input}"
  guest = entry.get() if entry.get() != "" else '익명'
  guestbook = entry_2.get()
  request_body = '' if method == "GET" else f"{guest}said:{guestbook}"

  request_msg = (
    f"{method} {path} HTTP/1.1\r\n"
    f"Host: {serverName}\r\n"
    f"User-Agent: HelloSocket/1.0\r\n"
    f"Accept: text/plain; charset=utf-8\r\n"
    f"Content-Length: {str(len(request_body.encode()))}\r\n"
    f"\r\n"
    f"{request_body}"
  )

  clientSocket.send(request_msg.encode())

  response = ""
  while True:
      chunk = clientSocket.recv(1024).decode()
      if not chunk:
          break
      response += chunk
  
  print(f"\r\n{response}")

  header, body = response.split("\r\n\r\n", 1)

  lines = header.split("\r\n")
  version, status_code, status_phrase = lines[0].split(" ", 2)
  
  message = f"{status_code} {status_phrase}"
    
  output.config(text=message)
  entry.delete(0, tk.END)
  entry_2.delete(0, tk.END)
  path_entry.delete(0, tk.END)

  cumulative_output.delete("1.0", "end")
  cumulative_output.insert("end", body)

  clientSocket.close()


def on_close():
  root.destroy()






header_title = tk.Label(root, text="Hello Socket", font=("Helvetica", 18, "bold"))
header_title.pack(padx=10, pady=10, anchor="w")

################################
# 제목: header
################################
separator = ttk.Separator(root, orient="horizontal")
separator.pack(fill="x")

header_title = tk.Label(root, text="header")
header_title.pack(padx=10, pady=2, anchor="w")

separator = ttk.Separator(root, orient="horizontal")
separator.pack(fill="x", pady=2)

################################
# method / path → width 절반씩
################################
top_frame = tk.Frame(root)
top_frame.pack(fill="x", padx=10, pady=10)

# --- method 영역 ---
method_frame = tk.Frame(top_frame)
method_frame.pack(side="left", expand=True, fill="both")

tk.Label(method_frame, text="HTTP method를 선택하세요").pack(anchor="w")
def update_index_input():
  button.config(text=selected.get())
  output.config(text='')
  cumulative_output.delete("1.0", "end")

  if selected.get() in ['POST', 'PUT', '???']:
    entry.config(state='normal')
    entry_label.config(state='normal')
    entry_2.config(state='normal')
    entry_label_2.config(state='normal')
  else:
    entry.delete(0, tk.END)
    entry.config(state='disabled')
    entry_label.config(state='disabled')
    entry_2.config(state='disabled')
    entry_label_2.config(state='disabled')

tk.Radiobutton(method_frame, text="GET", value="GET", variable=selected, command=update_index_input).pack(anchor="w")
tk.Radiobutton(method_frame, text="POST", value="POST", variable=selected, command=update_index_input).pack(anchor="w")
tk.Radiobutton(method_frame, text="PUT",  value="PUT",  variable=selected, command=update_index_input).pack(anchor="w")
tk.Radiobutton(method_frame, text="HEAD", value="HEAD", variable=selected, command=update_index_input).pack(anchor="w")
tk.Radiobutton(method_frame, text="난 HTTP를 거부하겠다",  value="???",  variable=selected, command=update_index_input).pack(anchor="w")

# --- path 영역 ---
path_frame = tk.Frame(top_frame)
path_frame.pack(side="left", expand=True, fill="both")

tk.Label(path_frame, text="PUT/GET할 index를 입력하세요").pack(anchor="w")

row = tk.Frame(path_frame)
row.pack(anchor="w")

tk.Label(row, text="/").pack(side="left")

path_entry = tk.Entry(row, width=15)
path_entry.pack(side="left")

################################
# 제목: body
################################
separator = ttk.Separator(root, orient="horizontal")
separator.pack(fill="x")

body_title = tk.Label(root, text="body")
body_title.pack(padx=10, pady=2, anchor="w")

separator = ttk.Separator(root, orient="horizontal")
separator.pack(fill="x", pady=2)

# 입력 텍스트
entry_row = tk.Frame(root)
entry_row.pack(anchor="w", padx=10)

entry_label = tk.Label(entry_row, text="작성자")
entry_label.pack(pady=10, side="left")

entry = tk.Entry(entry_row, width=40)
entry.pack(side="left", padx=10)
entry.config(disabledbackground="#2C2C2C", disabledforeground="#bbbbbb")


entry_row_2 = tk.Frame(root)
entry_row_2.pack(anchor="w", padx=10)

entry_label_2 = tk.Label(entry_row_2, text="메세지")   # 여기 수정
entry_label_2.pack(pady=10, side="left")

entry_2 = tk.Entry(entry_row_2, width=40)
entry_2.pack(side="left", padx=10)
entry_2.config(disabledbackground="#2C2C2C", disabledforeground="#bbbbbb")

################################
# 전송 버튼 + 출력 → 가로정렬
################################
separator = ttk.Separator(root, orient="horizontal")
separator.pack(fill="x")

send_row = tk.Frame(root)
send_row.pack(anchor="w", padx=10, pady=10)

button = tk.Button(send_row, text=selected.get(), command=send_request)
button.pack(side="left")

output = tk.Label(send_row, text="")
output.pack(side="left", padx=10)


################################
# 결과
################################

text_frame = tk.Frame(root)
text_frame.pack(anchor="w", padx=10, pady=5, fill="both", expand=True)

scrollbar = tk.Scrollbar(text_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

cumulative_output = tk.Text(
  text_frame,
  width=50,
  height=20,
  yscrollcommand=scrollbar.set,
  bg="#333333",
  fg="#ffffff",
  highlightthickness=0,
  tabs=("20p",)
)
def block_edit(event):
    return "break"
cumulative_output.bind("<Key>", block_edit)
cumulative_output.bind("<BackSpace>", block_edit)
cumulative_output.bind("<Delete>", block_edit)
cumulative_output.pack(side="left", fill="both", expand=True)

scrollbar.config(command=cumulative_output.yview)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()