from struct import unpack, pack
import socket

serverIP     = "127.0.0.1"
serverPort   = 9876
bufferSize  = 1024

#msgFromServer       = "Hello UDP Client"
#bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((serverIP, serverPort))

DynAddressPort   = ("127.0.0.2", 9877)

print("UDP server up and listening.\n")
print("Waiting client message...\n")

def generateMVValue(value):
    return (value*359.9) / 100.0

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    print(address)
    
    # Luminosity percentage
    PV_value = unpack('f', message)[0]
    
    # Open angle
    MV_value = generateMVValue(PV_value)
    angle = pack('f', MV_value)
    
    print('PV_value',PV_value)
    print('MV_value', MV_value)
    UDPServerSocket.sendto(angle, DynAddressPort)



    