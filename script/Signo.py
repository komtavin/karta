#!/usr/bin/python
"""Modelo del signo zodiacal dentro de una carta astral."""


class Signo:
    """Representa un signo del zodíaco con sus atributos esenciales.

    Attributes:
        idSigno (str): Abreviatura de dos letras que identifica el signo
            (ej. 'ar' para Aries, 'ta' para Tauro).
        nombre (str): Nombre completo del signo en español.
        indice (int): Posición en el zodíaco, comenzando en 0 (Aries).
        polaridad (str): '+' para masculino/yang, '-' para femenino/yin.
        genero (str): 'masculino' o 'femenino'.
        elemento (str): Elemento al que pertenece ('fuego', 'tierra', 'aire', 'agua').
        simbolo (str): Palabra clave que describe la esencia del signo.
        anguloInicialReal (float): Ángulo de posición inicial en la rueda zodiacal.
        signoOpuesto (Signo): Referencia al signo opuesto (asignado por Carta).
        regente (Planeta | str): Planeta regente del signo.
        coRegente (Planeta | str): Planeta co-regente del signo.
        detrimentoModerno (Planeta | str): Planeta en detrimento moderno.
        exaltacion (Planeta | str): Planeta exaltado en este signo.
        caida (Planeta | str): Planeta en caída en este signo.
        deltaAnguloCarta (float): Delta de movimiento respecto a la carta anterior.
        anguloCarta (float): Distancia total recorrida hasta la carta actual.
        indiceOrbitaCarta (int): Índice de órbita utilizada en la animación.
        orbitaPosicional (float): Distancia radial del objeto en la escena.
        orbitaAltura (float): Altura axial en la escena 3D.
        escalaRuna (float): Escala de la runa en la animación.
        escalaPlatonico (float): Escala del sólido platónico en la animación.
    """

    def __init__(self, idSigno: str):
        """Inicializa el signo zodiacal a partir de su abreviatura.

        Args:
            idSigno: Abreviatura de dos letras del signo
                ('ar', 'ta', 'ge', 'cn', 'le', 'vi', 'li', 'sc', 'sa', 'cp', 'aq', 'pi').
        """
        self.idSigno = idSigno
        #self.padrePlaneta = ""
        #self.padreCasa = ""
        #self.padrePunto = ""
        self.setEntidadById(idSigno)
        #self.regenteVerdadero = []
        self.regente = ''
        self.coRegente = ''
        self.detrimentoModerno = ''
        self.exaltacion = ''
        self.caida = ''

    #def setRegentesVerdaderos(self, planeta):
    #    self.regenteVerdadero.append(planeta)

    def setRegente(self, punto) -> None:
        """Asigna el planeta regente del signo.

        Args:
            punto: Objeto Planeta o Asteroide que rige este signo.
        """
        self.regente = punto

    def setCoRegente(self, punto) -> None:
        """Asigna el planeta co-regente del signo.

        Args:
            punto: Objeto Planeta o Asteroide co-regente.
        """
        self.coRegente = punto

    def setDetrimentoModerno(self, punto) -> None:
        """Asigna el planeta en detrimento moderno para este signo.

        Args:
            punto: Objeto Planeta o Asteroide en detrimento.
        """
        self.detrimentoModerno = punto

    def setExaltacion(self, punto) -> None:
        """Asigna el planeta exaltado en este signo.

        Args:
            punto: Objeto Planeta o Asteroide exaltado.
        """
        self.exaltacion = punto

    def setCaida(self, punto) -> None:
        """Asigna el planeta en caída en este signo.

        Args:
            punto: Objeto Planeta o Asteroide en caída.
        """
        self.caida = punto

    def setEntidadById(self, idSigno: str) -> None:
        """Inicializa todos los atributos del signo según su abreviatura.

        Define nombre, índice, polaridad, género, elemento, símbolo y
        ángulo inicial real. También inicializa los atributos de animación
        en sus valores neutros.

        Args:
            idSigno: Abreviatura de dos letras del signo.
        """
        self.deltaAnguloCarta = 0.0
        self.anguloCarta = 0.0
        self.indiceOrbitaCarta = 0
        self.orbitaPosicional = 0.0
        self.orbitaAltura = 0.0
        self.escalaRuna = 0.0
        self.escalaPlatonico = 0.0

        signos = {
            'ar': (0,  'aries',      '+', 'masculino', 'fuego',   'renacimiento'),
            'ta': (1,  'tauro',      '-', 'femenino',  'tierra',  'consolidacion'),
            'ge': (2,  'geminis',    '+', 'masculino', 'aire',    'conciencia concreta'),
            'cn': (3,  'cancer',     '-', 'femenino',  'agua',    'familia'),
            'le': (4,  'leo',        '+', 'masculino', 'fuego',   'fuerza de la vida'),
            'vi': (5,  'virgo',      '-', 'femenino',  'tierra',  'servicio y trabajo'),
            'li': (6,  'libra',      '+', 'masculino', 'aire',    'equilibrio y armonia'),
            'sc': (7,  'escorpio',   '-', 'femenino',  'agua',    'pasion'),
            'sa': (8,  'sagitario',  '+', 'masculino', 'fuego',   'conciencia superior'),
            'cp': (9,  'capricorneo','-', 'femenino',  'tierra',  'sabiduria'),
            'aq': (10, 'aquario',    '+', 'masculino', 'aire',    'revolucion'),
            'pi': (11, 'piscis',     '-', 'femenino',  'agua',    'disolucion'),
        }

        indice, nombre, polaridad, genero, elemento, simbolo = signos[idSigno]
        self.indice = indice
        self.nombre = nombre
        self.polaridad = polaridad
        self.genero = genero
        self.elemento = elemento
        self.simbolo = simbolo
        # El ángulo inicial coloca el centro del signo en su posición zodiacal.
        # El +15 desplaza desde el borde al centro de cada sector de 30°.
        self.anguloInicialReal = -(30 * indice + 15)

    def __getitem__(self, key: str):
        """Permite acceso a atributos mediante notación de diccionario.

        Args:
            key: Nombre del atributo.

        Returns:
            El valor del atributo correspondiente.
        """
        return getattr(self, key)
