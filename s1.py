from socket import *
serverName = '127.0.0.1'
serverPort = 8080

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)
print('the server is ready to receive')

while True:
  connectionSocket, addr = serverSocket.accept()

  sentence = connectionSocket.recv(1024).decode()
  capitalizedSentence = sentence.upper()
  print(capitalizedSentence)
  connectionSocket.send(capitalizedSentence.encode())
  connectionSocket.close()