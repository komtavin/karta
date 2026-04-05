#!/usr/bin/python
"""Modelo de puntos celestes sensibles dentro de una carta astral.

Los puntos sensibles son posiciones matemáticamente derivadas de la carta
(no cuerpos físicos): Ascendente, Medio Cielo, Nodo Norte, Nodo Sur y ARMC.
"""


class Punto:
    """Representa un punto sensible de la carta astral.

    A diferencia de los planetas, los puntos sensibles no son cuerpos físicos
    sino posiciones calculadas: Ascendente, Medio Cielo, Nodos Lunares y ARMC
    (Right Ascension of the Midheaven).

    Attributes:
        idPunto (str): Identificador en inglés tal como lo entrega swete64
            ('Ascendant', 'MC', 'mean Node', 'true Node', 'ARMC').
        carta (Carta): Referencia a la carta astral que contiene este punto.
        nombre (str): Nombre en español usado como clave interna.
        anguloGrado (str): Grados del ángulo, tal como llega de swete64.
        anguloMinuto (str): Minutos del ángulo.
        anguloSegundo (str): Segundos del ángulo.
        anguloReal (float): Ángulo en grados decimales dentro del signo.
        signo (Signo): Signo zodiacal en que se ubica el punto.
        sentido (str): Dirección de movimiento ('directo' | 'retrogrado').
        deltaAnguloCarta (float): Delta de movimiento respecto a la carta anterior.
        anguloCarta (float): Distancia total recorrida hasta la carta actual.
        indiceOrbitaCarta (int): Índice de órbita utilizada en la animación.
        orbitaPosicional (float): Distancia radial en la escena 3D.
        orbitaAltura (float): Altura axial en la escena 3D.
        escalaRuna (float): Escala de la runa en la animación.
    """

    def __init__(self, idPunto: str, anguloGrado: str, anguloMinuto: str,
                 anguloSegundo: str, signo, carta):
        """Inicializa el punto sensible a partir de su identificador swete64.

        Args:
            idPunto: Identificador en inglés ('Ascendant', 'MC', etc.).
            anguloGrado: Grados del ángulo, como string.
            anguloMinuto: Minutos del ángulo, como string.
            anguloSegundo: Segundos del ángulo, como string.
            signo: Instancia de Signo correspondiente a la posición del punto.
            carta: Instancia de Carta que contiene este punto.
        """
        self.idPunto = idPunto
        self.carta = carta
        self.anguloGrado = anguloGrado
        self.anguloMinuto = anguloMinuto
        self.anguloSegundo = anguloSegundo
        self.signo = signo
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

    def setEntidadById(self) -> None:
        """Asigna el nombre interno y los atributos de animación según el id del punto."""
        self.deltaAnguloCarta = 0.0
        self.anguloCarta = 0.0
        self.indiceOrbitaCarta = 0
        self.orbitaPosicional = 0.0
        self.orbitaAltura = 0.0
        self.escalaRuna = 0.0

        nombres = {
            'Ascendant': 'ascendente',
            'MC':        'medioCielo',
            'mean Node': 'nodoNorte',
            'true Node': 'nodoSur',
            'ARMC':      'armc',
        }
        self.nombre = nombres[self.idPunto]

    def __getitem__(self, key: str):
        """Permite acceso a atributos mediante notación de diccionario.

        Args:
            key: Nombre del atributo.

        Returns:
            El valor del atributo correspondiente.
        """
        return getattr(self, key)
