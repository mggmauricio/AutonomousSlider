import socket
from time import sleep
import serial
from struct import unpack, pack

# Pegando dados do protocolo estabelecido
from Protocol import *

# Criando cliente UDP
UDPSocketClient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

try:
    # Criando interface serial com o Arduino
    serialArduino = serial.Serial('COM5', 9600, timeout=1)
except:
    print("Erro ao iniciar servidor: Comunicação com o Arduino não pode ser estabelecida")
    exit(1)

# Função que transforma uma leitura digital com resolução de 0 a 1024 em um valor
# de porcentagem que representa a luminosidade do ambiente.


def getSensorData(value):
    return ((value + 1) * 100) / 1024.0


# Limpa o buffer antes de iniciar o looping principal
serialArduino.flush()

while(True):
    try: 
        print('Lendo comunicação do Arduino. Numero de bytes: {}'.format(
            serialArduino.in_waiting))

        # Caso tenhamos recebido 4 bytes do Arduino, temos um Float completo
        # que representa nosso PV_Value e podemos enviar este para o controlador.
        if(serialArduino.in_waiting == 4):
            # Lendo os dados do serial
            sensorData = serialArduino.read(4)

            # Transformando de bytes para float
            read_value = unpack('f', sensorData)[0]
            print('Valor recebido do Arduino: {}'.format(read_value))
            pv_value = getSensorData(read_value)
            print('Valor (em porcentagem) de luminosidade atual da planta: {}'.format(pv_value))

            # Transformando valor float para bytes e enviar para o servidor o PV_Value
            sendFloatUDPBroadcast(UDPSocketClient, pv_value)
            print('Enviando float com o valor do Sensor via UDP', getNowISODate(), '\n')

        # Caso o buffer esteja enchendo, limpamos a fila para retornar o estado de leitura inicial
        elif serialArduino.in_waiting > 4:
            serialArduino.read_all()
            serialArduino.flush()

        # Controle do ciclo de 1 segundo
        sleep(1)
        
    except (KeyboardInterrupt, SystemExit):
        print("Funcionamento interrompido manualmente.")
        raise exit(1)

    except:
        print("Erro na comunicação (FALHA NA COMUNICAÇÃO). Aguardando 1 segundo para tentar novamente.")
        sleep(1)
