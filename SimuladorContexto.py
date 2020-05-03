from datetime import date, timedelta
from enum import Enum
from time import sleep
import json
import geopy.distance


class LOCALIZACAO(Enum):
    CASA = "CASA"
    TRABALHO = "TRABALHO"

#SIMULA O MONITORAMENTO MINUTO A MINUTO
def simulaContexto(tp_perfil, informacao):

    if tp_perfil ==1:
        print("Monitorando Morador tonozeleira: {}".format(informacao))

        return True

    elif tp_perfil ==2:
        #O QUE FAZER: SIMULAR O CONTEXTO DE DA TURISTA ANDANDO PELA CIDADE ATÉ QUE ELA COMECE A ENTRAR NO BAIRRO RB
        x_base = -30.005656
        y_base = -51.091559
        print('Monitorando Turista por 20 minutos...')
        for w in range(20):
            x_base = x_base + 0.000200
            y_base = y_base + 0.000010

            x = "%.6f" % x_base
            y = "%.6f" % y_base

            print("Minuto {}: {}, {}".format((w+1), x, y))
            sleep(1.0)

            if float(x) == -30.001656 and float(y) == -51.091359:
                return True

#O QUE FAZER? SIMULAR O CONTEXTO PARA O AGRESSOR APROXIMANDO-SE DA VITIMA
DIAS = [
    'Segunda-feira',
    'Terça-feira',
    'Quarta-feira',
    'Quinta-Feira',
    'Sexta-feira',
    'Sábado',
    'Domingo'
]

def isHorarioComercial(horario):
    if 8 <= horario <= 17:
        return True
    else:
        return False

#traduz os dias da semana
def verificaLocalVitima(data):
    DIAS = [
    'Segunda-feira',
    'Terça-feira',
    'Quarta-feira',
    'Quinta-Feira',
    'Sexta-feira',
    'Sábado',
    'Domingo']

    data_e_hora_em_texto = data.strftime('%d/%m/%Y %H:%M')
    dia = data_e_hora_em_texto[0:2]
    mes = data_e_hora_em_texto[3:5]
    ano = data_e_hora_em_texto[6:10]
    hora = data_e_hora_em_texto[11:13]
    minuto = data_e_hora_em_texto[14:16]

    data = date(year=int(ano), month=int(mes), day=int(dia))

    #o dia da semana vai de 0 a 6 sendo 0 segunda-feira e 6 domingo
    if data.weekday() <= 4 and isHorarioComercial(int(hora)):
        print("Dia {} - {}. Pelo histórico de contexto a Morador_1 está no {}.".format(data_e_hora_em_texto, DIAS[data.weekday()],LOCALIZACAO.TRABALHO.value))
    else:
        print("Dia {} - {}. Pelo histórico de contexto a Morador_1 está em {}.".format(data_e_hora_em_texto, DIAS[data.weekday()],LOCALIZACAO.CASA.value))


def get_id_proprietario_veiculo(lista_veiculos, placa_pesquisa):
    for carro in lista_veiculos:

        carrega_carro = json.loads(carro)
        placa = carrega_carro['placa']
        proprietario = carrega_carro['proprietario']

        #LIMPANDO A STRING E APLICANDO SPLIT PARA CONSEGUIR O ID DO PROPRIETARIO DO CARRO
        id_proprietario_carro = proprietario.replace('{','').replace('}','').split(':')[1]
        if placa == placa_pesquisa:
            return int(id_proprietario_carro)

def get_proprietario_placa_veiculo(lista_nodos_pessoais, placa):
    for nodo in lista_nodos_pessoais:
        carrega_nodo = json.loads(nodo)
        id_nodo_pessoal = carrega_nodo['id_nodo_pessoal']

        if id_nodo_pessoal == get_id_proprietario_veiculo(lista_veiculos, placa):
           return carrega_nodo['nome']

def get_camera_veiculo(lista_cameras):
    placa_monitorada = "IZA-8J32"
    for x in lista_cameras:
        carrega_camera = json.loads(x)
        latitude_cam = carrega_camera['lat']
        longitude_cam = carrega_camera['lon']
        XY1 = ("-30.027336", "-51.175452")#coordenadas tornozeleira Morador_2
        XY2 = (latitude_cam, longitude_cam)#coordenadas cam
        dist_entre_nodo1_e_nodo2 = '{0:.1f}'.format(geopy.distance.vincenty(XY1, XY2).m)
        #COMO A DISTANCIA DEFINIDA PARA MARIA DA PENHA É DE 500M, SÓ ME INTERESSA ESSAS CAMERAS
        if float(dist_entre_nodo1_e_nodo2) <= 501.0:
            print("A {} visualizou o veículo {} pertencente ao {} a {} metros.".
                  format(carrega_camera['nome'], placa_monitorada,
                         get_proprietario_placa_veiculo(lista_nodos, placa_monitorada)
                         ,dist_entre_nodo1_e_nodo2))
