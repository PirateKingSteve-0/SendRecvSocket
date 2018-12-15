#Clientcode
from socket import *
from ftplib import FTP

def setFTP():
    print("Logging in...")
    ftp = FTP('ftp.cwi.nl')
    ftp.login()
    print("Login successful")
    #this can be changed depending on the machine
    ftp.cwd('/Macintosh HD/Users/pirateking/Gitfolder/project471')

def grabFile():
    filename = 'TheFile.txt'
    localfile = open(filename, 'wb')
    ftp.retrbinary('RETR' + filename, localfile.write, 1024)
    ftp.quit()
    localfile.close()

def placeFile():
    filename = 'Filed.txt'
    ftp.storbinary('STOR' + filename, open(filename, 'rb'))
    ftp.quit()

print ("Test 1")

# Name and port number of the server to 
# which want to connect .
serverName = '127.0.0.1' #local machine
serverPort = 12000

# Create a socket
clientSocket = socket(AF_INET, SOCK_STREAM) #SOCKSTREAM indicates a TCP stream
  
print ("Test 2")  

# Connect to the server
clientSocket.connect((serverName, serverPort))

print ("Test 3")

# A string we want to send to the server
data = "Hello world! This isaverylongstring."


bytesSent = 0 # keeps track of how many bytes are sent

#keep sending bytes until all bytes are sent
while bytesSent != len(data): #do until bytesSent = length of data
    # Send that string! 
    # Send returns the number of bytes it has send.
    # Data[bytesSent:] will return all bytes that come after the 
    #   the first bytesSent bytes of data. Resumes where left off.
    bytesSent += clientSocket.send(data[bytesSent:])
    print("Stuck")

# Close the socket
clientSocket.close()