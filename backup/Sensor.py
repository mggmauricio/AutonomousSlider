import signal
import socket, traceback
from time import sleep
import serial
from struct import unpack, pack
from Protocol import *

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.bind(('', serverPort))
# Criando Interface Serial com o Arduino
ser = serial.Serial('COM5', 9600, timeout=1)

def getSensorData(value):
    return ((value + 1) * 100) / 1024.0

ser.flush()

# signal.signal(signal.SIGINT, lambda: exit(1))
data = 1

while(True):
    print("Enviando", data)
    message, address = listenUDP(UDPClientSocket)
    sendFloatUDPBroadcast(UDPClientSocket, data)
    if message==data:
        print("Recebeu Confirmação")
        sendFloatUDPBroadcast(UDPClientSocket, 666)
        
    print("message")
    sleep(1)
    continue
    
    try:
        print('ser.in_waiting', ser.in_waiting)
        if(ser.in_waiting == 4):
            sensor = ser.read(4)
            UDPClientSocket.sendto(pack('s', 'sensor'), serverAddressPort)
            print('Enviando float com o valor do Sensor via UDP')
            read_value = unpack('f', sensor)[0]
            percentage_value = getSensorData(read_value)
            pv_value = pack('f', percentage_value)
            UDPClientSocket.sendto(pv_value, serverAddressPort) # Sending to server
            sleep(1)

        elif ser.in_waiting > 4:
            print("Flushing Buffer")
            ser.flush()
            ser.flushInput()
            ser.flushOutput()
            sleep(1)
            ser.read_all()
            print('After Flush', ser.in_waiting)

        else:
            sleep(1)

    except (KeyboardInterrupt, SystemExit):
        raise

    except:
        traceback.print_exc()
        
    
    
