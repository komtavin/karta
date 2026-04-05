#!/usr/bin/python
"""Motor de consulta a swete64 y construcción del modelo orientado a objetos de la carta astral."""

import subprocess
import re
import math
import calendar

from pytz import timezone
from datetime import datetime

from Carta import Carta
from Planeta import Planeta
from Casa import Casa
from Punto import Punto
from Asteroide import Asteroide


class Query:
    """Ejecuta swete64, parsea su salida tabular y construye las cartas astrales.

    El flujo de trabajo es:
    1. ``__init__``: recibe los parámetros de la consulta y calcula fechas y pasos.
    2. ``obtener()``: ejecuta swete64 dos veces (query completa y ventana principal)
       y almacena las matrices de texto.
    3. ``procesar()``: parsea las matrices y construye las listas de objetos OO.

    swete64 produce una salida tabular donde cada bloque de 39 filas representa
    una carta astral. Los campos se separan con el literal ``TABULADOR``.

    Attributes:
        ruta (str): Ruta al ejecutable swete64.exe en Windows.
        fechaLectura (str): Fecha de la carta principal en formato 'YYYY-MM-DD'.
        horaLectura (str): Hora local de la carta principal en formato 'HH:MM:SS'.
        longitud (str): Longitud geográfica en grados decimales.
        orientacionLongitud (str): 'E' o 'W'.
        latitud (str): Latitud geográfica en grados decimales.
        orientacionLatitud (str): 'N' o 'S'.
        algoritmo (str): Sistema de casas ('p' = Placidus).
        amplitud (int): Duración de cada paso en minutos.
        pasosExtra (int): Pasos adicionales antes y después de la ventana principal,
            equivalentes a medio día, para garantizar la detección de amanecer/atardecer.
        pasosLectura (int): Número de cartas de la ventana principal.
        pasosQuery (int): Total de pasos enviados a swete64 (extra + principal + extra).
        fechaPrincipal (str): Fecha UTC de inicio de la ventana principal (DD.MM.YYYY).
        horaPrincipal (str): Hora UTC de inicio de la ventana principal.
        fechaQuery (str): Fecha UTC de inicio de la consulta completa.
        horaQuery (str): Hora UTC de inicio de la consulta completa.
        matriz (str): Salida cruda de swete64 para la ventana principal.
        matrizQuery (str): Salida cruda de swete64 para la consulta completa.
        cartas (list[Carta]): Cartas de la ventana principal (usadas en la animación).
        cartasQuery (list[Carta]): Cartas de la consulta completa (usadas para
            detectar amanecer/atardecer y calcular retrogradaciones).
    """

    def __init__(self, fechaLectura: str, horaLectura: str, longitud: str,
                 orientacionLongitud: str, latitud: str, orientacionLatitud: str,
                 algoritmo: str, pasosLectura: str, deltaPaso: str, zonaHoraria: str):
        """Inicializa la consulta y calcula la ventana temporal de swete64.

        La consulta a swete64 necesita comenzar medio día antes de la carta
        principal para poder detectar el amanecer/atardecer previo. Por eso
        se calculan ``pasosExtra`` y se retrocede la fecha de inicio.

        Args:
            fechaLectura: Fecha de la carta en formato 'YYYY-MM-DD'.
            horaLectura: Hora local en formato 'HH:MM:SS'.
            longitud: Longitud geográfica en grados decimales (ej. '-70.6506').
            orientacionLongitud: 'E' o 'W'.
            latitud: Latitud geográfica en grados decimales (ej. '-33.4372').
            orientacionLatitud: 'N' o 'S'.
            algoritmo: Sistema de casas ('p' para Placidus).
            pasosLectura: Número de cartas a generar, en formato '-nN' (ej. '-n49').
            deltaPaso: Intervalo entre cartas en formato '-sXm' (ej. '-s30m').
            zonaHoraria: Nombre de zona horaria pytz (ej. 'America/Santiago').
        """
        self.ruta = 'D:\\karta\\efemerides\\swete64\\swete64.exe'
        #MAC#self.ruta = '/Users/komtavin/Desktop/Proyectos/rukaLab/karta/efemerides/swisseph-master/swetest'
        self.fechaLectura = fechaLectura
        self.horaLectura = horaLectura
        self.longitud = longitud
        self.orientacionLongitud = orientacionLongitud
        self.latitud = latitud
        self.orientacionLatitud = orientacionLatitud
        self.algoritmo = algoritmo
        self.pasosLectura = pasosLectura
        self.deltaPaso = deltaPaso
        self.setAmplitud()
        self.setPasos()
        self.setFecha(zonaHoraria)

    def setFecha(self, zonaHoraria: str) -> None:
        """Convierte la fecha/hora local a UTC y calcula el inicio de la consulta.

        Retrocede la fecha de inicio en ``pasosExtra * amplitud`` minutos para
        cubrir la ventana previa necesaria para detectar amanecer/atardecer.

        Args:
            zonaHoraria: Nombre de zona horaria pytz (ej. 'America/Santiago').
        """
        date_str = f'{self.fechaLectura} {self.horaLectura}'
        datetime_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

        datetime_obj_utc = datetime_obj.replace(
            tzinfo=timezone(zonaHoraria)
        ).isoformat()

        print(f'UTC: {datetime_obj_utc}')

        # Extraer offset de zona horaria y convertir a segundos
        signo_tz = datetime_obj_utc[19]
        offset_horas = int(datetime_obj_utc[20:22])
        tz = -offset_horas * 3600 if signo_tz == '+' else offset_horas * 3600

        segundos = tz + calendar.timegm((
            int(datetime_obj_utc[0:4]),
            int(datetime_obj_utc[5:7]),
            int(datetime_obj_utc[8:10]),
            int(datetime_obj_utc[11:13]),
            int(datetime_obj_utc[14:16]),
            0, 0, 0, 0
        ))

        dt_principal = str(datetime.utcfromtimestamp(segundos))
        partes_principal = re.split(r'[-\s]', dt_principal)
        self.fechaPrincipal = f'{partes_principal[2]}.{partes_principal[1]}.{partes_principal[0]}'
        self.horaPrincipal = dt_principal.split(' ')[1]

        # Retroceder la ventana para cubrir el medio día previo
        segundos_query = segundos - (self.pasosExtra * self.amplitud * 60)
        dt_query = str(datetime.utcfromtimestamp(segundos_query))
        partes_query = re.split(r'[-\s]', dt_query)
        self.fechaQuery = f'{partes_query[2]}.{partes_query[1]}.{partes_query[0]}'
        self.horaQuery = dt_query.split(' ')[1]

        print(f'Fecha lectura (HL): {self.fechaLectura} {self.horaLectura}')
        print(f'Fecha inicio query: {self.fechaQuery} {self.horaQuery}')
        print(f'Fecha principal:    {self.fechaPrincipal} {self.horaPrincipal}')

    def setAmplitud(self) -> None:
        """Extrae la amplitud de paso en minutos desde el parámetro deltaPaso."""
        self.amplitud = int(self.deltaPaso.replace('-s', '').replace('m', ''))

    def setPasos(self) -> None:
        """Calcula el número de pasos extra y el total de pasos para swete64.

        Los pasos extra equivalen a medio día de cobertura, lo que garantiza
        que siempre haya al menos un amanecer y un atardecer dentro de la
        ventana de la consulta.
        """
        multiplicador = 60 / self.amplitud
        self.pasosExtra = math.ceil((24 * multiplicador) / 2) + 1
        self.pasosLectura = int(self.pasosLectura.replace('-n', ''))
        self.pasosPrincipal = self.pasosLectura
        self.pasosQuery = self.pasosExtra + self.pasosLectura + self.pasosExtra

        print(f'Amplitud: {self.amplitud} min | Multiplicador: {multiplicador}')
        print(f'Pasos extra: {self.pasosExtra} | Pasos query: {self.pasosQuery}')

    def obtener(self) -> None:
        """Ejecuta swete64 dos veces y almacena la salida en texto plano.

        Primera ejecución: ventana completa (query) para detección de día/noche
        y cálculo de retrogradaciones.
        Segunda ejecución: ventana principal (las cartas que se animarán).
        """
        args_comunes = [
            f'-house{self.longitud},{self.latitud},{self.algoritmo}',
            '-fZPpT',
            '-head',
            '-g TABULADOR ',
            #MAC#'-gTABULADOR ', the 
            '-p0123456789mtAFDGHIs',
            '-xs136199',
        ]

        self.matrizQuery = self.cmd([
            self.ruta,
            f'-b{self.fechaQuery}',
            f'-ut{self.horaQuery}',
            *args_comunes,
            f'-n{self.pasosQuery}',
            self.deltaPaso,
        ]).rstrip()

        self.matriz = self.cmd([
            self.ruta,
            f'-b{self.fechaPrincipal}',
            f'-ut{self.horaPrincipal}',
            *args_comunes,
            f'-n{self.pasosPrincipal}',
            self.deltaPaso,
        ]).rstrip()

    def cmd(self, comando: list) -> str:
        """Ejecuta un comando de shell y devuelve su salida estándar.

        Args:
            comando: Lista de strings que forman el comando (compatible con
                ``subprocess.run``).

        Returns:
            Salida estándar del proceso como string.
        """
        print(f"COMANDO A EJECUTAR: {' '.join(comando)}")
        proceso = subprocess.run(
            comando,
            check=True,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        return proceso.stdout

    def procesar(self) -> None:
        """Parsea las matrices de texto y construye las listas de cartas OO."""
        self.cartas = []
        self.setCartas(self.cartas, self.matriz)
        self.cartasQuery = []
        self.setCartas(self.cartasQuery, self.matrizQuery)

    def setCartas(self, cartas: list, matriz: str) -> None:
        """Parsea la matriz tabular de swete64 y construye objetos Carta.

        Cada carta ocupa exactamente 39 filas en la salida de swete64.
        La primera columna de cada fila contiene los datos angulares del objeto
        (grado, signo, minuto, segundo), y la segunda columna el nombre del objeto.

        Args:
            cartas: Lista destino donde se añadirán las cartas construidas.
            matriz: Texto crudo de salida de swete64.
        """
        filas = re.split(r'\n', matriz)
        filas_por_carta = 39
        numero_cartas = int(len(filas) / filas_por_carta)

        for i in range(numero_cartas):
            inicio = i * filas_por_carta
            fin = inicio + filas_por_carta
            columnas_cabecera = re.split('TABULADOR', filas[inicio])
            carta = Carta(columnas_cabecera[3])
            cartas.append(carta)

            bloque = filas[inicio:fin]
            carta.setPuntos(
                self.setPuntos(bloque, 'planeta', carta),
                self.setPuntos(bloque, 'casa', carta),
                self.setPuntos(bloque, 'punto', carta),
                self.setPuntos(bloque, 'asteroide', carta),
            )
            carta.setDomicilios()
            carta.setDignidades()

    def setPuntos(self, filas: list, tipo: str, carta) -> list:
        """Parsea las filas de un bloque de carta y construye objetos del tipo indicado.

        Filtra las filas por el nombre del objeto en la segunda columna y
        construye la instancia correspondiente (Planeta, Casa, Punto o Asteroide).

        Args:
            filas: Lista de strings con las 39 filas de una carta.
            tipo: Tipo de objeto a extraer ('planeta', 'casa', 'punto', 'asteroide').
            carta: Instancia de Carta destino para los objetos construidos.

        Returns:
            Lista de objetos del tipo solicitado.
        """
        ids_por_tipo = {
            'planeta': {
                'Sun', 'Moon', 'Mercury', 'Venus', 'Mars',
                'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto',
            },
            'casa': {
                'house 1', 'house 2', 'house 3', 'house 4',
                'house 5', 'house 6', 'house 7', 'house 8',
                'house 9', 'house 10', 'house 11', 'house 12',
            },
            'punto': {'Ascendant', 'MC', 'mean Node', 'true Node'},
            'asteroide': {
                'Ceres', 'Chiron', 'Pallas', 'Juno', 'Vesta',
                'mean Apogee', 'Vertex', 'Eris',
            },
        }
        constructores = {
            'planeta':   Planeta,
            'casa':      Casa,
            'punto':     Punto,
            'asteroide': Asteroide,
        }

        ids_validos = ids_por_tipo[tipo]
        constructor = constructores[tipo]
        respuesta = []

        for fila in filas:
            columnas = re.split('TABULADOR', fila)
            columnas[0] = columnas[0].lstrip().replace('  ', ' ')
            columnas[1] = ' '.join(columnas[1].split())

            if columnas[1] in ids_validos:
                partes = self.getPartes(columnas[0])
                respuesta.append(constructor(
                    columnas[1],
                    partes[0],
                    partes[2].replace("'", ''),
                    partes[3],
                    carta.getSigno(partes[1]),
                    carta,
                ))

        return respuesta

    def getPartes(self, columna: str) -> list:
        """Parsea la columna angular de swete64 en sus componentes.

        El formato de swete64 es: ``'GG ss MM' SS.ssss'`` donde GG = grado,
        ss = abreviatura del signo, MM = minuto, SS.ssss = segundo decimal.

        Args:
            columna: String con el dato angular crudo (ej. '21 sc 16'18.9993').

        Returns:
            Lista de cuatro strings: [grado, signo, minuto, segundo].
        """
        columna = columna.strip()
        partes_comilla = re.split("'", columna)
        parte_izq = partes_comilla[0].strip().split()
        grado = parte_izq[0]
        signo = parte_izq[1]
        minuto = parte_izq[2]
        segundo = partes_comilla[1].strip().split()[0]
        return [grado, signo, minuto, segundo]

    def clonar(self, objetos: list) -> list:
        """Crea una copia superficial de una lista de objetos.

        Args:
            objetos: Lista de objetos a clonar.

        Returns:
            Nueva lista con las mismas referencias.
        """
        return list(objetos)
