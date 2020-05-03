''' SCRIPT QUE SIMULA O UFOLLOWER - Fabio Viegas - 14/04/2020 '''

import datetime
import json
import geopy.distance
from geopy.geocoders import Nominatim
from enum import Enum
import re
import Simulacao.SimuladorContexto as simulador
from time import sleep

placa_monitorada = "IZA-8J32"

ALERTA_UFOLLOWER_SEGURANCA_FEMINICIDIO = 'Atenção! O nodo pessoal do {} está infringindo medida legal contra o nodo pessoal da {}.' \
                          ' {} está a {}km da {}. Deslocar o {} para {}. '
ALERTA_UFOLLOWER_SEGURANCA_TURISTA = 'Atenção! O nodo pessoal do {} está prestes a entrar em um zona de risco {}. ' \
                                  'Para o bairro {} foram registradas {} ocorrências no último mês.'

'''INCLUI NODO PESSOAL PARA A SIMULACAO'''
lista_nodos_pessoais = []
def adicionaNodoPessoal(nodoPessoal):
    lista_nodos_pessoais.append(nodoPessoal)

#NODOS PESSOAIS:
nodo_1 = '{ "id_nodo_pessoal": 1, "perfil": "Morador",  "nome": "Morador_1", "genero": "Feminino", "lat": "-30.027336", ' \
         '"lon": "-51.175452", "med_prot_id": 2}'
adicionaNodoPessoal(nodo_1)

nodo_2 = '{ "id_nodo_pessoal": 2, "perfil": "Morador", "nome": "Morador_2", "genero": "Masculinho","lat": "-30.020953", ' \
         '"lon": "-51.173528", "tornozeleira_id": "TORNOZELEIRA001"}'
adicionaNodoPessoal(nodo_2)

nodo_3 = '{ "id_nodo_pessoal": 3, "perfil": "Morador", "nome": "Morador_3", "genero": "Feminino","lat": "-30.027336", ' \
         '"lon": "-51.175452"}'
adicionaNodoPessoal(nodo_3)

#turista entrando no bairro Rubem Berta
nodo_4 = '{ "id_nodo_pessoal": 4, "perfil": "Turista", "nome": "Turista_1", "genero": "Feminino","lat": "-30.001656", ' \
         '"lon": "-51.091359"}'
adicionaNodoPessoal(nodo_4)

#Agentes: nodo 5 mais perto do nodo 2 podendo atuar. Nodo 6, mais longe, não sendo notificado.
nodo_5 = '{ "id_nodo_pessoal": 5, "perfil": "Agente", "nome": "Agente_1", "genero": "Masculino","lat": "-30.028848",' \
         ' "lon": "-51.192653"}'
adicionaNodoPessoal(nodo_5)

nodo_6 = '{ "id_nodo_pessoal": 6, "perfil": "Agente", "nome": "Agente_2", "genero": "Masculino","lat": "-30.027176", ' \
         '"lon": "-51.206365"}'
adicionaNodoPessoal(nodo_6)

#turista 2: no centro de POA
nodo_7 = '{ "id_nodo_pessoal": 7, "perfil": "Turista", "nome": "Turista_2", "genero": "Masculino","lat": "-30.034505", ' \
         '"lon": "-51.231191"}'
adicionaNodoPessoal(nodo_7)

nodo_8 = '{ "id_nodo_pessoal": 8, "perfil": "Morador", "nome": "Morador_4", "genero": "Masculino","lat": "-29.921151", ' \
         '"lon": "-51.140146", "tornozeleira_id": "TORNOZELEIRA002"}'
adicionaNodoPessoal(nodo_8)

nodo_9 = '{ "id_nodo_pessoal": 9, "perfil": "Agente", "nome": "Agente_3", "genero": "Feminino","lat": "-30.034505", ' \
         '"lon": "-51.231191"}'
adicionaNodoPessoal(nodo_9)

nodo_10 = '{ "id_nodo_pessoal": 10, "perfil": "Turista", "nome": "Turista_3", "genero": "Masculino","lat": "-30.134919", ' \
         '"lon": "-51.231713"}'
adicionaNodoPessoal(nodo_10)

nodo_11 = '{ "id_nodo_pessoal": 11, "perfil": "Morador",  "nome": "Morador_5", "genero": "Feminino", "lat": "-30.020037", ' \
         '"lon": "-51.179350", "med_prot_id": 8}'
#adicionaNodoPessoal(nodo_11)

nodo_12 = '{ "id_nodo_pessoal": 12, "perfil": "Morador", "nome": "Morador_6", "genero": "Masculinho","lat": "-30.020037", ' \
         '"lon": "-51.179350"}'
adicionaNodoPessoal(nodo_12)

'''INCLUI CAMERAS PARA A SIMULACAO'''
lista_cameras = []
def adicionaNodoCamera(camera):
    lista_cameras.append(camera)

cam_1 = '{"id_cam_1":1, "lat": "-30.022822", "lon": "-51.175602", "nome":"Câmera 1"}'#R. Anita Garibaldi
adicionaNodoCamera(cam_1)
cam_2 = '{"id_cam_2":1, "lat": "-30.023472", "lon": "-51.176332", "nome":"Câmera 2"}'#R. Tomaz Gonzaga
adicionaNodoCamera(cam_2)
cam_3 = '{"id_cam_3":3, "lat": "-30.024930", "lon": "-51.175849", "nome":"Câmera 3"}' #R. 14 de Julho
adicionaNodoCamera(cam_3)
cam_4 = '{"id_cam_4":4, "lat": "-30.023054", "lon": "-51.196792", "nome":"Câmera 4"}'#Plínio Brasil Milano
adicionaNodoCamera(cam_4)
cam_5 = '{"id_cam_5":5, "lat": "-30.022459", "lon": "-51.189721", "nome":"Câmera 5"}'#24 de Outubro
adicionaNodoCamera(cam_5)

'''INCLUI CARROS PARA A SIMULACAO'''
lista_veiculos = []
def adiciona_veiculo(carro):
    lista_veiculos.append(carro)

carro_1 = '{"id_carro_1": 1, "placa": "IZA-8J32", "proprietario": "{id_nodo_pessoal: 2"}'
adiciona_veiculo(carro_1)
carro_2 = '{"id_carro_2": 2, "placa": "IJK-0A23", "proprietario": "{id_nodo_pessoal: 8"}'
adiciona_veiculo(carro_2)
carro_3 = '{"id_carro_3": 3, "placa": "IFF-9C00", "proprietario": "{id_nodo_pessoal: 11"}'
adiciona_veiculo(carro_3)



#10 BAIRROS MAIS PERIGOSOS
class BairroOco(Enum):
    CENTRO_HISORICO = 1490
    MOINHOS_VENTO = 20
    RUBEM_BERTA = 780
    RESTINGA = 600
    SARANDI = 700
    PARTENON = 470
    FORESTA = 300
    CIDADE_BAIXA = 591
    AZENHA = 538
    LOMBA_PINHEIRO = 518

class PERFIL(Enum):
    MORADOR = 1
    TURISTA = 2
    AGENTE = 3


'''VERIFICA A DISTANCIA ENTRE DUAS COORDENADAS'''
def verificaDistancia(coords1, coords2):
    return geopy.distance.vincenty(coords1, coords2).km

'''RETORNA O ENDERECO DADO UMA LOCALIZACAO'''
def devolveEnderecoLocalizacao(lat, lon):
    geolocator = Nominatim(user_agent="U'Follower")
    localizacao = geolocator.reverse(lat + "," + lon)
    return localizacao

'''RETORNA QUAL O AGENTE MAIS PRÓXIMO DE UM X,Y PARA ATENDER UMA OCORRENCIA'''
def verificaAgenteMaisPerto(agentes, XIndiciado, YIndiciado):
    for agente in agentes:
        coordenadasAgente = (agente["lat"], agente["lon"])
        coordenadasMedProt = (XIndiciado, YIndiciado)
        distancia = verificaDistancia(coordenadasAgente, coordenadasMedProt)
        if distancia < 3.0:#verifica qual agente está a menos de 3km
            return agente["nome"]

'''FORMATA A MENSAGEM QUE SERÁ ENVIADA EM CASO DE UMA ABORDAGEM PARA FEMINICIDIO'''
def formataAlertaUfollowerFeminicidio(nomeIndiciado, nomeVitima, distanciaEntreVitimaIndiciado, agenteMaisProximo, localizacaoIndiciado):
    print(ALERTA_UFOLLOWER_SEGURANCA_FEMINICIDIO.format(nomeIndiciado, nomeVitima, nomeIndiciado,
                                                        distanciaEntreVitimaIndiciado,
                                                        nomeVitima,
                                                        agenteMaisProximo,
                                                        localizacaoIndiciado))

'''RETORNA QUAL O GRAU DE PERICULOSIDADE DE UM BAIRRO DADO O NRO DE OCORRENCIAS NESSE BAIRRO NO ULTIMO MES'''
def verficarPericulosidadeBairro(nroOcorrenciasMes):
    periculosidade = ""
    if nroOcorrenciasMes <= 500:
        periculosidade = "Baixa"
    elif 500 < nroOcorrenciasMes <= 750:
        periculosidade = "Média"
    elif nroOcorrenciasMes > 750:
        periculosidade = "Alta"
    return periculosidade

'''FORMATA A MENSAGEM QUE SERÁ ENVIADA EM CASO DE TURISTA EM BAIRRO DE PERICULOSIDADE ALTA'''
def formataAlertaUfollowerTurista(nomeTurista, bairro, nroOcorrencias):
    periculosidade = verficarPericulosidadeBairro(nroOcorrencias)
    if simulador.simulaContexto(PERFIL.TURISTA.value, ''):
        print(ALERTA_UFOLLOWER_SEGURANCA_TURISTA.format(nomeTurista, periculosidade, bairro, nroOcorrencias))

'''VERIFICA QUAL ENTRE OS TURISTAS ESTA ENTRANDO EM UM BAIRRO DE PERICULOSIDADE ALTA'''
def verificaSituacaoTurista(turistas):
    for turista in turistas:
        localizacao = devolveEnderecoLocalizacao(turista["lat"] , turista["lon"])
        for ocorrenciasBairro in BairroOco:
            if re.search(localizacao.address[31:36], ocorrenciasBairro.name , re.IGNORECASE):
                formataAlertaUfollowerTurista(turista["nome"], ocorrenciasBairro.name, ocorrenciasBairro.value)

def getTimeCarregaSimulacao(tp_perfil):
    print("Carregando simulação para {}".format(tp_perfil))
    a = [".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
    for x in range(10):
        print(a[x], end="", flush=True)
        sleep(1.0)
    print()

#################################################################
def get_id_proprietario_veiculo(lista_veiculos, placa_monitorada):
    for carro in lista_veiculos:

        carrega_carro = json.loads(carro)
        placa = carrega_carro['placa']
        proprietario = carrega_carro['proprietario']

        #LIMPANDO A STRING E APLICANDO SPLIT PARA CONSEGUIR O ID DO PROPRIETARIO DO CARRO
        id_proprietario_carro = proprietario.replace('{','').replace('}','').split(':')[1]
        if placa == placa_monitorada:
            return int(id_proprietario_carro)

def get_proprietario_placa_veiculo(lista_nodos_pessoais, placa_monitorada):
    for nodo in lista_nodos_pessoais:
        carrega_nodo = json.loads(nodo)
        id_nodo_pessoal = carrega_nodo['id_nodo_pessoal']

        if id_nodo_pessoal == get_id_proprietario_veiculo(lista_veiculos, placa_monitorada):
           return carrega_nodo['nome']

def get_camera_veiculo(lista_cameras):
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
                         get_proprietario_placa_veiculo(lista_nodos_pessoais, placa_monitorada)
                         ,dist_entre_nodo1_e_nodo2))
#################################################################





med = 0;
tem_med_prot = {}
indiciado_med_prot = {}
lista_agentes = []
lista_turistas = []
for x in range(len(lista_nodos_pessoais)):
    carrega_json = json.loads(lista_nodos_pessoais[x])
    for z, y in carrega_json.items():
        if z == "med_prot_id":
            tem_med_prot = lista_nodos_pessoais[int(x)]
            med = y
        if z == "id_nodo_pessoal" and y == med :
         indiciado_med_prot = lista_nodos_pessoais[int(x)]

        if z == "perfil" and y == "Agente":
            y = json.dumps(carrega_json)
            x = json.loads(y)
            lista_agentes.append(x)

        if z == "perfil" and y == "Turista":
            y = json.dumps(carrega_json)
            x = json.loads(y)
            lista_turistas.append(x)


#PEGAR AS COORDENADAS DA MULHER VÍTIMA
tem_med_prot_JSON = json.loads(tem_med_prot)
lat1 = tem_med_prot_JSON["lat"]
lon1 = tem_med_prot_JSON["lon"]

#PEGAR AS COORDENADAS DO AGRESSOR
indiciado_med_prot_JSON = json.loads(indiciado_med_prot)
lat2 = indiciado_med_prot_JSON["lat"]
lon2 = indiciado_med_prot_JSON["lon"]
tornozeleira = indiciado_med_prot_JSON["tornozeleira_id"]

#BUSCANDO O ENDERECO DE ONDE ESTÁ O AGRESSOR DADO UM X,Y
geolocator = Nominatim(user_agent="U'Follower")
localizacao = devolveEnderecoLocalizacao(lat2, lon2)

#CALCULA A DISTANCIA ENTRE MULHER VÍTIMA E AGRESSOR
XY1 = (lat1, lon1)
XY2 = (lat2, lon2)
dist_entre_nodo1_e_nodo2 = '{0:.2f}'.format(geopy.distance.vincenty(XY1, XY2).km)

#VERIFICA QUAL O AGENTE ESTÁ MAIS PERTO
agenteMaisPerto = verificaAgenteMaisPerto(lista_agentes, lat2, lon2)

#SE A DISTANCIA ENTRE VITIMA E AGRESSOR FOR MENOR DO QUE 1KM ALERTAR
if float(dist_entre_nodo1_e_nodo2) < 1.0:
    getTimeCarregaSimulacao(PERFIL.MORADOR.name)
    simulador.verificaLocalVitima(datetime.datetime.now())
    if simulador.simulaContexto(PERFIL.MORADOR.value, tornozeleira):
        formataAlertaUfollowerFeminicidio(indiciado_med_prot_JSON["nome"], tem_med_prot_JSON["nome"],
                                          dist_entre_nodo1_e_nodo2, agenteMaisPerto, localizacao.address[0:42])
    print("________________FIM SIMULACAO FEMINICIDIO________________")

get_camera_veiculo(lista_cameras)
getTimeCarregaSimulacao(PERFIL.TURISTA.name)

#VERIFICA A SITUACAO DOS TURISTAS
verificaSituacaoTurista(lista_turistas)
