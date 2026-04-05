#!/usr/bin/python
"""Modelo de la carta astral: instantánea del cielo para una fecha y lugar dados."""

import re

from Signo import Signo
from Arabigo import Arabigo


class Carta:
    """Representa una instantánea astral completa para una fecha, hora y lugar.

    Contiene todos los objetos del cielo (planetas, casas, puntos sensibles,
    asteroides, signos y puntos arábigos) y proporciona acceso unificado a
    cualquiera de ellos mediante ``getPunto()``.

    Attributes:
        idFecha (str): Identificador de la carta en formato de fecha UTC
            tal como lo entrega swete64 (ej. '13.11.1989 3:45:00 UT').
        signos (list[Signo]): Los doce signos del zodíaco.
        idSignos (list[str]): Abreviaturas de los doce signos, en orden zodiacal.
        arabigos (list[Arabigo]): Todos los Puntos Arábigos de la carta.
        idArabigos (list[str]): Identificadores canónicos de los arábigos.
        planetas (list[Planeta]): Planetas asignados por ``setPuntos()``.
        casas (list[Casa]): Casas asignadas por ``setPuntos()``.
        puntos (list[Punto]): Puntos sensibles asignados por ``setPuntos()``.
        asteroides (list[Asteroide]): Asteroides asignados por ``setPuntos()``.
        diaNoche (str): Indica si la carta es diurna o nocturna ('dia' | 'noche').
            Calculado por SecuenciaAstral; el valor inicial es 'noche'.
    """

    def __init__(self, idFecha: str):
        """Inicializa la carta para la fecha dada.

        Crea los doce signos zodiacales, establece los signos opuestos entre sí,
        e inicializa todos los Puntos Arábigos.

        Args:
            idFecha: Identificador de fecha UTC entregado por swete64.
        """
        self.idFecha = idFecha
        self.idSignos = ['ar', 'ta', 'ge', 'cn', 'le', 'vi',
                         'li', 'sc', 'sa', 'cp', 'aq', 'pi']
        self.idArabigos = [
            'fortuna', 'infortunio|azemena-o-enfermedad|enemigos', 'amigos|paz',
            'amor-y-amistad', 'arar-y-sembrar', 'audacia-y-fortaleza',
            'lugar-de-la-enfermedad', 'buena-suerte-en-las-luchas',
            'celada-(Espíritu)', 'copulacion-o-amor-de-hombre',
            'delicias-y-sabor|firmeza-crecimiento-y-limpieza', 'enemigos-(Hermes)',
            'esperanza', 'haber', 'hermanos', 'numero-de-hermanos', 'hijos|vida',
            'sexo-de-los-hijos', 'hileg', 'ley|voluntad-y-justicia', 'madre',
            'matanza', 'matrimonio-para-varones-(Hermes)',
            'matrimonio-para-mujeres-(Hermes)', 'matrimonio-(Valens)', 'mercancia',
            'muerte', 'muerte-(Hermes)', 'muerte-(Zaradest)', 'navegar',
            'padres|rey', 'planeta-matador', 'pleitos-y-los-contrincantes',
            'profesion-y-reino-(A)|lugares-sobre-los-que-se-ejercera-el-cargo',
            'profesion-y-reino-(B)', 'profesion-y-reino-(C)', 'propiedades-(A)',
            'propiedades-(B)', 'religion', 'dignidad-(1)', 'dignidad-(2)',
            'perder-el-cargo', 'recuperar-el-cargo',
            'seso-alta-reflexion-y-razon-(Hermes)',
            'seso-alta-reflexion-y-razon-(Abumaxar)',
            'siervos-o-empleados-recaderos-y-mensajeros',
            'termino-o-final-de-las-cosas', 'viajes',
            'victoria-buena-andanza-escapamiento-y-defensa',
        ]
        self.signos = []
        self.arabigos = []
        self.diaNoche = 'noche'
        self.setSignos()
        self.setArabigos()

    def setSignos(self) -> None:
        """Crea los doce signos zodiacales y enlaza cada uno con su opuesto."""
        for idSigno in self.idSignos:
            signo = Signo(idSigno)
            self.signos.append(signo)
            # Los signos opuestos se enlazan mutuamente a partir del índice 6
            if signo.indice > 5:
                opuesto = self.getSigno(self.idSignos[signo.indice - 6])
                opuesto.signoOpuesto = signo
                signo.signoOpuesto = opuesto

    def getSigno(self, idSigno: str):
        """Devuelve el signo correspondiente a la abreviatura dada.

        Args:
            idSigno: Abreviatura de dos letras del signo (ej. 'ar').

        Returns:
            Instancia de Signo, o None si no se encuentra.
        """
        for signo in self.signos:
            if signo.idSigno == idSigno:
                return signo

    def setPuntos(self, planetas: list, casas: list, puntos: list, asteroides: list) -> None:
        """Asigna los objetos celestes calculados por Query a la carta.

        Args:
            planetas: Lista de instancias de Planeta.
            casas: Lista de instancias de Casa.
            puntos: Lista de instancias de Punto.
            asteroides: Lista de instancias de Asteroide.
        """
        self.planetas = planetas
        self.casas = casas
        self.puntos = puntos
        self.asteroides = asteroides

    def setDignidades(self) -> None:
        """Asigna las dignidades astrológicas a planetas y asteroides.

        Delega en el método ``setDignidades()`` de cada objeto, que registra
        las relaciones bidireccionalmente con los signos.
        """
        for planeta in self.planetas:
            planeta.setDignidades()
        for asteroide in self.asteroides:
            asteroide.setDignidades()

    def setDomicilios(self) -> None:
        """Asigna el signo de domicilio natural a cada casa."""
        for casa in self.casas:
            casa.setDomicilios()

    def setArabigos(self) -> None:
        """Crea e inicializa todos los Puntos Arábigos de la carta."""
        for idArabigo in self.idArabigos:
            self.arabigos.append(Arabigo(idArabigo, self))

    def getPunto(self, parametro: str):
        """Devuelve cualquier objeto de la carta mediante una ruta de atributos.

        La ruta puede tener hasta tres niveles separados por punto, por ejemplo:
        ``'sol'``, ``'sol.anguloReal'``, ``'sol.signo.nombre'``.

        La búsqueda recorre en orden: planetas → casas → puntos → asteroides
        → signos → arábigos.

        Args:
            parametro: Ruta de acceso al objeto o atributo (ej. 'luna.signo.nombre').

        Returns:
            El objeto o valor encontrado, o None si no existe (con aviso en consola).
        """
        parametros = re.split(r'\.', parametro)
        respuesta = None
        sigo = True

        colecciones = [
            self.planetas,
            self.casas,
            self.puntos,
            self.asteroides,
            self.signos,
            self.arabigos,
        ]

        for coleccion in colecciones:
            if not sigo:
                break
            for objeto in coleccion:
                if objeto.nombre == parametros[0]:
                    if len(parametros) == 1:
                        respuesta = objeto
                    elif len(parametros) == 2:
                        respuesta = objeto[parametros[1]]
                    else:
                        respuesta = objeto[parametros[1]][parametros[2]]
                    sigo = False
                    break

        if respuesta is None:
            print(f'getPunto NO encontró: {parametro} | idFecha: {self.idFecha}')

        return respuesta
