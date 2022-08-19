from datetime import datetime
import signal
import socket
from struct import unpack
from time import sleep
import PyDynamixel_v2 as pd
import numpy as np


def getNowISODate():
    return datetime.now().isoformat()


serverIP = ""
serverPort = 5555
bufferSize = 1024

stepAngleSize = 5

# Create a datagram socket
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPClientSocket.bind((serverIP, serverPort))
# print("Servidor configurado no IP {} e porta {} - {}".format(serverIP,
#                                                              serverPort, getNowISODate()))

DynSerial = pd.DxlComm(port='COM4', baudrate=57600)
actuator = pd.Joint(servo_id=12)

DynSerial.attach_joints([actuator])
print(DynSerial.joint_ids)
actuator.enable_torque()


def handler():
    exit(1)


signal.signal(signal.SIGINT, handler)


def updateActuatorAngleTo(value):
    actualAngle = actuator.get_angle()
    diffAngle = value - actualAngle
    print("diffAngle", diffAngle)
    print("Actual Angle", actualAngle)
    stepAngle = np.arange(
        actualAngle, (diffAngle + actualAngle), stepAngleSize)
    print("stepAngle", stepAngle)
    if len(stepAngle) >= 2:
        print("Sended Angle: ", stepAngle[1])
        actuator.send_angle(stepAngle[1])
        # sleep(0.05)

while True:
    message, address = UDPClientSocket.recvfrom(1024)
    UDPClientSocket.sendto(message, address)
    print("Actuator", message, address)
    # mv_value = unpack('f', message)[0]

    # print("Message", message)
    # print("Origem", address)

    # print('mv_value', mv_value)
    # updateActuatorAngleTo(mv_value)
    sleep(1)
