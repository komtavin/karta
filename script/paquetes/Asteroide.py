#!/usr/bin/python
"""Modelo de los asteroides y puntos menores dentro de una carta astral."""


class Asteroide:
    """Representa un asteroide o punto menor del sistema solar en una carta astral.

    Cubre los cuerpos Ceres, Quirón, Palas, Juno, Vesta, Lilith (Apogeo Medio),
    Vertex y Eris. A diferencia de los planetas clásicos, no todos los asteroides
    tienen regencias establecidas; solo Ceres y Eris tienen dignidades definidas.

    Attributes:
        idAsteroide (str): Identificador en inglés tal como lo entrega swete64
            (ej. 'Chiron', 'mean Apogee').
        carta (Carta): Referencia a la carta astral que contiene este objeto.
        nombre (str): Nombre en español usado como clave interna.
        anguloGrado (str): Grados del ángulo, tal como llega de swete64.
        anguloMinuto (str): Minutos del ángulo.
        anguloSegundo (str): Segundos del ángulo.
        anguloReal (float): Ángulo en grados decimales dentro del signo.
        signo (Signo): Signo zodiacal en que se ubica el asteroide.
        sentido (str): Dirección de movimiento ('directo' | 'retrogrado').
        regenteVerdadero (Signo | str): Signo de domicilio verdadero.
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
        escalaPlatonico (float): Escala del sólido platónico en la animación.
    """

    def __init__(self, idAsteroide: str, anguloGrado: str, anguloMinuto: str,
                 anguloSegundo: str, signo, carta):
        """Inicializa el asteroide a partir de su identificador swete64.

        Args:
            idAsteroide: Nombre en inglés del asteroide ('Ceres', 'Chiron', etc.).
            anguloGrado: Grados del ángulo, como string.
            anguloMinuto: Minutos del ángulo, como string.
            anguloSegundo: Segundos del ángulo, como string.
            signo: Instancia de Signo correspondiente a la posición del asteroide.
            carta: Instancia de Carta que contiene este asteroide.
        """
        self.idAsteroide = idAsteroide
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
        """Asigna regencias, exaltación, caída y detrimento para Ceres y Eris.

        Solo Ceres y Eris tienen dignidades formalmente establecidas en la
        astrología moderna. Los demás asteroides no tienen dignidades asignadas.
        Las dignidades se registran bidireccionalmente: en el asteroide y en
        el signo correspondiente.
        """
        if self.idAsteroide == 'Ceres':
            self.regente = self.carta.getPunto('virgo')
            self.carta.getPunto('virgo').setRegente(self)
            self.coRegente = self.carta.getPunto('geminis')
            self.carta.getPunto('geminis').setCoRegente(self)
            self.detrimentoModerno = self.carta.getPunto('piscis')
            self.carta.getPunto('piscis').setDetrimentoModerno(self)
            self.exaltacion = self.carta.getPunto('geminis')
            self.carta.getPunto('geminis').setExaltacion(self)
            self.caida = self.carta.getPunto('sagitario')
            self.carta.getPunto('sagitario').setCaida(self)

        elif self.idAsteroide == 'Eris':
            self.regenteVerdadero = self.carta.getPunto('libra')
            self.carta.getPunto('libra').setRegente(self)
            self.regente = self.carta.getPunto('libra')
            self.coRegente = self.carta.getPunto('tauro')
            self.carta.getPunto('tauro').setCoRegente(self)
            self.detrimentoModerno = self.carta.getPunto('aries')
            self.carta.getPunto('aries').setDetrimentoModerno(self)
            self.exaltacion = self.carta.getPunto('sagitario')
            self.carta.getPunto('sagitario').setExaltacion(self)
            self.caida = self.carta.getPunto('geminis')
            self.carta.getPunto('geminis').setCaida(self)

    def setEntidadById(self) -> None:
        """Asigna el nombre interno y los atributos de animación según el id."""
        self.deltaAnguloCarta = 0.0
        self.anguloCarta = 0.0
        self.indiceOrbitaCarta = 0
        self.orbitaPosicional = 0.0
        self.orbitaAltura = 0.0
        self.escalaRuna = 0.0
        self.escalaPlatonico = 0.0

        nombres = {
            'Ceres':       'ceres',
            'Chiron':      'kiron',
            'Pallas':      'palas',
            'Juno':        'juno',
            'Vesta':       'vesta',
            'mean Apogee': 'lilith',
            'Vertex':      'vertex',
            'Eris':        'eris',
        }
        self.nombre = nombres[self.idAsteroide]

    def __getitem__(self, key: str):
        """Permite acceso a atributos mediante notación de diccionario.

        Args:
            key: Nombre del atributo.

        Returns:
            El valor del atributo correspondiente.
        """
        return getattr(self, key)
