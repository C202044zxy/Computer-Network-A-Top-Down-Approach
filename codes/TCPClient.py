from socket import *
serverName = '100.67.74.250'  # ip address of my laptop
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

sentence = input()

clientSocket.send(sentence.encode())
clientSocket.close()