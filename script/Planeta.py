#!/usr/bin/python
"""Modelo del planeta dentro de una carta astral."""


class Planeta:
    """Representa un planeta del sistema solar en una carta astral.

    Cubre los diez planetas clásicos y modernos: Sol, Luna, Mercurio, Venus,
    Marte, Júpiter, Saturno, Urano, Neptuno y Plutón.

    Las dignidades (regencia, co-regencia, exaltación, caída y detrimento)
    se registran bidireccionalmente: el planeta referencia al signo y el signo
    referencia al planeta. Esto permite navegar la carta en ambas direcciones.

    Attributes:
        idPlaneta (str): Identificador en inglés tal como lo entrega swete64
            (ej. 'Sun', 'Moon', 'Mercury').
        carta (Carta): Referencia a la carta astral que contiene este planeta.
        nombre (str): Nombre en español usado como clave interna.
        anguloGrado (str): Grados del ángulo eclíptico, tal como llega de swete64.
        anguloMinuto (str): Minutos del ángulo.
        anguloSegundo (str): Segundos del ángulo.
        anguloReal (float): Ángulo en grados decimales dentro del signo.
        signo (Signo): Signo zodiacal en que se ubica el planeta.
        sentido (str): Dirección de movimiento observable ('directo' | 'retrogrado').
        regenteVerdadero (Signo | str): Signo de domicilio esencial.
        regente (Signo | str): Signo regente principal.
        coRegente (Signo | str): Signo co-regente.
        detrimentoModerno (Signo | str): Signo de detrimento moderno.
        exaltacion (Signo | str): Signo de exaltación.
        caida (Signo | str): Signo de caída.
        deltaAnguloCarta (float): Delta de movimiento respecto a la carta anterior.
        anguloCarta (float): Distancia total recorrida hasta la carta actual.
        indiceOrbitaCarta (int): Índice de órbita utilizada en la animación.
        orbitaPosicional (float): Distancia radial en la escena 3D.
        orbitaAltura (float): Altura axial en la escena 3D.
        escalaRuna (float): Escala de la runa en la animación.
    """

    def __init__(self, idPlaneta: str, anguloGrado: str, anguloMinuto: str,
                 anguloSegundo: str, signo, carta):
        """Inicializa el planeta a partir de su identificador swete64.

        Args:
            idPlaneta: Nombre en inglés del planeta ('Sun', 'Moon', etc.).
            anguloGrado: Grados del ángulo eclíptico, como string.
            anguloMinuto: Minutos del ángulo, como string.
            anguloSegundo: Segundos del ángulo, como string.
            signo: Instancia de Signo correspondiente a la posición del planeta.
            carta: Instancia de Carta que contiene este planeta.
        """
        self.idPlaneta = idPlaneta
        self.carta = carta
        self.anguloGrado = anguloGrado
        self.anguloMinuto = anguloMinuto
        self.anguloSegundo = anguloSegundo
        self.signo = signo
        self.regenteVerdadero = ''
        self.regente = ''
        self.coRegente = ''
        self.detrimentoModerno = ''
        self.exaltacion = ''
        self.caida = ''
        self.sentido = ''
        self.setEntidadById()
        self.setAnguloReal()

    def setAnguloReal(self) -> None:
        """Calcula el ángulo en grados decimales dentro del signo."""
        self.anguloReal = (
            int(self.anguloGrado)
            + int(self.anguloMinuto) / 60
            + float(self.anguloSegundo) / 3600
        )

    def setDignidades(self) -> None:
        """Asigna regencias, exaltación, caída y detrimento del planeta.

        Las dignidades se registran bidireccionalmente en el planeta y en
        cada signo afectado. Se usan las correspondencias de la astrología
        moderna (incluye Urano, Neptuno y Plutón como regentes modernos).
        """
        dignidades = {
            'Sun': {
                'regenteVerdadero': 'leo',
                'regente':          'leo',
                'coRegente':        'cancer',
                'detrimentoModerno':'aquario',
                'exaltacion':       'aries',
                'caida':            'libra',
            },
            'Moon': {
                'regenteVerdadero': 'cancer',
                'regente':          'cancer',
                'coRegente':        'leo',
                'detrimentoModerno':'capricorneo',
                'exaltacion':       'tauro',
                'caida':            'escorpio',
            },
            'Mercury': {
                # Mercurio tiene dos domicilios verdaderos: Géminis y Virgo
                'regenteVerdadero': 'virgo',
                'regente':          'geminis',
                'coRegente':        'virgo',
                'detrimentoModerno':'aquario',
                'exaltacion':       'aries',
                'caida':            'libra',
            },
            'Venus': {
                'regenteVerdadero': 'tauro',
                'regente':          'tauro',
                'coRegente':        'libra',
                'detrimentoModerno':'escorpio',
                'exaltacion':       'piscis',
                'caida':            'virgo',
            },
            'Mars': {
                'regenteVerdadero': 'aries',
                'regente':          'aries',
                'coRegente':        'escorpio',
                'detrimentoModerno':'libra',
                'exaltacion':       'capricorneo',
                'caida':            'cancer',
            },
            'Jupiter': {
                'regenteVerdadero': 'sagitario',
                'regente':          'sagitario',
                'coRegente':        'piscis',
                'detrimentoModerno':'geminis',
                'exaltacion':       'cancer',
                'caida':            'capricorneo',
            },
            'Saturn': {
                'regenteVerdadero': 'capricorneo',
                'regente':          'capricorneo',
                'coRegente':        'aquario',
                'detrimentoModerno':'cancer',
                'exaltacion':       'libra',
                'caida':            'aries',
            },
            'Uranus': {
                'regenteVerdadero': 'aquario',
                'regente':          'aquario',
                'coRegente':        'capricorneo',
                'detrimentoModerno':'leo',
                'exaltacion':       'escorpio',
                'caida':            'tauro',
            },
            'Neptune': {
                'regenteVerdadero': 'piscis',
                'regente':          'piscis',
                'coRegente':        'sagitario',
                'detrimentoModerno':'virgo',
                'exaltacion':       'leo',
                'caida':            'aquario',
            },
            'Pluto': {
                'regenteVerdadero': 'escorpio',
                'regente':          'escorpio',
                'coRegente':        'aries',
                'detrimentoModerno':'tauro',
                'exaltacion':       'aquario',
                'caida':            'leo',
            },
        }

        d = dignidades[self.idPlaneta]
        self.regenteVerdadero = self.carta.getPunto(d['regenteVerdadero'])
        self.carta.getPunto(d['regenteVerdadero']).setRegente(self)
        self.regente = self.carta.getPunto(d['regente'])
        self.carta.getPunto(d['regente']).setRegente(self)
        self.coRegente = self.carta.getPunto(d['coRegente'])
        self.carta.getPunto(d['coRegente']).setCoRegente(self)
        self.detrimentoModerno = self.carta.getPunto(d['detrimentoModerno'])
        self.carta.getPunto(d['detrimentoModerno']).setDetrimentoModerno(self)
        self.exaltacion = self.carta.getPunto(d['exaltacion'])
        self.carta.getPunto(d['exaltacion']).setExaltacion(self)
        self.caida = self.carta.getPunto(d['caida'])
        self.carta.getPunto(d['caida']).setCaida(self)

    def setEntidadById(self) -> None:
        """Asigna el nombre interno y los atributos de animación según el id del planeta."""
        self.deltaAnguloCarta = 0.0
        self.anguloCarta = 0.0
        self.indiceOrbitaCarta = 0
        self.orbitaPosicional = 0.0
        self.orbitaAltura = 0.0
        self.escalaRuna = 0.0

        nombres = {
            'Sun':     'sol',
            'Moon':    'luna',
            'Mercury': 'mercurio',
            'Venus':   'venus',
            'Mars':    'marte',
            'Jupiter': 'jupiter',
            'Saturn':  'saturno',
            'Uranus':  'urano',
            'Neptune': 'neptuno',
            'Pluto':   'pluton',
        }
        self.nombre = nombres[self.idPlaneta]

    def __getitem__(self, key: str):
        """Permite acceso a atributos mediante notación de diccionario.

        Args:
            key: Nombre del atributo.

        Returns:
            El valor del atributo correspondiente.
        """
        return getattr(self, key)
