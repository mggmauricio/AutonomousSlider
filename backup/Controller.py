# 1. Confirmação de recebimento
# 2. Latencia da mensagem
# 3. Indentificador de mensagem

from struct import unpack, pack
import sys
import socket
import traceback
import signal
import datetime

from Protocol import * 

# Lendo o teclado para encerrar o servidor
signal.signal(signal.SIGINT, lambda: exit(1))

def sendMVValueToActuator(value):
    UDPSocketServer.sendto(value, ("255.255.255.255", serverPort))


def goToSafeFailState():
    print("Conduzindo a planta para o estado seguro ({}º) - {}".format(safeAngle, getNowISODate()))
    sendMVValueToActuator(safeAngle)


try:
    # Instanciando Servidor
    UDPSocketServer = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_DGRAM)
    print('Servidor Instanciado - ' + getNowISODate())

    # Configurando servidor para Broadcast
    UDPSocketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    UDPSocketServer.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bindando o servidor no IP e porta especificados
    UDPSocketServer.bind((serverIP, serverPort))
    print("Servidor configurado no IP {} e porta {} - {}".format(serverIP,
          serverPort, getNowISODate()))

except ValueError:
    print('Erro ao configurar e instanciar servidor.', ValueError)
    sys.exit()


def generateMVValue(value):
    return (value*359.9) / 100.0


availableActions = {
    1: lambda data: print("Mensagem do SENSOR", data)
}
# Iniciando Loop Principal
while(True):
    try:
        action, address = listenUDP(UDPSocketServer)
        print("Received Action", action)

        if action in availableActions:
            message, address = listenUDP(UDPSocketServer)
            value = unpack('f', message)[0]
            print("Received value", value)
            availableActions[action](value)

        # if(message != None):

        #     # Luminosity percentage
        #     # PV_value = unpack('f', message)[0]
        #     # print("Mensagem recebida de {}: {}".format(address, PV_value))

        #     # print("Enviando confirmação do recebimento da mensagem.")
        # else:
        #     print("Erro ao recebimento da mensagem.")

        # # Open angle
        # MV_value = generateMVValue(PV_value)
        # generatedAngle = pack('f', MV_value)

        # print('PV_value', PV_value)
        # print('MV_value', MV_value)
        # sendMVValueToActuator(generatedAngle)

    except (KeyboardInterrupt, SystemExit):
        raise

    except:
        traceback.print_exc()
