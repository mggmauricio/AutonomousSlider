from struct import unpack, pack
import socket
from time import sleep
from Protocol import *

# Create a datagram socket
UDPSocketServer = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPSocketServer.bind((serverIP, serverPort))
print("Servidor de Controle online - {}".format(getNowISODate()))

while(True):
    try:
        bytesAddressPair = UDPSocketServer.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        
        # Porcentagem de luminosidade recebida do Sensor
        PV_value = unpack('f', message)[0]
        print('PV_value - Leitura do sensor (em % de luminosidade):',PV_value)
        
        # Calculo do angulo de abertura
        MV_value = generateMVValue(PV_value)
        print('MV_value - Angulo de abertura (em º) definido pelo controlador:', MV_value)
        angle = pack('f', MV_value)
        
        try:
            UDPSocketServer.sendto(angle, (serverIP, dynamixelPort))
            print('Enviando MV_value para o atuador - {}.\n'.format(getNowISODate()))
        except:
            print("Erro ao se comunicar com o atuador. FALHA NA CONEXÃO \nTentando novamente em 1s.\n")
    
        sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Funcionamento interrompido manualmente.")
        raise exit(1)

    except:
        print("Erro na comunicação. Enviando Atuador para o estado seguro.")
        angle = pack('f', safeAngle)
        UDPSocketServer.sendto(angle, ActuatorAddressPort)
        sleep(1)



    