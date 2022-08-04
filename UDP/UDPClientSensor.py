import socket
from time import sleep
import serial
from struct import unpack, pack

serverAddressPort   = ("127.0.0.1", 9876)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

def getSensorData(value):
    return ((value + 1) * 100) / 1024.0

ser.flush()

while(True):
    print('ser.in_waiting', ser.in_waiting) 
    if(ser.in_waiting == 4):
        sensor = ser.read(4)
        print('Enviando float com o valor do Sensor via UDP')
        read_value = unpack('f', sensor)[0]
        percentage_value = getSensorData(read_value)
        pv_value = pack('f', percentage_value )
        UDPClientSocket.sendto(pv_value, serverAddressPort)   
        
    elif ser.in_waiting > 4:
        ser.flush()

    sleep(1)