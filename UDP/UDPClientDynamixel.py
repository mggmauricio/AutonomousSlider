import socket
from struct import unpack
import PyDynamixel_v2 as pd

serverIP     = "127.0.0.2"
serverPort   = 9877
bufferSize  = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((serverIP, serverPort))

print("UDP server up and listening.\n")
print("Waiting client message...\n")

DynSerial = pd.DxlComm(port='/dev/ttyUSB0', baudrate=57600)
actuator = pd.Joint(servo_id=12)

DynSerial.attach_joints([actuator])
print(DynSerial.joint_ids)
actuator.enable_torque()



# def setActuatorAngle():
#     print(actuator.get_angle())
    
    
# setActuatorAngle()    


while True:
    msgFromServer = UDPServerSocket.recvfrom(bufferSize)
    mv_value = unpack('f', msgFromServer[0])[0]
    print('mv_value', mv_value)
    actuator.send_angle(mv_value)

