from socket import *
serverName = '127.0.0.1'
serverPort = 8080

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input('ffdfd')
clientSocket.send(sentence.encode())

modifiedSentence = clientSocket.recv(1024) # 소켓으로부터 최대 #byte의 데이터를 수신함.
print('from server:', modifiedSentence.decode())
clientSocket.close()