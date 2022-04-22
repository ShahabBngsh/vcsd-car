import socket
from socket import SHUT_RDWR
import os
if __name__ == '__main__':
  # host = '127.0.0.1'  # Server
  # port = 4001
  # serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  # serverSocket.bind((host, port))
  serverSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  serverSocket.bind(('127.0.0.1',4018))#Server address i.e
  serverSocket.listen(5)
  conn, addr = serverSocket.accept()
  conn.setblocking(0)
  while(1):
    try:
      # print ('connection from',addr)
      data=conn.recv(1000).decode()
      print ("Received Input is: "+str(data))
      if data=='e':
        conn.close()
        serverSocket.close()
        break
    except:
      print("works")

