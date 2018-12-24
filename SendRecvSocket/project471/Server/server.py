 # Server code
from socket import *
import subprocess

# Funciton that send small amounts of information
def sendInfo(connectionSocket, info):
    info = info.encode('ASCII')

    bytesSent = 0

    while bytesSent != len(info):
        bytesSent += connectionSocket.send(info[bytesSent:])


# Function to receive the commmand from the client,
# we don't really need to loop for the amount of bytes
# to receive because each command is about less then 4 bytes long
def recInfo(connectionSocket, numBytes):
	recvBuffer = ""
	tmpBuffer = ""
	temp = ""

	#receives the amount of bytes given
	tmpBuffer = connectionSocket.recv(numBytes)

	temp = tmpBuffer.decode('ASCII')

	recvBuffer += temp
	# print("Server executing command for ftp> " + recvBuffer + "\n")

	return recvBuffer

# Function that sends a file requested by the client, back to the client
def sendFile(filename):
    # Open the file
    fileObj = open(filename,"r")

    # The number of bytes sent
    numSent = 0
    # The file data
    fileData = None
    # Keep sending until all is sent
    while True:
	    # Read 65536 bytes of data
	    fileData = fileObj.read(65536)
	
	    # Make sure we did not hit EOF
	    if fileData:	
		    # Get the size of the data read
		    # and convert it to string
		    dataSizeStr = str(len(fileData))
		
		    # Prepend 0's to the size string
		    # until the size is 10 bytes
		    while len(dataSizeStr) < 10:
			    dataSizeStr = "0" + dataSizeStr

		    # Prepend the size of the data to the
		    # file data.
		    fileData = dataSizeStr + fileData	
		
		    # The number of bytes sent
		    numSent = 0
		
		    # Send the data!
		    while len(fileData) > numSent:
			    numSent += connectionSocket.send(fileData[numSent:])
	    # The file has been read. We are done
	    else:
		    break
    print "Sent ", numSent, " bytes.\n"
    
    # Close the socket and the file
    #clientSocket.close()
    fileObj.close()

# Function that receives all data that is sent
def recvAll(sock, numBytes):
	# The buffer
	recvBuff = ""
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	
	return recvBuff

# Function that will place the file reived on the server
def recvFile(connectionSocket):
	# The buffer to all data received from the
	# the client.
	fileData = ""
	
	# The size of the incoming file
	fileSize = 0	
	
	# The buffer containing the file size
	fileSizeBuff = ""
	
	# Receive the first 10 bytes indicating the
	# size of the file
	fileSizeBuff = recvAll(connectionSocket, 10)
		
	# Get the file size
	fileSize = int(fileSizeBuff)
	print "The file size is ", fileSize
	# Get the file data
	fileData = recvAll(connectionSocket, fileSize)

	fileObj = open("FileFromClient.txt", "w")
	fileObj.write(fileData)

	fileObj.close()
	print "The file data is: "
	print fileData

def lsCommand():
	data = str(subprocess.check_output(["ls", "-l",]))

	sendInfo(connectionSocket, data)
	



# The port on which to listen
serverPort = 12000

# Create a TCP socket
serverSocket = socket(AF_INET,SOCK_STREAM)

# Bind the socket to the port
serverSocket.bind(('', serverPort))

# Start listening for incoming connections
serverSocket.listen(1)
print "The server is ready to receive...\n"

commandRec = ""

#accept a connection; get client's socket
connectionSocket, addr = serverSocket.accept()

#Forever accept incoming connections
while 1:
	commandRec = recInfo(connectionSocket, 4) # test to recv command; generally commands are not more than 10 bytes

	if commandRec == "get":
		print("Server executing command for ftp> " + commandRec + "\n")
		nameOfFile = recInfo(connectionSocket, 20)
		print("Sending file " + nameOfFile + " to the client.\n")
		sendFile(nameOfFile)
		print("Success.\n")
	elif commandRec == "put":
		print("Server executing command for ftp> " + commandRec + "\n")
		recvFile(connectionSocket)
		print("Success.\n")
	elif commandRec == "ls":
		print("Server executing command for ftp> " + commandRec + "\n")
		lsCommand()
		print("Success.\n")
	elif commandRec == "quit": # if quit then we will close stop listening to the server socket and force ourselves out of the loop
		break

print("\nQuit initiated.\nStop server from listening.")
#close the socket	
connectionSocket.close()
