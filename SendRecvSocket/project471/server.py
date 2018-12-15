 # Server code
from socket import *

# The port on which to listen
serverPort = 12000

# Create a TCP socket
serverSocket = socket(AF_INET,SOCK_STREAM)

# Bind the socket to the port
serverSocket.bind(('', serverPort))

# Start listening for incoming connections
serverSocket.listen(1)

print "The server is ready to receive"

data = "" #data that is sent accross

#Forever accept incoming connections
while 1:
	print ("Test 4")
	#accept a connectino; get client's socket
	connectionSocket, addr = serverSocket.accept()

	print ("Test 5")

	#the temporary buffer
	tmpBuff = ""

	while len(data) != 40:
		#receive whatever the newly connected client has to send
		tmpBuff = connectionSocket.recv(40)

		#the other side unexpectedly closed it's socket
		if not tmpBuff:
			break

		#save the data
		data += tmpBuff

		print("In server while loop...")
		
	print data
	
	#close the socket
	connectionSocket.close()
