from datetime import datetime
from struct import pack, unpack

# Parâmetros
safeAngle = 0

# Configurações do servidor
serverIP = "127.0.0.1"
serverPort = 5555
dynamixelPort = 5556
bufferSize = 1024

def listenUDP(UDP):
    # Recebe a mensagem
    message, address = UDP.recvfrom(bufferSize)

    # Confirma o recebimento
    # UDP.sendto(message, address)
    
    formatted = unpack('f', message)[0]

    return formatted, address
  
def sendFloatUDPBroadcast(UDP, data):
  value = pack('f', data)
  UDP.sendto(value, (serverIP, serverPort))
  
def getNowISODate():
    return datetime.now().isoformat()
  
def generateMVValue(value):
    return (value*359.9) / 100.0