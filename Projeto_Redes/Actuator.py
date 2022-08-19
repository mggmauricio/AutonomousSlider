import socket
from struct import unpack
from time import sleep
import PyDynamixel_v2 as pd

from Protocol import *

# Criando conexão UDP
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Conectando servidor a porta e endereço fornecidos pelo protocolo
UDPServerSocket.bind((serverIP, dynamixelPort))
print("Servidor UDP do atuador online - {}.\n".format(getNowISODate()))

try:
    print("Instanciando comunicação com o atuador:")
    # Criando interface Dynamixel com uso da biblioteca PyDynamixel_v2
    DynSerial = pd.DxlComm(port='COM4', baudrate=57600)

    # Instancia do atuador
    actuator = pd.Joint(servo_id=12)

    # Atribuindo atuadores aos motores funcionais
    DynSerial.attach_joints([actuator])

    # Habilitar o torque do motor
    actuator.enable_torque()
    print("Atuador conectado com sucesso - {}\n".format(getNowISODate()))
except:
    print("Erro ao iniciar comunicação com atuador - Verifique se o Atuador está devidamente conectado ao sistema")
    exit(1)

while True:
    try: 
        message, address = UDPServerSocket.recvfrom(bufferSize)
        mv_value = unpack('f', message)[0]
        print('MV_value - Angulo definido pelo servidor de controle recebido:', mv_value)
        actuator.send_angle(mv_value)
        print('Posição do atuador atualizada para {}º\n'.format(mv_value))
        
    except (KeyboardInterrupt, SystemExit):
        print("Funcionamento interrompido manualmente.")
        raise exit(1)

    except:
        print("Erro na comunicação (FALHA NA COMUNICAÇÃO).\n Enviando planta para o estado seguro\n")
        sa = unpack('f', safeAngle)[0]
        actuator.send_angle(sa)
        sleep(1)

