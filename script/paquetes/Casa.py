#!/usr/bin/python
"""Modelo de la casa astrológica dentro de una carta astral."""


class Casa:
    """Representa una de las doce casas del zodíaco en una carta astral.

    Las casas definen áreas temáticas de la vida (identidad, recursos,
    comunicación, etc.) y se calculan según el sistema Placidus a partir
    de la hora y lugar de nacimiento.

    Attributes:
        idCasa (str): Identificador en formato 'house N' (ej. 'house 1').
        carta (Carta): Referencia a la carta astral que contiene esta casa.
        indice (int): Número de la casa (1–12).
        nombre (str): Nombre legible en español (ej. 'casa 1').
        anguloGrado (str): Grados del ángulo cuspidal, tal como llega de swete64.
        anguloMinuto (str): Minutos del ángulo cuspidal.
        anguloSegundo (str): Segundos del ángulo cuspidal.
        anguloReal (float): Ángulo cuspidal en grados decimales dentro del signo.
        signo (Signo): Signo zodiacal en que se ubica la cúspide de la casa.
        domicilio (Signo): Signo natural de esta casa según el zodíaco natural.
        deltaAnguloCarta (float): Delta de movimiento respecto a la carta anterior.
        anguloCarta (float): Distancia total recorrida hasta la carta actual.
    """

    def __init__(self, idCasa: str, anguloGrado: str, anguloMinuto: str,
                 anguloSegundo: str, signo, carta):
        """Inicializa la casa astrológica.

        Args:
            idCasa: Identificador en formato 'house N'.
            anguloGrado: Grados de la cúspide, como string.
            anguloMinuto: Minutos de la cúspide, como string.
            anguloSegundo: Segundos de la cúspide, como string.
            signo: Instancia de Signo correspondiente a la cúspide.
            carta: Instancia de Carta que contiene esta casa.
        """
        self.idCasa = idCasa
        self.carta = carta
        self.anguloGrado = anguloGrado
        self.anguloMinuto = anguloMinuto
        self.anguloSegundo = anguloSegundo
        self.signo = signo
        self.setEntidadById()
        self.setAnguloReal()

    def setAnguloReal(self) -> None:
        """Calcula el ángulo cuspidal en grados decimales."""
        self.anguloReal = (
            int(self.anguloGrado)
            + int(self.anguloMinuto) / 60
            + float(self.anguloSegundo) / 3600
        )

    def setDomicilios(self) -> None:
        """Asigna el signo de domicilio natural de esta casa.

        El domicilio natural corresponde al signo que gobierna cada casa
        en el zodíaco natural (Aries→casa 1, Tauro→casa 2, etc.).
        """
        domicilios = {
            'house 1':  'aries',
            'house 2':  'tauro',
            'house 3':  'geminis',
            'house 4':  'cancer',
            'house 5':  'leo',
            'house 6':  'virgo',
            'house 7':  'libra',
            'house 8':  'escorpio',
            'house 9':  'sagitario',
            'house 10': 'capricorneo',
            'house 11': 'aquario',
            'house 12': 'piscis',
        }
        self.domicilio = self.carta.getPunto(domicilios[self.idCasa])

    def setEntidadById(self) -> None:
        """Inicializa índice, nombre y atributos de animación según el id de casa."""
        self.deltaAnguloCarta = 0.0
        self.anguloCarta = 0.0

        numero = int(self.idCasa.replace('house ', ''))
        self.indice = numero
        self.nombre = f'casa {numero}'

    def __getitem__(self, key: str):
        """Permite acceso a atributos mediante notación de diccionario.

        Args:
            key: Nombre del atributo.

        Returns:
            El valor del atributo correspondiente.
        """
        return getattr(self, key)
