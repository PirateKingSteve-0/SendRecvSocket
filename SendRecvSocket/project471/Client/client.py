#Clientcode
from socket import *
from ftplib import FTP

# Function to send the command over to the server 
def sendInfo(clientSocket, info):
    info = info.encode('ASCII')

    bytesSent = 0

    while bytesSent != len(info):
        bytesSent += clientSocket.send(info[bytesSent:])

# Function to receive the commmand from the client,
# we don't really need to loop for the amount of bytes
# to receive because each command is about less then 4 bytes long
def recInfo(clientSocket, numBytes):
	recvBuffer = ""
	tmpBuffer = ""
	temp = ""

	#receives the amount of bytes given
	tmpBuffer = clientSocket.recv(numBytes)

	temp = tmpBuffer.decode('ASCII')

	recvBuffer += temp
	# print("Server executing command for ftp> " + recvBuffer + "\n")

	return recvBuffer

# Function that will receive all the information sent from the server
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

# Function that will receive the information on the file being sent from the server
def getFile(clientSocket, fileName):
    	# The buffer to all data received from the
	# the client.
	fileData = ""
	
	# The size of the incoming file
	fileSize = 0	
	
	# The buffer containing the file size
	fileSizeBuff = ""
	
	# Receive the first 10 bytes indicating the
	# size of the file
	fileSizeBuff = recvAll(clientSocket, 10)
		
	# Get the file size
	fileSize = int(fileSizeBuff)
	print "The file size is ", fileSize
	# Get the file data
	fileData = recvAll(clientSocket, fileSize)

	fileObj = open(fileName, "w")
	fileObj.write(fileData)

	fileObj.close()
	print "The file data is: "
	print fileData

# Function that places the files the client has on the server
def putFile(clientSocket, nameOfFile):
    # Open the file
    fileObj = open(nameOfFile, "r")
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
			    numSent += clientSocket.send(fileData[numSent:])
	    # The file has been read. We are done
	    else:
		    break
    print "Sent ", numSent, " bytes."
    
    # Close the socket and the file
    #clientSocket.close()
    fileObj.close()


# Name and port number of the server to 
# which want to connect .
serverName = '127.0.0.1' #local machine
serverPort = 12000

print("Creating client socket...\n")
# Create a socket
clientSocket = socket(AF_INET, SOCK_STREAM) #SOCKSTREAM indicates a TCP stream

# Connect to the server
clientSocket.connect((serverName, serverPort))

# Display the list of ftp options for the user
print("ftp> get <file name> (downloads file <file name> from the server)")
print("ftp> put <filename> (uploads file <file name> to the server)")
print("ftp> ls (lists files on the server)")
print("ftp> quit (disconnects from the server and exits)")

ftpCommand = raw_input("Enter ftp command to execute: ")

# As long as the option is not to quit do these
while ftpCommand != "quit":

    if ftpCommand == "get":
        print("\nPrompting the server for ftp command > " + ftpCommand + "\n")
        sendInfo(clientSocket, ftpCommand)
        recvFileName = raw_input("Enter file name to receive from server: ")
        sendInfo(clientSocket, recvFileName)
        getFile(clientSocket, recvFileName)
        print("Success")
    elif ftpCommand == "put":
        print("\nPrompting the server for ftp command > " + ftpCommand + "\n")
        sendInfo(clientSocket, ftpCommand)
        nameOfFile = raw_input("Enter name of file to put on server: ")
        putFile(clientSocket, nameOfFile)
        print("Success")
    elif ftpCommand == "ls":
        print("\nPrompting the server for ftp command > " + ftpCommand + "\n")
        sendInfo(clientSocket, ftpCommand)
        lsInfo = recInfo(clientSocket, 1000)
        print(lsInfo)
        print("Success")
    else:
        print("\nCommand given was " + ftpCommand + ": this is not a valid command. Please re-enter command.\n")

    print("\nftp> get <file name> (downloads file <file name> from the server)")
    print("ftp> put <filename> (uploads file <file name> to the server)")
    print("ftp> ls (lists files on the server)")
    print("ftp> quit (disconnects from the server and exits)")
    ftpCommand = raw_input("Enter ftp command to execute: ")

# send the quit command to the server so it knows to also close the server socket
if ftpCommand == "quit":
    sendInfo(clientSocket, ftpCommand)
    print("\nDisconnecting from the client socket from the server")
# Close the socket
clientSocket.close()