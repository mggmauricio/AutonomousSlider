from time import sleep
import PyDynamixel_v2 as pd
import serial

from math import pi

DynSerial = pd.DxlComm(port='/dev/ttyUSB0', baudrate=57600)
joint1 = pd.Joint(servo_id=12)
#joint2 = pd.Joint(servo_id)


DynSerial.attach_joints([joint1])
print(DynSerial.joint_ids)
joint1.enable_torque()


joint1.send_angle(0)
sleep(1)
joint1.send_angle(90)
sleep(1)
joint1.send_angle(180)
sleep(1)
joint1.send_angle(359.9)
sleep(1)
# joint1.send_angle(720)


# ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
# print(ser.readline())

# def getSensorData(value):
#     return ((value + 1) * 1023) / 100

# while(True):
#     sensor = bytes(ser.readline())
#     # for i in sensor:
#     print('sensor', sensor)
#     withoutInit = sensor.split("b'")[1]
#     cleanValue = withoutInit.split('\r')
#     print("cleanValue", cleanValue)

#     # sensorValue = getSensorData(cleanValue)
#     print("Sensor Percentage", sensor)

