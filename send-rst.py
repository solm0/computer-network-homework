import socket, struct, time

s = socket.socket()
s.connect(("127.0.0.1", 8080))
s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
s.close()