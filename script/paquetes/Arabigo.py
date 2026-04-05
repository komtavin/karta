#!/usr/bin/python
"""Modelo de los Puntos Arábigos (Lotes Herméticos) dentro de una carta astral."""

import math


class Arabigo:
    """Representa un Punto Arábigo (Lote Hermético) de la tradición astrológica clásica.

    Los Puntos Arábigos son posiciones matemáticas calculadas a partir de la
    combinación de tres factores de la carta (planeta, casa o punto), con una
    fórmula diferente para cartas de día y de noche.

    Cada instancia define sus fórmulas ``dia`` y ``noche`` como listas de cinco
    elementos: [factor1, operador, factor2, operador, factor3].
    Los factores pueden ser nombres de objetos de la carta o la cadena '0'
    (indica que ese factor vale cero grados).
    Los factores de la forma ``'regente de N'`` indican el regente del signo
    de la casa N.

    Attributes:
        idArabigo (str): Identificador único con el nombre canónico del arábigo.
        carta (Carta): Referencia a la carta astral que contiene este objeto.
        nombre (str): Nombre corto usado como clave en la carta.
        dia (list[str]): Fórmula para cartas diurnas.
        noche (list[str]): Fórmula para cartas nocturnas.
        tieneRuna (bool): Indica si este arábigo tiene representación visual de runa.
        anguloReal (float): Ángulo calculado en grados dentro del signo (0–30).
        anguloGrado (int): Parte entera del ángulo.
        anguloMinuto (int): Minutos de arco.
        anguloSegundo (float): Segundos de arco.
        signo (Signo | str): Signo zodiacal en que se ubica el arábigo.
        sentido (str): Dirección de movimiento observable ('directo' | 'retrogrado').
        deltaAnguloCarta (float): Delta de movimiento respecto a la carta anterior.
        anguloCarta (float): Distancia total recorrida hasta la carta actual.
        indiceOrbitaCarta (int): Índice de órbita utilizada en la animación.
        orbitaPosicional (float): Distancia radial en la escena 3D.
        escalaRuna (float): Escala de la runa en la animación.
        escalaPlatonico (float): Escala del sólido platónico en la animación.
        escalaSubRuna (float): Escala de la sub-runa en la animación.
        subRuna1 (list[float]): Posición espacial [x, y, z] de la sub-runa 1.
        subRuna2 (list[float]): Posición espacial [x, y, z] de la sub-runa 2.
        subRuna3 (list[float]): Posición espacial [x, y, z] de la sub-runa 3.
    """

    def __init__(self, idArabigo: str, carta):
        """Inicializa el Punto Arábigo a partir de su identificador.

        Args:
            idArabigo: Nombre canónico del arábigo (ej. 'fortuna').
            carta: Instancia de Carta que contiene este arábigo.
        """
        self.idArabigo = idArabigo
        self.carta = carta
        self.anguloGrado = 0
        self.anguloMinuto = 0
        self.anguloSegundo = 0
        self.anguloReal = 0.0
        self.signo = ''
        self.sentido = ''
        self.setEntidadById()
        #self.setAnguloReal()

    def setAnguloReal(self, anguloReal: float) -> None:
        """Asigna el ángulo calculado y descompone en grado, minuto y segundo.

        Args:
            anguloReal: Ángulo en grados decimales dentro del signo (0–30).
        """
        self.anguloReal = anguloReal
        self.anguloGrado = math.floor(anguloReal)
        self.anguloMinuto = math.floor((anguloReal - self.anguloGrado) * 60)
        self.anguloSegundo = (
            ((anguloReal - self.anguloGrado) * 60) - self.anguloMinuto
        ) * 60
        #self.anguloReal = int(self.anguloGrado) + (int(self.anguloMinuto) / 60) + (float(self.anguloSegundo) / 3600)

    def setEntidadById(self) -> None:
        """Inicializa nombre, fórmulas día/noche, runa y atributos de animación.

        Las fórmulas siguen la tradición de Abū Maʿshar y Hermes Trismegisto.
        Cada lista tiene la forma [factor1, operador, factor2, operador, factor3].
        """
        self.deltaAnguloCarta = 0.0
        self.anguloCarta = 0.0
        self.indiceOrbitaCarta = 0
        self.orbitaPosicional = 0.0
        self.escalaRuna = 0.0
        self.escalaPlatonico = 0.0
        self.escalaSubRuna = 0.0
        self.subRuna1 = [0.0, 0.0, 0.0]
        self.subRuna2 = [0.0, 0.0, 0.0]
        self.subRuna3 = [0.0, 0.0, 0.0]

        # Tabla de arábigos: idArabigo → (nombre, dia, noche, tieneRuna)
        # Fuente: Abū Maʿshar, Hermes Trismegisto y Vettius Valens.
        _tabla = {
            'fortuna': (
                'fortuna',
                ['ascendente', '+', 'luna', '-', 'sol'],
                ['ascendente', '+', 'sol', '-', 'luna'],
                True,
            ),
            'infortunio|azemena-o-enfermedad|enemigos': (
                'infortunio',
                ['ascendente', '+', 'marte', '-', 'saturno'],
                ['ascendente', '+', 'saturno', '-', 'marte'],
                True,
            ),
            'amigos|paz': (
                'paz',
                ['ascendente', '+', 'mercurio', '-', 'luna'],
                ['ascendente', '+', 'mercurio', '-', 'luna'],
                False,
            ),
            'amor-y-amistad': (
                'amistad',
                ['ascendente', '+', 'fortuna', '-', 'venus'],
                ['ascendente', '+', 'fortuna', '-', 'venus'],
                False,
            ),
            'arar-y-sembrar': (
                'sembrar',
                ['ascendente', '+', 'fortuna', '-', 'saturno'],
                ['ascendente', '+', 'saturno', '-', 'fortuna'],
                False,
            ),
            'audacia-y-fortaleza': (
                'fortaleza',
                ['ascendente', '+', 'fortuna', '-', 'marte'],
                ['ascendente', '+', 'fortuna', '-', 'marte'],
                False,
            ),
            'lugar-de-la-enfermedad': (
                'enfermedad',
                ['0', '+', 'sol', '-', 'regente de 1'],
                ['0', '+', 'sol', '-', 'regente de 1'],
                False,
            ),
            'buena-suerte-en-las-luchas': (
                'suerte-luchas',
                ['ascendente', '+', 'marte', '-', 'sol'],
                ['ascendente', '+', 'marte', '-', 'sol'],
                False,
            ),
            'celada-(Espíritu)': (
                'celada',
                ['ascendente', '+', 'sol', '-', 'luna'],
                ['ascendente', '+', 'luna', '-', 'sol'],
                False,
            ),
            'copulacion-o-amor-de-hombre': (
                'copulacion',
                ['ascendente', '+', 'venus', '-', 'marte'],
                ['ascendente', '+', 'venus', '-', 'marte'],
                False,
            ),
            'delicias-y-sabor|firmeza-crecimiento-y-limpieza': (
                'delicias',
                ['ascendente', '+', 'fortuna', '-', 'venus'],
                ['ascendente', '+', 'venus', '-', 'fortuna'],
                False,
            ),
            'enemigos-(Hermes)': (
                'enemigos',
                ['ascendente', '+', 'saturno', '-', 'sol'],
                ['ascendente', '+', 'sol', '-', 'saturno'],
                False,
            ),
            'esperanza': (
                'esperanza',
                ['ascendente', '+', 'mercurio', '-', 'saturno'],
                ['ascendente', '+', 'saturno', '-', 'mercurio'],
                False,
            ),
            'haber': (
                'haber',
                ['ascendente', '+', 'regente de 2', '-', 'luna'],
                ['ascendente', '+', 'luna', '-', 'regente de 2'],
                False,
            ),
            'hermanos': (
                'hermanos',
                ['ascendente', '+', 'saturno', '-', 'luna'],
                ['ascendente', '+', 'luna', '-', 'saturno'],
                False,
            ),
            'numero-de-hermanos': (
                'numero-hermanos',
                ['ascendente', '+', 'saturno', '-', 'mercurio'],
                ['ascendente', '+', 'mercurio', '-', 'saturno'],
                False,
            ),
            'hijos|vida': (
                'hijos',
                ['ascendente', '+', 'jupiter', '-', 'saturno'],
                ['ascendente', '+', 'saturno', '-', 'jupiter'],
                False,
            ),
            'sexo-de-los-hijos': (
                'sexo-hijos',
                ['ascendente', '+', 'venus', '-', 'luna'],
                ['ascendente', '+', 'luna', '-', 'venus'],
                False,
            ),
            'hileg': (
                'hileg',
                ['ascendente', '+', 'sol', '-', 'luna'],
                ['ascendente', '+', 'luna', '-', 'sol'],
                False,
            ),
            'ley|voluntad-y-justicia': (
                'ley',
                ['ascendente', '+', 'saturno', '-', 'venus'],
                ['ascendente', '+', 'venus', '-', 'saturno'],
                False,
            ),
            'madre': (
                'madre',
                ['ascendente', '+', 'luna', '-', 'venus'],
                ['ascendente', '+', 'venus', '-', 'luna'],
                False,
            ),
            'matanza': (
                'matanza',
                ['ascendente', '+', 'marte', '-', 'saturno'],
                ['ascendente', '+', 'saturno', '-', 'marte'],
                True,
            ),
            'matrimonio-para-varones-(Hermes)': (
                'matrimonio-varones',
                ['ascendente', '+', 'venus', '-', 'saturno'],
                ['ascendente', '+', 'saturno', '-', 'venus'],
                False,
            ),
            'matrimonio-para-mujeres-(Hermes)': (
                'matrimonio-mujeres',
                ['ascendente', '+', 'marte', '-', 'luna'],
                ['ascendente', '+', 'luna', '-', 'marte'],
                False,
            ),
            'matrimonio-(Valens)': (
                'matrimonio-valens',
                ['ascendente', '+', 'venus', '-', 'saturno'],
                ['ascendente', '+', 'marte', '-', 'luna'],
                False,
            ),
            'mercancia': (
                'mercancia',
                ['ascendente', '+', 'mercurio', '-', 'sol'],
                ['ascendente', '+', 'sol', '-', 'mercurio'],
                False,
            ),
            'muerte': (
                'muerte',
                ['ascendente', '+', 'regente de 8', '-', 'luna'],
                ['ascendente', '+', 'luna', '-', 'regente de 8'],
                False,
            ),
            'muerte-(Hermes)': (
                'muerte-hermes',
                ['ascendente', '+', 'saturno', '-', 'luna'],
                ['ascendente', '+', 'luna', '-', 'saturno'],
                False,
            ),
            'muerte-(Zaradest)': (
                'muerte-zaradest',
                ['ascendente', '+', 'regente de 8', '-', 'saturno'],
                ['ascendente', '+', 'saturno', '-', 'regente de 8'],
                False,
            ),
            'navegar': (
                'navegar',
                ['ascendente', '+', 'luna', '-', 'saturno'],
                ['ascendente', '+', 'saturno', '-', 'luna'],
                True,
            ),
            'padres|rey': (
                'padres',
                ['ascendente', '+', 'sol', '-', 'saturno'],
                ['ascendente', '+', 'saturno', '-', 'sol'],
                False,
            ),
            'planeta-matador': (
                'planeta-matador',
                ['ascendente', '+', 'saturno', '-', 'marte'],
                ['ascendente', '+', 'marte', '-', 'saturno'],
                False,
            ),
            'pleitos-y-los-contrincantes': (
                'pleitos',
                ['ascendente', '+', 'marte', '-', 'jupiter'],
                ['ascendente', '+', 'jupiter', '-', 'marte'],
                False,
            ),
            'profesion-y-reino-(A)|lugares-sobre-los-que-se-ejercera-el-cargo': (
                'reino-a',
                ['ascendente', '+', 'marte', '-', 'sol'],
                ['ascendente', '+', 'jupiter', '-', 'luna'],
                False,
            ),
            'profesion-y-reino-(B)': (
                'reino-b',
                ['medioCielo', '+', 'luna', '-', 'sol'],
                ['medioCielo', '+', 'sol', '-', 'luna'],
                False,
            ),
            'profesion-y-reino-(C)': (
                'reino-c',
                ['ascendente', '+', 'luna', '-', 'saturno'],
                ['ascendente', '+', 'saturno', '-', 'luna'],
                False,
            ),
            'propiedades-(A)': (
                'propiedades-a',
                ['ascendente', '+', 'luna', '-', 'saturno'],
                ['ascendente', '+', 'luna', '-', 'saturno'],
                False,
            ),
            'propiedades-(B)': (
                'propiedades-b',
                ['casa 4', '+', 'saturno', '-', 'regente de 4'],
                # Noche: fórmula invertida según la tradición clásica
                ['casa 4', '-', 'saturno', '+', 'regente de 4'],
                False,
            ),
            'religion': (
                'religion',
                ['ascendente', '+', 'mercurio', '-', 'luna'],
                ['ascendente', '+', 'luna', '-', 'mercurio'],
                False,
            ),
            'dignidad-(1)': (
                'dignidad-1',
                ['ascendente', '+', 'jupiter', '-', 'reino-a'],
                ['ascendente', '+', 'jupiter', '-', 'reino-a'],
                False,
            ),
            'dignidad-(2)': (
                'dignidad-2',
                ['ascendente', '+', 'reino-a', '-', 'sol'],
                ['ascendente', '+', 'reino-a', '-', 'sol'],
                False,
            ),
            'perder-el-cargo': (
                'perder-cargo',
                ['saturno', '+', 'jupiter', '-', 'sol'],
                ['saturno', '+', 'jupiter', '-', 'sol'],
                False,
            ),
            'recuperar-el-cargo': (
                'recuperar-cargo',
                ['ascendente', '+', 'jupiter', '-', 'sol'],
                ['ascendente', '+', 'jupiter', '-', 'sol'],
                False,
            ),
            'seso-alta-reflexion-y-razon-(Hermes)': (
                'razon-hermes',
                ['ascendente', '+', 'mercurio', '-', 'saturno'],
                ['ascendente', '+', 'saturno', '-', 'mercurio'],
                False,
            ),
            'seso-alta-reflexion-y-razon-(Abumaxar)': (
                'razon-abumaxar',
                ['ascendente', '+', 'marte', '-', 'mercurio'],
                ['ascendente', '+', 'mercurio', '-', 'marte'],
                False,
            ),
            'siervos-o-empleados-recaderos-y-mensajeros': (
                'mensajeros',
                ['ascendente', '+', 'luna', '-', 'mercurio'],
                ['ascendente', '+', 'luna', '-', 'mercurio'],
                False,
            ),
            'termino-o-final-de-las-cosas': (
                'final',
                ['ascendente', '+', 'marte', '-', 'saturno'],
                ['ascendente', '+', 'marte', '-', 'saturno'],
                False,
            ),
            'viajes': (
                'viajes',
                ['ascendente', '+', 'casa 9', '-', 'regente de 9'],
                ['ascendente', '+', 'casa 9', '-', 'regente de 9'],
                False,
            ),
            'victoria-buena-andanza-escapamiento-y-defensa': (
                'buena-andanza',
                ['ascendente', '+', 'jupiter', '-', 'celada'],
                ['ascendente', '+', 'celada', '-', 'jupiter'],
                False,
            ),
        }

        nombre, dia, noche, tieneRuna = _tabla[self.idArabigo]
        self.nombre = nombre
        self.dia = dia
        self.noche = noche
        self.tieneRuna = tieneRuna

    def __getitem__(self, key: str):
        """Permite acceso a atributos mediante notación de diccionario.

        Args:
            key: Nombre del atributo.

        Returns:
            El valor del atributo correspondiente.
        """
        return getattr(self, key)
