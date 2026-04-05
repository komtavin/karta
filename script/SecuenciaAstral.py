#!/usr/bin/python
"""Motor de animación de la secuencia astral en Blender.

Orquesta el cálculo de posiciones celestes a lo largo de una secuencia de
cartas y las escribe como keyframes en la escena de Blender.
"""

import re
import bpy
import math


class SecuenciaAstral:
    """Secuencia de cartas astrales animada en Blender.

    Recibe una instancia de Query ya configurada, ejecuta la consulta a swete64,
    calcula las posiciones de todos los objetos celestes en cada carta y escribe
    los keyframes correspondientes en la escena de Blender.

    El flujo de construcción es:
    1. ``calculosQuery``: determina si cada carta es de día o de noche (detección
       de amanecer/atardecer) y calcula los Puntos Arábigos.
    2. ``calculosQuery1``: determina el sentido (directo/retrógrado) de cada objeto.
    3. ``setInstantanea``: calcula los ángulos de animación y escribe los keyframes
       en Blender para cada carta.

    Attributes:
        cartas (list[Carta]): Cartas de la ventana principal que se animarán.
        cartasQuery (list[Carta]): Cartas completas (ventana extendida) usadas
            para detectar amanecer/atardecer y calcular retrogradaciones.
        constante (int): Número de frames de Blender asignados a cada carta.
        deltaOrbita (float): Separación radial entre órbitas de objetos (unidades Blender).
        orbitaInicial (float): Radio de la primera órbita desde el centro.
        tolerancia (float): Margen en grados (±) para determinar si dos objetos
            se solapan angularmente en la misma órbita.
        numeroDiscosCasa (int): Número de discos clonados por casa en la escena.
        objetosArr (list[str]): Nombres de los arábigos con representación visual
            (runa) en la animación.
        indiceOrbitaActual (int): Contador de órbita usado durante la traslación
            en ``setInstantanea``.
    """

    def __init__(self, query):
        """Inicializa la secuencia, ejecuta la consulta y anima la escena.

        Args:
            query: Instancia de Query configurada con fecha, lugar y parámetros
                de swete64. Se llama a ``obtener()`` y ``procesar()`` internamente.
        """
        query.obtener()
        query.procesar()
        self.cartas = query.cartas
        self.cartasQuery = query.cartasQuery
        self.constante = 30         # Frames de Blender por carta
        self.deltaOrbita = 6        # Separación radial entre órbitas (unidades Blender)
        self.orbitaInicial = 20     # Radio de la primera órbita
        self.tolerancia = 20        # Margen angular ± en grados para colisión orbital
        self.numeroDiscosCasa = 40  # Discos clonados por casa
        self.objetosArr = [
            'fortuna', 'infortunio', 'paz', 'enfermedad',
            'hileg', 'navegar', 'matanza',
        ]

        for i in range(len(self.cartasQuery)):
            self.calculosQuery(i)

        for i in range(len(self.cartasQuery)):
            self.calculosQuery1(i)

        for i in range(len(self.cartas)):
            self.setInstantanea(i)

    '''Operaciones sobre cartaQuery'''
    def calculosQuery(self, indiceCartasQuery: int) -> None:
        """Determina si la carta es de día o de noche y calcula los Puntos Arábigos.

        La detección de amanecer (día) y atardecer (noche) se realiza comparando
        el signo del Sol con el del Ascendente: si coinciden → amanecer (carta diurna);
        si el Ascendente está en el signo opuesto al Sol → atardecer (carta nocturna).
        En cualquier otro caso, la carta hereda el valor de la anterior.

        Los Puntos Arábigos se calculan con la fórmula correspondiente a día o noche
        y su resultado se propaga a la carta de la ventana principal que tenga la
        misma idFecha.

        Args:
            indiceCartasQuery: Índice de la carta en ``self.cartasQuery``.
        """
        # Determinar momento de la carta, o sea, dia o noche
        if self.cartasQuery[indiceCartasQuery].getPunto('sol.signo.nombre') == self.cartasQuery[indiceCartasQuery].getPunto('ascendente.signo.nombre'):
            anguloSol_AscendenteTMP = self.cartasQuery[indiceCartasQuery].getPunto('sol.anguloReal') - self.cartasQuery[indiceCartasQuery].getPunto('ascendente.anguloReal')
            self.cartasQuery[indiceCartasQuery].diaNoche = 'dia'
            for j in range(len(self.cartas)):
                if self.cartas[j].idFecha == self.cartasQuery[indiceCartasQuery].idFecha:
                    self.cartas[j].diaNoche = 'dia'
                    break
            if indiceCartasQuery > 0:
                self.cartasQuery[indiceCartasQuery - 1].diaNoche = 'noche'
                for j in range(len(self.cartas)):
                    if self.cartas[j].idFecha == self.cartasQuery[indiceCartasQuery - 1].idFecha:
                        self.cartas[j].diaNoche = 'noche'
                        break
        elif self.cartasQuery[indiceCartasQuery].getPunto('ascendente.signo.nombre') == self.cartasQuery[indiceCartasQuery].getPunto('sol.signo').signoOpuesto.nombre:
            anguloSol_AscendenteTMP = self.cartasQuery[indiceCartasQuery].getPunto('sol.anguloReal') - self.cartasQuery[indiceCartasQuery].getPunto('ascendente.anguloReal')
            self.cartasQuery[indiceCartasQuery].diaNoche = 'noche'
            for j in range(len(self.cartas)):
                if self.cartas[j].idFecha == self.cartasQuery[indiceCartasQuery].idFecha:
                    self.cartas[j].diaNoche = 'noche'
                    break
            if indiceCartasQuery > 0:
                self.cartasQuery[indiceCartasQuery - 1].diaNoche = 'dia'
                for j in range(len(self.cartas)):
                    if self.cartas[j].idFecha == self.cartasQuery[indiceCartasQuery - 1].idFecha:
                        self.cartas[j].diaNoche = 'dia'
                        break
        else:
            if indiceCartasQuery == 0:
                self.cartasQuery[0].diaNoche = 'noche'
                for j in range(len(self.cartas)):
                    if self.cartas[j].idFecha == self.cartasQuery[0].idFecha:
                        self.cartas[j].diaNoche = 'noche'
                        break
            else:
                self.cartasQuery[indiceCartasQuery].diaNoche = self.cartasQuery[indiceCartasQuery - 1].diaNoche
                for j in range(len(self.cartas)):
                    if self.cartas[j].idFecha == self.cartasQuery[indiceCartasQuery].idFecha:
                        self.cartas[j].diaNoche = self.cartasQuery[indiceCartasQuery - 1].diaNoche
                        break
        
        # CALCULO
        '''for arabigo in self.cartasQuery[indiceCartasQuery].arabigos:
            if arabigo.nombre == 'propiedades-b':
                cualquier_cosa = 0
                #for casa in self.cartasQuery[indiceCartasQuery].casas:
                #    print('Regente', casa.nombre, casa.signo.nombre, casa.signo.regente.nombre, casa.signo.regente.signo.nombre)
                #    print('Co-Regente', casa.nombre, casa.signo.nombre, casa.signo.coRegente.nombre, casa.signo.coRegente.signo.nombre)
            else:#elif '13.11.1989 3:45:00 UT' == self.cartasQuery[indiceCartasQuery].idFecha and arabigo.nombre == 'celada':
                diaNoche = self.cartasQuery[indiceCartasQuery].diaNoche
                calculo = 0
                factorEsNumerico = [False, False, False]
                #factor2EsNumerico = False
                #factor3EsNumerico = False
                for j in range(len(arabigo[diaNoche])):
                    #if j == 0:
                    #    try:
                    #        temp = int(arabigo[diaNoche][j])#self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).anguloReal + -1 * (self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).signo.anguloInicialReal + 15)
                    #        factorEsNumerico[j] = True
                    #    except ValueError:
                    #        temp = self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).anguloReal + -1 * (self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).signo.anguloInicialReal + 15)
                    #        factorEsNumerico[j] = False
                    #    calculo = calculo + temp
                    #elif j == 2 or j == 4:
                    aux = re.split(' ', arabigo[diaNoche][j])
                    if len(aux) == 3:
                        casa = self.cartasQuery[indiceCartasQuery].getPunto('casa ' + aux[2])
                        temp = casa.signo.regente.anguloReal + -1 * (casa.signo.regente.signo.anguloInicialReal + 15)
                    else:
                        #if j == 0:
                        #    #try:
                        #    #    temp = int(arabigo[diaNoche][j])#self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).anguloReal + -1 * (self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).signo.anguloInicialReal + 15)
                        #    #    factorEsNumerico[j] = True
                        #    #except ValueError:
                        #    #    temp = self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).anguloReal + -1 * (self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).signo.anguloInicialReal + 15)
                        #    #    factorEsNumerico[j] = False
                        #if j == 2:
                        #    corrigeIndice = j / 2 # 1
                        #    #try:
                        #    #    temp = int(arabigo[diaNoche][j])
                        #    #    factorEsNumerico[j - 1] = True
                        #    #except ValueError:
                        #    #    temp = self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).anguloReal + -1 * (self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).signo.anguloInicialReal + 15)
                        #    #    factorEsNumerico[j - 1] = False
                        #if j == 4:
                        #    corrigeIndice = j / 2 # 2
                        if j == 0 or j == 2 or j == 4:
                            corrigeIndice = int(j / 2)
                            try:
                                temp = int(arabigo[diaNoche][j])
                                factorEsNumerico[j - corrigeIndice] = True
                            except ValueError:
                                temp = self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).anguloReal + -1 * (self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).signo.anguloInicialReal + 15)
                                factorEsNumerico[j - corrigeIndice] = False
                        #temp = self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).anguloReal + -1 * (self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).signo.anguloInicialReal + 15)
                    if j == 0:
                        calculo = calculo + temp
                    elif j == 2 or j == 4:
                        if arabigo[diaNoche][j - 1] == '+':
                            calculo = calculo + temp
                        else:
                            calculo = calculo - temp
                for signo in self.cartasQuery[indiceCartasQuery].signos:
                    anguloReal = calculo - signo.indice * 30
                    if anguloReal > 360:
                        anguloReal -= 360
                    elif anguloReal < -360:
                        anguloReal += 360
                    if calculo < 0:
                        anguloReal += 30
                    if (anguloReal >= 0 and anguloReal < 30):
                        arabigo.setAnguloReal(anguloReal)
                        if calculo < 0:
                            if signo.indice == 0:
                                arabigo.signo = self.cartasQuery[indiceCartasQuery].signos[11]
                            else:
                                arabigo.signo = self.cartasQuery[indiceCartasQuery].signos[signo.indice - 1]
                        else:
                            arabigo.signo = signo
                        for j in range(len(self.cartas)):
                            if self.cartas[j].idFecha == self.cartasQuery[indiceCartasQuery].idFecha:
                                self.cartas[j].getPunto(arabigo.nombre).anguloReal = arabigo.anguloReal
                                self.cartas[j].getPunto(arabigo.nombre).signo = arabigo.signo
                                break
                        break
                for j in range(len(self.cartas)):
                    if self.cartas[j].idFecha == self.cartasQuery[indiceCartasQuery].idFecha:
                        # FIX v1.0: reemplaza el arábigo existente en lugar de duplicarlo
                        for k in range(len(self.cartas[j].arabigos)):
                            if self.cartas[j].arabigos[k].nombre == arabigo.nombre:
                                self.cartas[j].arabigos[k] = arabigo
                                break
                        break
                #if '13.11.1989 3:45:00 UT' == self.cartasQuery[indiceCartasQuery].idFecha and arabigo.nombre == 'propiedades-a':
                #    print()
                #    print('Carta:', self.cartasQuery[indiceCartasQuery].idFecha, arabigo.nombre, '=', arabigo[diaNoche][0], arabigo[diaNoche][1], arabigo[diaNoche][2], arabigo[diaNoche][3], arabigo[diaNoche][4], self.cartasQuery[indiceCartasQuery].diaNoche)
                #    if factorEsNumerico[0]:
                #        print(arabigo[diaNoche][0], '+', 'sin signo', '=', arabigo[diaNoche][0], '+', 'sin anguloInicialReal', '=', 'arabigo[diaNoche][0]', '=', arabigo[diaNoche][0], '°', '00', '\'', '00', '"')
                #    else:
                #        print(arabigo[diaNoche][0], '+', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][0]).signo.nombre, '=', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][0]).anguloReal, '+', -1 * self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][0]).signo.anguloInicialReal + 15, '=', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][0]).anguloReal + -1 * self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][0]).signo.anguloInicialReal + 15, '=', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][0]).anguloGrado, '°', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][0]).anguloMinuto, '\'', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][0]).anguloSegundo, '"')
                #    print(arabigo[diaNoche][2], '+', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][2]).signo.nombre, '=', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][2]).anguloReal, '+', -1 * self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][2]).signo.anguloInicialReal + 15, '=', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][2]).anguloReal + -1 * self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][2]).signo.anguloInicialReal + 15, '=', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][2]).anguloGrado, '°', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][2]).anguloMinuto, '\'', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][2]).anguloSegundo, '"')
                #    aux = re.split(' ', arabigo[diaNoche][j])
                #    if len(aux) == 3:
                #        casa = self.cartasQuery[indiceCartasQuery].getPunto('casa ' + aux[2])
                #        print(arabigo[diaNoche][4], '+', casa.signo.regente.signo.nombre, '=', casa.signo.regente.anguloReal, '+', -1 * casa.signo.regente.signo.anguloInicialReal + 15, '=', casa.signo.regente.anguloReal + -1 * casa.signo.regente.signo.anguloInicialReal + 15, '=', casa.signo.regente.anguloGrado, '°', casa.signo.regente.anguloMinuto, '\'', casa.signo.regente.anguloSegundo, '"')#, '=', casa.anguloReal, '+', -1 * casa.signo.anguloInicialReal + 15, '=', casa.anguloReal + -1 * casa.signo.anguloInicialReal + 15, '=', casa.anguloGrado, '°', casa.anguloMinuto, '\'', casa.anguloSegundo, '"')
                #    else:
                #        print(arabigo[diaNoche][4], '+', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][4]).signo.nombre, '=', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][4]).anguloReal, '+', -1 * self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][4]).signo.anguloInicialReal + 15, '=', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][4]).anguloReal + -1 * self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][4]).signo.anguloInicialReal + 15, '=', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][4]).anguloGrado, '°', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][4]).anguloMinuto, '\'', self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][4]).anguloSegundo, '"')
                #    print(arabigo.nombre, arabigo.signo.nombre, '=', anguloReal, '=', arabigo.anguloReal, '=', arabigo.anguloGrado, '°', arabigo.anguloMinuto, '\'', arabigo.anguloSegundo, '"')
        '''
    def calculosQuery1(self, indiceCartasQuery: int) -> None:
        """Determina el sentido de movimiento (directo/retrógrado) de cada objeto.

        Compara el ángulo real de cada objeto con el de la carta anterior o
        siguiente para calcular la diferencia y asignar el sentido. El resultado
        se propaga a la carta correspondiente en la ventana principal.

        Actualmente activos: planetas, puntos y asteroides.
        Pendiente de activación: arábigos.

        Args:
            indiceCartasQuery: Índice de la carta en ``self.cartasQuery``.
        """
        # ANALISIS
        for planeta in self.cartasQuery[indiceCartasQuery].planetas:
            # Set Retrogrados|Directos
            if indiceCartasQuery == 0:
                planetaAnguloSiguiente = self.cartasQuery[indiceCartasQuery + 1].getPunto(planeta.nombre + '.anguloReal')#[indiceCartasQuery + 1]
                diferencia = planetaAnguloSiguiente - planeta.anguloReal
            elif indiceCartasQuery > 0:
                planetaAnguloAnterior = self.cartasQuery[indiceCartasQuery - 1].getPunto(planeta.nombre + '.anguloReal')#[indiceCartasQuery - 1]
                diferencia = planeta.anguloReal - planetaAnguloAnterior
            if diferencia <= 0:
                planeta.sentido = 'retrogrado'
            elif diferencia > 0:
                planeta.sentido = 'directo'
            # Cambia Planeta de signo?
            if indiceCartasQuery > 0:
                planetaSignoNombreAnterior = self.cartasQuery[indiceCartasQuery - 1].getPunto(planeta.nombre + '.signo.nombre')#[indiceCartasQuery - 1]
            for j in range(len(self.cartas)):
                if self.cartas[j].idFecha == self.cartasQuery[indiceCartasQuery].idFecha:
                    self.cartas[j].getPunto(planeta.nombre).sentido = planeta.sentido
                    break
        for punto in self.cartasQuery[indiceCartasQuery].puntos:
            # Set Retrogrados|Directos
            if indiceCartasQuery == 0:
                puntoAnguloSiguiente = self.cartasQuery[indiceCartasQuery + 1].getPunto(punto.nombre + '.anguloReal')#[indiceCartasQuery + 1]
                diferencia = puntoAnguloSiguiente - punto.anguloReal
            elif indiceCartasQuery > 0:
                puntoAnguloAnterior = self.cartasQuery[indiceCartasQuery - 1].getPunto(punto.nombre + '.anguloReal')#[indiceCartasQuery - 1]
                diferencia = punto.anguloReal - puntoAnguloAnterior
            if diferencia <= 0:
                punto.sentido = 'retrogrado'
            elif diferencia > 0:
                punto.sentido = 'directo'
            # Cambia Planeta de signo?
            if indiceCartasQuery > 0:
                puntoSignoNombreAnterior = self.cartasQuery[indiceCartasQuery - 1].getPunto(punto.nombre + '.signo.nombre')#[indiceCartasQuery - 1]
            for j in range(len(self.cartas)):
                if self.cartas[j].idFecha == self.cartasQuery[indiceCartasQuery].idFecha:
                    self.cartas[j].getPunto(punto.nombre).sentido = punto.sentido
                    break
        for asteroide in self.cartasQuery[indiceCartasQuery].asteroides:
            # Set Retrogrados|Directos
            if indiceCartasQuery == 0:
                asteroideAnguloSiguiente = self.cartasQuery[indiceCartasQuery + 1].getPunto(asteroide.nombre + '.anguloReal')#[indiceCartasQuery + 1]
                diferencia = asteroideAnguloSiguiente - asteroide.anguloReal
            elif indiceCartasQuery > 0:
                asteroideAnguloAnterior = self.cartasQuery[indiceCartasQuery - 1].getPunto(asteroide.nombre + '.anguloReal')#[indiceCartasQuery - 1]
                diferencia = asteroide.anguloReal - asteroideAnguloAnterior
            if diferencia <= 0:
                asteroide.sentido = 'retrogrado'
            elif diferencia > 0:
                asteroide.sentido = 'directo'
            # Cambia Planeta de signo?
            if indiceCartasQuery > 0:
                asteroideSignoNombreAnterior = self.cartasQuery[indiceCartasQuery - 1].getPunto(asteroide.nombre + '.signo.nombre')#[indiceCartasQuery - 1]
            for j in range(len(self.cartas)):
                if self.cartas[j].idFecha == self.cartasQuery[indiceCartasQuery].idFecha:
                    self.cartas[j].getPunto(asteroide.nombre).sentido = asteroide.sentido
                    break
        '''for arabigo in self.cartasQuery[indiceCartasQuery].arabigos:
            if arabigo.nombre == 'propiedades-b':
                cualquier_cosa = 0
            else:
                # Set Retrogrados|Directos
                if indiceCartasQuery == 0:
                    arabigoAnguloSiguiente = self.cartasQuery[indiceCartasQuery + 1].getPunto(arabigo.nombre + '.anguloReal')#[indiceCartasQuery + 1]
                    diferencia = arabigoAnguloSiguiente - arabigo.anguloReal
                elif indiceCartasQuery > 0:
                    arabigoAnguloAnterior = self.cartasQuery[indiceCartasQuery - 1].getPunto(arabigo.nombre + '.anguloReal')#[indiceCartasQuery - 1]
                    diferencia = arabigo.anguloReal - arabigoAnguloAnterior
                if diferencia <= 0:
                    arabigo.sentido = 'retrogrado'
                elif diferencia > 0:
                    arabigo.sentido = 'directo'
                # Cambia Planeta de signo?
                if indiceCartasQuery > 0:
                    arabigoSignoNombreAnterior = self.cartasQuery[indiceCartasQuery - 1].getPunto(arabigo.nombre + '.signo.nombre')#[indiceCartasQuery - 1]
                for j in range(len(self.cartas)):
                    if self.cartas[j].idFecha == self.cartasQuery[indiceCartasQuery].idFecha:
                        self.cartas[j].getPunto(arabigo.nombre).sentido = arabigo.sentido
                        break
        '''
        '''
        # Analisis Casas
        for casa in self.cartasQuery[indiceCartasQuery].casas:
            if indiceCartasQuery > 0:
                casaSignoNombreAnterior = self.getCartas(casa.nombre + '.signo.nombre')[indiceCartasQuery - 1]
                if casaSignoNombreAnterior != casa.signo.nombre:
                    print('Casa', casa.nombre, 'cambia de,', casaSignoNombreAnterior, 'a', casa.signo.nombre)
        '''
        
    def getCartas(self, parametro: str) -> list:
        """Devuelve el valor del parámetro indicado para todas las cartas de la secuencia.

        Equivale a llamar ``carta.getPunto(parametro)`` para cada carta en
        ``self.cartas`` y devolver los resultados como lista ordenada por índice.

        Ejemplo de uso::

            secuenciaAstral.getCartas('ascendente.anguloReal')[0]
            secuenciaAstral.getCartas('luna.signo.nombre')[2]

        Args:
            parametro: Ruta de atributo en formato 'objeto' o 'objeto.atributo'
                o 'objeto.atributo.subatributo' (ej. 'sol.signo.nombre').

        Returns:
            Lista con un valor por carta, en el mismo orden que ``self.cartas``.
        """
        respuesta = []
        for i in range(len(self.cartas)):
            respuesta.append(self.cartas[i].getPunto(parametro))
        return respuesta

    def setInstantanea(self, indiceCarta: int) -> None:
        """Calcula los ángulos de animación y escribe los keyframes en Blender.

        Para cada carta de la secuencia:
        1. Calcula el ``deltaAnguloCarta`` y ``anguloCarta`` de cada objeto
           (signos, planetas, puntos, asteroides, casas) usando la posición del
           Ascendente como referencia de rotación.
        2. Asigna órbitas posicionales a los objetos en la primera carta (índice 0).
        3. Escribe en Blender: traslaciones, escalas, clonaciones de Platónico,
           luces, visibilidad de directo/retrógrado y keyframes de rotación.

        El bloque completo está envuelto en try/except para que un error en una
        carta no detenga la animación del resto de la secuencia.

        Args:
            indiceCarta: Índice de la carta en ``self.cartas``.
        """
        print(f'setInstantanea carta: {indiceCarta} | frame: {indiceCarta * self.constante}')
        try:
            anguloAscendente = self.getCartas('ascendente.anguloReal')[indiceCarta]
            indiceSignoAscendente = self.getCartas('ascendente.signo.indice')[indiceCarta]
            if indiceCarta > 0:
                indiceSignoAscendenteAnterior = self.getCartas('ascendente.signo.indice')[indiceCarta - 1]
                anguloAscendenteAnterior = self.getCartas('ascendente.anguloReal')[indiceCarta - 1]

            # CALCULOS
            # Rotacion Signos
            for signo in self.cartas[indiceCarta].signos:
                if indiceCarta > 0:
                    signoAnguloCartaAnterior = self.getCartas(signo.nombre + '.anguloCarta')[indiceCarta - 1]
                    if indiceSignoAscendente == indiceSignoAscendenteAnterior:
                        signo.deltaAnguloCarta = (-anguloAscendenteAnterior + anguloAscendente)
                    else:
                        signo.deltaAnguloCarta = (30 - anguloAscendenteAnterior + anguloAscendente)
                    signo.anguloCarta += signoAnguloCartaAnterior
                else:
                    signo.deltaAnguloCarta = (signo.anguloInicialReal)
                    signo.deltaAnguloCarta += (30 * indiceSignoAscendente)
                    signo.deltaAnguloCarta += (anguloAscendente)
                signo.anguloCarta += signo.deltaAnguloCarta
            # Rotacion Planetas
            for planeta in self.cartas[indiceCarta].planetas:
                if indiceCarta > 0:
                    planetaAnguloCartaAnterior = self.getCartas(planeta.nombre + '.anguloCarta')[indiceCarta - 1]
                    planeta.deltaAnguloCarta = (planeta.signo.anguloCarta) - planetaAnguloCartaAnterior
                    planeta.deltaAnguloCarta += (15)
                    planeta.deltaAnguloCarta -= (planeta.anguloReal)
                else:
                    planeta.deltaAnguloCarta = (planeta.signo.deltaAnguloCarta)
                    planeta.deltaAnguloCarta += (15)
                    planeta.deltaAnguloCarta -= (planeta.anguloReal)
                    #if planeta.nombre == 'luna':
                planeta.anguloCarta += planeta.deltaAnguloCarta
                if indiceCarta > 0:
                    planeta.anguloCarta += planetaAnguloCartaAnterior
            # Rotacion Puntos
            for punto in self.cartas[indiceCarta].puntos:
                if indiceCarta > 0:
                    puntoAnguloCartaAnterior = self.getCartas(punto.nombre + '.anguloCarta')[indiceCarta - 1]
                    punto.deltaAnguloCarta = (punto.signo.anguloCarta) - puntoAnguloCartaAnterior
                    punto.deltaAnguloCarta += (15)
                    punto.deltaAnguloCarta -= (punto.anguloReal)
                else:
                    punto.deltaAnguloCarta = (punto.signo.deltaAnguloCarta)
                    punto.deltaAnguloCarta += (15)
                    punto.deltaAnguloCarta -= (punto.anguloReal)
                punto.anguloCarta += punto.deltaAnguloCarta
                if indiceCarta > 0:
                    punto.anguloCarta += puntoAnguloCartaAnterior
            # Rotacion Asteroides
            for asteroide in self.cartas[indiceCarta].asteroides:
                if indiceCarta > 0:
                    asteroideAnguloCartaAnterior = self.getCartas(asteroide.nombre + '.anguloCarta')[indiceCarta - 1]
                    asteroide.deltaAnguloCarta = (asteroide.signo.anguloCarta) - asteroideAnguloCartaAnterior
                    asteroide.deltaAnguloCarta += (15)
                    asteroide.deltaAnguloCarta -= (asteroide.anguloReal)
                else:
                    asteroide.deltaAnguloCarta = (asteroide.signo.deltaAnguloCarta)
                    asteroide.deltaAnguloCarta += (15)
                    asteroide.deltaAnguloCarta -= (asteroide.anguloReal)
                asteroide.anguloCarta += asteroide.deltaAnguloCarta
                if indiceCarta > 0:
                    asteroide.anguloCarta += asteroideAnguloCartaAnterior
            # Rotacion Casas
            for casa in self.cartas[indiceCarta].casas:
                if indiceCarta > 0:
                    casaAnguloCartaAnterior = self.getCartas(casa.nombre + '.anguloCarta')[indiceCarta - 1]
                    casa.deltaAnguloCarta = (casa.signo.anguloCarta) - casaAnguloCartaAnterior
                    casa.deltaAnguloCarta += (15)
                    casa.deltaAnguloCarta -= (casa.anguloReal)
                else:
                    casa.deltaAnguloCarta = (casa.signo.deltaAnguloCarta)
                    casa.deltaAnguloCarta += (15)
                    casa.deltaAnguloCarta -= (casa.anguloReal)
                casa.anguloCarta += casa.deltaAnguloCarta
                if indiceCarta > 0:
                    casa.anguloCarta += casaAnguloCartaAnterior
            # Rotacion Arabigos
            '''for arabigo in self.cartas[indiceCarta].arabigos:
                if arabigo.nombre != 'propiedades-b' and self.pasaAdelante(arabigo.nombre):
                    if indiceCarta > 0:
                        arabigoAnguloCartaAnterior = self.getCartas(arabigo.nombre + '.anguloCarta')[indiceCarta - 1]
                        arabigo.deltaAnguloCarta = (arabigo.signo.anguloCarta) - arabigoAnguloCartaAnterior
                        arabigo.deltaAnguloCarta += (15)
                        arabigo.deltaAnguloCarta -= (arabigo.anguloReal)
                    else:
                        arabigo.deltaAnguloCarta = (arabigo.signo.deltaAnguloCarta)
                        arabigo.deltaAnguloCarta += (15)
                        arabigo.deltaAnguloCarta -= (arabigo.anguloReal)
                    arabigo.anguloCarta += arabigo.deltaAnguloCarta
                    if indiceCarta > 0:
                        arabigo.anguloCarta += arabigoAnguloCartaAnterior
                    #if (indiceCarta == 1 or indiceCarta == 2 or indiceCarta == 3) and arabigo.nombre == 'luna':
            '''
            # Traslacion Signos
            for signo in self.cartas[indiceCarta].signos:
                if indiceCarta == 0:
                    signo.indiceOrbitaCarta = 8
                    signo.orbitaPosicional = self.orbitaInicial + (signo.indiceOrbitaCarta - 1) * self.deltaOrbita
                    signo.orbitaAltura = 28
                    signo.escalaRuna = 1.6
                    signo.escalaPlatonico = 3.0
            # Traslacion
            if indiceCarta == 0:
                objetosOrdenados = self.clonar(self.cartas[indiceCarta].planetas)
                objetosOrdenados += self.clonar(self.cartas[indiceCarta].asteroides)
                objetosOrdenados += self.clonar(self.cartas[indiceCarta].arabigos)
                self.selectionSort(objetosOrdenados)
                self.indiceOrbitaActual = 1
            # Traslacion Planetas
            for planeta in self.cartas[indiceCarta].planetas:
                if indiceCarta == 0:
                    planeta.indiceOrbitaCarta = self.sondaOrbita(planeta, indiceCarta, self.indiceOrbitaActual, objetosOrdenados)
                    planeta.orbitaPosicional = self.orbitaInicial + (planeta.indiceOrbitaCarta - 1) * self.deltaOrbita
                    planeta.orbitaAltura = 0 + 5
                    planeta.escalaRuna = 1.20
                    #objetosOrdenados = self.clonar(self.cartas[indiceCarta].planetas)
                    #self.selectionSort(objetosOrdenados)
            # Traslacion Puntos
            for punto in self.cartas[indiceCarta].puntos:
                if indiceCarta == 0:
                    punto.indiceOrbitaCarta = 7 #self.sondaOrbita(punto, indiceCarta, self.indiceOrbitaActual, objetosOrdenados)
                    punto.orbitaPosicional = self.orbitaInicial + (punto.indiceOrbitaCarta - 1) * self.deltaOrbita
                    if punto.nombre == 'ascendente' or punto.nombre == 'medioCielo':
                        punto.orbitaAltura = 10
                    else:
                        punto.orbitaAltura = 8.5
                    punto.escalaRuna = 1.20
                    #objetosOrdenados = self.clonar(self.cartas[indiceCarta].puntos)
                    #self.selectionSort(objetosOrdenados)
            # Traslacion Asteroides
            for asteroide in self.cartas[indiceCarta].asteroides:
                if indiceCarta == 0:
                    asteroide.indiceOrbitaCarta = self.sondaOrbita(asteroide, indiceCarta, self.indiceOrbitaActual, objetosOrdenados)
                    asteroide.orbitaPosicional = self.orbitaInicial + (asteroide.indiceOrbitaCarta - 1) * self.deltaOrbita
                    asteroide.orbitaAltura = 0 + 5
                    asteroide.escalaRuna = 1.20
                    asteroide.escalaPlatonico = 1.04
            # Traslacion Arabigos
            '''for arabigo in self.cartas[indiceCarta].arabigos:
                if arabigo.nombre != 'propiedades-b' and self.pasaAdelante(arabigo.nombre):
                    if indiceCarta == 0:
                        arabigo.indiceOrbitaCarta = self.sondaOrbita(arabigo, indiceCarta, self.indiceOrbitaActual, objetosOrdenados)
                        arabigo.orbitaPosicional = self.orbitaInicial + (arabigo.indiceOrbitaCarta - 1) * self.deltaOrbita
                        arabigo.orbitaAltura = 0 + 5
                        arabigo.escalaRuna = 1.20
                        arabigo.escalaPlatonico = 0.159
                        arabigo.escalaSubRuna = 0.65
                        arabigo.subRuna1 = [0.55, 0, 0]
                        #objetosOrdenados = np.concatenate(self.clonar(self.cartas[indiceCarta].planetas), self.clonar(self.cartas[indiceCarta].arabigos))
                        #self.selectionSort(objetosOrdenados)
            '''
            # GRAFICA
            # Inicializacion de escena
            if indiceCarta == 0:
                self.setToTransform('tierra')
                # Traslacion tierra
                bpy.ops.transform.translate(value=(-bpy.data.objects['tierra'].location.x, -bpy.data.objects['tierra'].location.y, -bpy.data.objects['tierra'].location.z))

            modo = 'galactico' # galactico|terrestre

            for signo in self.cartas[indiceCarta].signos:
                if indiceCarta == 0:
                    self.setToTransform(signo.nombre)
                    # Traslacion signo
                    bpy.ops.transform.translate(value=(-bpy.data.objects[signo.nombre].location.x, -bpy.data.objects[signo.nombre].location.y, -bpy.data.objects[signo.nombre].location.z))

                    self.setToTransform(signo.nombre + 'Runa')
                    # Traslacion Runa
                    bpy.ops.transform.translate(value=(signo.orbitaPosicional, 0, signo.orbitaAltura))
                    # Escala Runa
                    bpy.ops.transform.resize(value=(signo.escalaRuna, signo.escalaRuna, signo.escalaRuna), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
                    bpy.data.objects[signo.nombre + 'Runa'].keyframe_insert(data_path="scale", frame = indiceCarta * self.constante)
                    if modo == 'terrestre':
                        # Rotacion Runa
                        bpy.ops.transform.rotate(value=(90 * math.pi / 180), orient_axis='Y')
                        bpy.data.objects[signo.nombre + 'Runa'].keyframe_insert(data_path='rotation_euler', frame = indiceCarta * self.constante)

                    # Clonacion de Platonico
                    ob = bpy.data.objects[signo.elemento + 'Elemento'].copy()
                    ob.name = signo.nombre + 'Elemento'
                    ob.parent = bpy.data.objects[signo.nombre + 'Platonico']
                    bpy.data.collections[signo.nombre].objects.link(ob)

                    self.setToTransform(signo.nombre + 'Platonico')
                    # Traslacion Platonico
                    bpy.ops.transform.translate(value=(signo.orbitaPosicional, 0, signo.orbitaAltura))

                    self.setToTransform(signo.nombre + 'Elemento')
                    # Escala Elemento
                    bpy.ops.transform.resize(value=(signo.escalaPlatonico, signo.escalaPlatonico, signo.escalaPlatonico), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
                    bpy.data.objects[signo.nombre + 'Elemento'].keyframe_insert(data_path="scale", frame = indiceCarta * self.constante)

                    # Luces Platonico
                    luz = bpy.data.objects['Point'].copy()
                    luz.data = bpy.data.objects['Point'].data.copy()
                    luz.name = signo.nombre + 'PlatonicoLuz'
                    luz.parent = bpy.data.objects[signo.nombre + 'Platonico']
                    bpy.data.collections[signo.nombre].objects.link(luz)
                    self.setToTransform(signo.nombre + 'PlatonicoLuz')
                    if modo == 'terrestre':
                        bpy.data.objects[signo.nombre + 'PlatonicoLuz'].data.type = 'POINT'
                        # Traslacion PlatonicoLuz
                        if signo.elemento == 'fuego':
                            bpy.ops.transform.translate(value=(-1.5, 0, 0))
                            bpy.data.objects[signo.nombre + 'PlatonicoLuz'].data.energy = 2000
                        elif signo.elemento == 'tierra':
                            bpy.ops.transform.translate(value=(-1.5, 0, 0))
                            bpy.data.objects[signo.nombre + 'PlatonicoLuz'].data.energy = 2000
                        elif signo.elemento == 'aire':
                            bpy.ops.transform.translate(value=(-1.5, 0, 0))
                            bpy.data.objects[signo.nombre + 'PlatonicoLuz'].data.energy = 2000
                        elif signo.elemento == 'agua':
                            bpy.ops.transform.translate(value=(-1.5, 0, 0))
                            bpy.data.objects[signo.nombre + 'PlatonicoLuz'].data.energy = 2000
                        # Rotacion PlatonicoLuz
                        bpy.ops.transform.rotate(value=(90 * math.pi / 180), orient_axis='Y')
                        bpy.data.objects[signo.nombre + 'PlatonicoLuz'].keyframe_insert(data_path='rotation_euler', frame = indiceCarta * self.constante)
                    elif modo == 'galactico': # Hay que ajustar
                        bpy.data.objects[signo.nombre + 'PlatonicoLuz'].data.type = 'AREA'
                        # Traslacion PlatonicoLuz
                        if signo.elemento == 'fuego':
                            bpy.ops.transform.translate(value=(0, 0, 16.5))
                            bpy.data.objects[signo.nombre + 'PlatonicoLuz'].data.energy = 2000
                        elif signo.elemento == 'tierra':
                            bpy.ops.transform.translate(value=(0, 0, 9))
                            bpy.data.objects[signo.nombre + 'PlatonicoLuz'].data.energy = 2000
                        elif signo.elemento == 'aire':
                            bpy.ops.transform.translate(value=(0, 0, 14.5))
                            bpy.data.objects[signo.nombre + 'PlatonicoLuz'].data.energy = 2000
                        elif signo.elemento == 'agua':
                            bpy.ops.transform.translate(value=(0, 0, 11))
                            bpy.data.objects[signo.nombre + 'PlatonicoLuz'].data.energy = 2000

                self.setToTransform(signo.nombre)
                # Rotacion signo
                bpy.ops.transform.rotate(value=((signo.deltaAnguloCarta) * math.pi / 180))
                bpy.data.objects[signo.nombre].keyframe_insert(data_path='rotation_euler', frame = indiceCarta * self.constante)

            for planeta in self.cartas[indiceCarta].planetas:
                if indiceCarta == 0:
                    self.setToTransform(planeta.nombre)
                    # Traslacion planeta
                    bpy.ops.transform.translate(value=(-bpy.data.objects[planeta.nombre].location.x, -bpy.data.objects[planeta.nombre].location.y, -bpy.data.objects[planeta.nombre].location.z))

                    self.setToTransform(planeta.nombre + 'Runa')
                    # Traslacion Runa
                    bpy.ops.transform.translate(value=(planeta.orbitaPosicional, 0, planeta.orbitaAltura))
                    # Escala Runa
                    bpy.ops.transform.resize(value=(planeta.escalaRuna, planeta.escalaRuna, planeta.escalaRuna), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
                    bpy.data.objects[planeta.nombre + 'Runa'].keyframe_insert(data_path="scale", frame = indiceCarta * self.constante)
                    if modo == 'terrestre':
                        # Rotacion Runa
                        bpy.ops.transform.rotate(value=(60 * math.pi / 180), orient_axis='Y')
                        bpy.data.objects[planeta.nombre + 'Runa'].keyframe_insert(data_path='rotation_euler', frame = indiceCarta * self.constante)

                    # Clonacion de Platonico
                    ob = bpy.data.objects['prana' + 'Elemento'].copy()
                    ob.name = planeta.nombre + 'Elemento'
                    ob.parent = bpy.data.objects[planeta.nombre + 'Platonico']
                    bpy.data.collections[planeta.nombre].objects.link(ob)

                    self.setToTransform(planeta.nombre + 'Platonico')
                    # Traslacion Platonico
                    bpy.ops.transform.translate(value=(planeta.orbitaPosicional, 0, planeta.orbitaAltura))

                    # Escala Elemento

                    # Luces Platonico
                    luz = bpy.data.objects['Point'].copy()
                    luz.data = bpy.data.objects['Point'].data.copy()
                    luz.name = planeta.nombre + 'PlatonicoLuz'
                    luz.parent = bpy.data.objects[planeta.nombre + 'Platonico']
                    bpy.data.collections[planeta.nombre].objects.link(luz)
                    self.setToTransform(planeta.nombre + 'PlatonicoLuz')
                    if modo == 'terrestre':
                        bpy.data.objects[planeta.nombre + 'PlatonicoLuz'].data.type = 'POINT'
                        # Traslacion PlatonicoLuz
                        bpy.ops.transform.translate(value=(-1.5, 0, 0))
                        bpy.data.objects[planeta.nombre + 'PlatonicoLuz'].data.energy = 2000
                        # Rotacion PlatonicoLuz
                        bpy.ops.transform.rotate(value=(90 * math.pi / 180), orient_axis='Y')
                        bpy.data.objects[planeta.nombre + 'PlatonicoLuz'].keyframe_insert(data_path='rotation_euler', frame = indiceCarta * self.constante)
                    elif modo == 'galactico': # Hay que ajustar
                        bpy.data.objects[planeta.nombre + 'PlatonicoLuz'].data.type = 'AREA'
                        # Traslacion PlatonicoLuz
                        bpy.ops.transform.translate(value=(0, 0, 3.3))
                        bpy.data.objects[planeta.nombre + 'PlatonicoLuz'].data.energy = 2000

                # hide_viewport directo|retrogrado
                if planeta.sentido == 'directo':
                    bpy.data.objects[planeta.nombre + '-directo'].hide_viewport = False
                    bpy.data.objects[planeta.nombre + '-directo'].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)
                    bpy.data.objects[planeta.nombre + '-retrogrado'].hide_viewport = True
                    bpy.data.objects[planeta.nombre + '-retrogrado'].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)
                elif planeta.sentido == 'retrogrado':
                    bpy.data.objects[planeta.nombre + '-directo'].hide_viewport = True
                    bpy.data.objects[planeta.nombre + '-directo'].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)
                    bpy.data.objects[planeta.nombre + '-retrogrado'].hide_viewport = False
                    bpy.data.objects[planeta.nombre + '-retrogrado'].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)

                self.setToTransform(planeta.nombre)
                # Rotacion planeta
                bpy.ops.transform.rotate(value=((planeta.deltaAnguloCarta) * math.pi / 180))
                bpy.data.objects[planeta.nombre].keyframe_insert(data_path='rotation_euler', frame = indiceCarta * self.constante)
            for punto in self.cartas[indiceCarta].puntos:
                if punto.nombre != 'nodoSur':
                    if indiceCarta == 0:
                        self.setToTransform(punto.nombre)
                        # Traslacion punto
                        bpy.ops.transform.translate(value=(-bpy.data.objects[punto.nombre].location.x, -bpy.data.objects[punto.nombre].location.y, -bpy.data.objects[punto.nombre].location.z))

                        self.setToTransform(punto.nombre + 'Runa')
                        # Traslacion Runa
                        bpy.ops.transform.translate(value=(punto.orbitaPosicional, 0, punto.orbitaAltura))
                        # Escala Runa
                        bpy.ops.transform.resize(value=(punto.escalaRuna, punto.escalaRuna, punto.escalaRuna), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
                        bpy.data.objects[punto.nombre + 'Runa'].keyframe_insert(data_path="scale", frame = indiceCarta * self.constante)
                        if modo == 'terrestre':
                            # Rotacion Runa
                            bpy.ops.transform.rotate(value=(60 * math.pi / 180), orient_axis='Y')
                            bpy.data.objects[punto.nombre + 'Runa'].keyframe_insert(data_path='rotation_euler', frame = indiceCarta * self.constante)

                        # Clonacion de Platonico
                        #ob = bpy.data.objects['prana' + 'Elemento'].copy()
                        #ob.name = punto.nombre + 'Elemento'
                        #ob.parent = bpy.data.objects[punto.nombre + 'Platonico']
                        #bpy.data.collections[punto.nombre].objects.link(ob)

                        self.setToTransform(punto.nombre + 'Platonico')
                        # Traslacion Platonico
                        bpy.ops.transform.translate(value=(punto.orbitaPosicional, 0, punto.orbitaAltura))

                        # Escala Elemento

                        # Luces Platonico
                        luz = bpy.data.objects['Point'].copy()
                        luz.data = bpy.data.objects['Point'].data.copy()
                        luz.name = punto.nombre + 'PlatonicoLuz'
                        luz.parent = bpy.data.objects[punto.nombre + 'Platonico']
                        bpy.data.collections[punto.nombre].objects.link(luz)
                        self.setToTransform(punto.nombre + 'PlatonicoLuz')
                        if modo == 'terrestre':
                            bpy.data.objects[punto.nombre + 'PlatonicoLuz'].data.type = 'POINT'
                            # Traslacion PlatonicoLuz
                            bpy.ops.transform.translate(value=(-1.5, 0, 0))
                            bpy.data.objects[punto.nombre + 'PlatonicoLuz'].data.energy = 2000
                            # Rotacion PlatonicoLuz
                            bpy.ops.transform.rotate(value=(90 * math.pi / 180), orient_axis='Y')
                            bpy.data.objects[punto.nombre + 'PlatonicoLuz'].keyframe_insert(data_path='rotation_euler', frame = indiceCarta * self.constante)
                        elif modo == 'galactico': # Hay que ajustar
                            bpy.data.objects[punto.nombre + 'PlatonicoLuz'].data.type = 'SPOT'
                            # Traslacion PlatonicoLuz
                            bpy.ops.transform.translate(value=(0, 0, 6))
                            bpy.data.objects[punto.nombre + 'PlatonicoLuz'].data.energy = 15000

                    # hide_viewport directo|retrogrado
                    if punto.sentido == 'directo':
                        bpy.data.objects[punto.nombre + '-directo'].hide_viewport = False
                        bpy.data.objects[punto.nombre + '-directo'].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)
                        bpy.data.objects[punto.nombre + '-retrogrado'].hide_viewport = True
                        bpy.data.objects[punto.nombre + '-retrogrado'].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)
                    elif punto.sentido == 'retrogrado':
                        bpy.data.objects[punto.nombre + '-directo'].hide_viewport = True
                        bpy.data.objects[punto.nombre + '-directo'].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)
                        bpy.data.objects[punto.nombre + '-retrogrado'].hide_viewport = False
                        bpy.data.objects[punto.nombre + '-retrogrado'].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)

                    self.setToTransform(punto.nombre)
                    # Rotacion punto
                    bpy.ops.transform.rotate(value=((punto.deltaAnguloCarta) * math.pi / 180))
                    bpy.data.objects[punto.nombre].keyframe_insert(data_path='rotation_euler', frame = indiceCarta * self.constante)
            for asteroide in self.cartas[indiceCarta].asteroides:
                if asteroide.nombre != 'eris':
                    if indiceCarta == 0:
                        self.setToTransform(asteroide.nombre)
                        # Traslacion asteroide
                        bpy.ops.transform.translate(value=(-bpy.data.objects[asteroide.nombre].location.x, -bpy.data.objects[asteroide.nombre].location.y, -bpy.data.objects[asteroide.nombre].location.z))

                        self.setToTransform(asteroide.nombre + 'Runa')
                        # Traslacion Runa
                        bpy.ops.transform.translate(value=(asteroide.orbitaPosicional, 0, asteroide.orbitaAltura))
                        # Escala Runa
                        bpy.ops.transform.resize(value=(asteroide.escalaRuna, asteroide.escalaRuna, asteroide.escalaRuna), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
                        bpy.data.objects[asteroide.nombre + 'Runa'].keyframe_insert(data_path="scale", frame = indiceCarta * self.constante)  # BUG ORIGINAL: punto.nombre → asteroide.nombre
                        if modo == 'terrestre':
                            # Rotacion Runa
                            bpy.ops.transform.rotate(value=(60 * math.pi / 180), orient_axis='Y')
                            bpy.data.objects[asteroide.nombre + 'Runa'].keyframe_insert(data_path='rotation_euler', frame = indiceCarta * self.constante)  # BUG ORIGINAL: punto.nombre → asteroide.nombre

                        # Clonacion de Platonico
                        ob = bpy.data.objects['prana' + 'Elemento'].copy()
                        ob.name = asteroide.nombre + 'Elemento'
                        ob.parent = bpy.data.objects[asteroide.nombre + 'Platonico']
                        bpy.data.collections[asteroide.nombre].objects.link(ob)

                        self.setToTransform(asteroide.nombre + 'Platonico')
                        # Traslacion Platonico
                        bpy.ops.transform.translate(value=(asteroide.orbitaPosicional, 0, asteroide.orbitaAltura))

                        # Escala Platonico
                        bpy.ops.transform.resize(value=(asteroide.escalaPlatonico, asteroide.escalaPlatonico, asteroide.escalaPlatonico), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
                        bpy.data.objects[asteroide.nombre + 'Platonico'].keyframe_insert(data_path="scale", frame = indiceCarta * self.constante)

                        # Luces Platonico
                        luz = bpy.data.objects['Point'].copy()
                        luz.data = bpy.data.objects['Point'].data.copy()
                        luz.name = asteroide.nombre + 'PlatonicoLuz'
                        luz.parent = bpy.data.objects[asteroide.nombre + 'Platonico']
                        bpy.data.collections[asteroide.nombre].objects.link(luz)
                        self.setToTransform(asteroide.nombre + 'PlatonicoLuz')
                        if modo == 'terrestre':
                            bpy.data.objects[asteroide.nombre + 'PlatonicoLuz'].data.type = 'POINT'
                            # Traslacion PlatonicoLuz
                            bpy.ops.transform.translate(value=(-1.5, 0, 0))
                            bpy.data.objects[asteroide.nombre + 'PlatonicoLuz'].data.energy = 2000
                            # Rotacion PlatonicoLuz
                            bpy.ops.transform.rotate(value=(90 * math.pi / 180), orient_axis='Y')
                            bpy.data.objects[asteroide.nombre + 'PlatonicoLuz'].keyframe_insert(data_path='rotation_euler', frame = indiceCarta * self.constante)
                        elif modo == 'galactico': # Hay que ajustar
                            bpy.data.objects[asteroide.nombre + 'PlatonicoLuz'].data.type = 'AREA'
                            # Traslacion PlatonicoLuz
                            bpy.ops.transform.translate(value=(0, 0, 3.3))
                            bpy.data.objects[asteroide.nombre + 'PlatonicoLuz'].data.energy = 2000

                    # hide_viewport directo|retrogrado
                    if asteroide.sentido == 'directo':
                        bpy.data.objects[asteroide.nombre + '-directo'].hide_viewport = False
                        bpy.data.objects[asteroide.nombre + '-directo'].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)
                        bpy.data.objects[asteroide.nombre + '-retrogrado'].hide_viewport = True
                        bpy.data.objects[asteroide.nombre + '-retrogrado'].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)
                    elif asteroide.sentido == 'retrogrado':
                        bpy.data.objects[asteroide.nombre + '-directo'].hide_viewport = True
                        bpy.data.objects[asteroide.nombre + '-directo'].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)
                        bpy.data.objects[asteroide.nombre + '-retrogrado'].hide_viewport = False
                        bpy.data.objects[asteroide.nombre + '-retrogrado'].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)

                    self.setToTransform(asteroide.nombre)
                    # Rotacion asteroide
                    bpy.ops.transform.rotate(value=((asteroide.deltaAnguloCarta) * math.pi / 180))
                    bpy.data.objects[asteroide.nombre].keyframe_insert(data_path='rotation_euler', frame = indiceCarta * self.constante)
            for casa in self.cartas[indiceCarta].casas:
                if indiceCarta == 0:
                    self.setToTransform(casa.nombre)
                    # Clonacion de Disco para casa N ... para alcanzar su magnitud energetica
                    for grado in range(self.numeroDiscosCasa):
                        ob = bpy.data.objects['casa ' + str(casa.indice) + 'Disco1'].copy()
                        ob.name = 'casa ' + str(casa.indice) + 'Disco' + str(grado + 2)
                        bpy.data.collections['casas'].objects.link(ob)
                        ob.delta_rotation_euler.z = ((grado + 1) * math.pi / 180)

                self.setToTransform(casa.nombre)
                # Rotacion casa
                bpy.ops.transform.rotate(value=((casa.deltaAnguloCarta) * math.pi / 180))
                bpy.data.objects[casa.nombre].keyframe_insert(data_path='rotation_euler', frame = indiceCarta * self.constante)
                # hide_viewport DiscoN
                for casaTemp in self.cartas[indiceCarta].casas:
                    if (casa.indice == 12 and casaTemp.indice == 1) or casaTemp.indice == casa.indice + 1:
                        magnitudAngular = casa.anguloCarta - casaTemp.anguloCarta
                        if casa.anguloCarta - casaTemp.anguloCarta < 0:
                            magnitudAngular += 360
                        pasosAngulares = math.floor(magnitudAngular)
                        for angulo in range(self.numeroDiscosCasa + 1):
                            if angulo <= pasosAngulares:
                                bpy.data.objects[casa.nombre + "Disco" + str(angulo + 1)].hide_viewport = False
                            else:
                                bpy.data.objects[casa.nombre + "Disco" + str(angulo + 1)].hide_viewport = True
                            bpy.data.objects[casa.nombre + "Disco" + str(angulo + 1)].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)
                        break

            # Construccion de arabigos
            '''for arabigo in self.cartas[indiceCarta].arabigos:
                if arabigo.nombre != 'propiedades-b' and self.pasaAdelante(arabigo.nombre):
                    if indiceCarta == 0:
                        if not arabigo.tieneRuna:
                            otrosPuntos = arabigo[self.cartas[indiceCarta].diaNoche]
                            try:
                                otroPuntoNombre = int(otrosPuntos[0])#self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).anguloReal + -1 * (self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).signo.anguloInicialReal + 15)
                                factor1EsNumerico = True
                                #otroPuntoNombre = 'ascendente' # Cualquiera valido sirve aqui
                            except ValueError:
                                #temp = self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).anguloReal + -1 * (self.cartasQuery[indiceCartasQuery].getPunto(arabigo[diaNoche][j]).signo.anguloInicialReal + 15)
                                factor1EsNumerico = False
                                otroPuntoNombre = otrosPuntos[0]

                            # Temporal Clonacion de Aro de otro objeto (ascendente, sol, casa 1, infortunio)
                            ob = bpy.data.objects['sol' + 'Aro'].copy()
                            ob.data = bpy.data.objects['sol' + 'Aro'].data.copy()
                            ob.name = arabigo.nombre + 'Aro'
                            ob.parent = bpy.data.objects[arabigo.nombre + 'Runa']
                            bpy.data.collections[arabigo.nombre].objects.link(ob)
                            ob = bpy.data.objects.find(arabigo.nombre + 'Aro.001')
                            if ob > 0:
                                bpy.ops.object.select_all(action='DESELECT')
                                bpy.data.objects[arabigo.nombre + 'Aro.001'].select_set(True)
                                bpy.ops.object.delete()
                            
                            if not factor1EsNumerico:
                                # Clonacion de Aro de otro objeto (ascendente, sol, casa 1, infortunio)
                                ob = bpy.data.objects[otroPuntoNombre + 'Aro'].copy()
                                ob.data = bpy.data.objects[otroPuntoNombre + 'Aro'].data.copy()
                                ob.name = arabigo.nombre + '-' + otroPuntoNombre + 'Aro'
                                ob.parent = bpy.data.objects[arabigo.nombre + 'Runa']
                                bpy.data.collections[arabigo.nombre].objects.link(ob)
                                ob = bpy.data.objects.find(arabigo.nombre + '-' + otroPuntoNombre + 'Aro.001')
                                if ob > 0:
                                    bpy.ops.object.select_all(action='DESELECT')
                                    bpy.data.objects[arabigo.nombre + '-' + otroPuntoNombre + 'Aro.001'].select_set(True)
                                    bpy.ops.object.delete()
                                
                                self.setToTransform(arabigo.nombre + '-' + otroPuntoNombre + 'Aro')
                                # Traslacion SubRuna
                                bpy.ops.transform.translate(value=(arabigo.subRuna1))
                                # Escala SubRuna
                                bpy.ops.transform.resize(value=(arabigo.escalaSubRuna, arabigo.escalaSubRuna, arabigo.escalaSubRuna), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
                                bpy.data.objects[arabigo.nombre + 'Runa'].keyframe_insert(data_path="scale", frame = indiceCarta * self.constante)

                                # Clonacion de directo|retrogrado de otro objeto (ascendente, sol, casa 1, infortunio)
                                print(self.cartas[indiceCarta].getPunto(otroPuntoNombre).sentido)
                                ob = bpy.data.objects[otroPuntoNombre + '-' + self.cartas[indiceCarta].getPunto(otroPuntoNombre).sentido].copy()
                                ob.data = bpy.data.objects[otroPuntoNombre + '-' + self.cartas[indiceCarta].getPunto(otroPuntoNombre).sentido].data.copy()
                                ob.name = arabigo.nombre + '-' + otroPuntoNombre + '-' + self.cartas[indiceCarta].getPunto(otroPuntoNombre).sentido
                                ob.parent = bpy.data.objects[arabigo.nombre + 'Runa']
                                bpy.data.collections[arabigo.nombre].objects.link(ob)
                                ob = bpy.data.objects.find(arabigo.nombre + '-' + otroPuntoNombre + '-' + self.cartas[indiceCarta].getPunto(otroPuntoNombre).sentido + '.001')
                                if ob > 0:
                                    bpy.ops.object.select_all(action='DESELECT')
                                    bpy.data.objects[arabigo.nombre + '-' + otroPuntoNombre + '-' + self.cartas[indiceCarta].getPunto(otroPuntoNombre).sentido + '.001'].select_set(True)
                                    bpy.ops.object.delete()

                                self.setToTransform(arabigo.nombre + '-' + otroPuntoNombre + '-' + self.cartas[indiceCarta].getPunto(otroPuntoNombre).sentido)
                                # Traslacion SubRuna
                                bpy.ops.transform.translate(value=(arabigo.subRuna1))
                                # Escala SubRuna
                                bpy.ops.transform.resize(value=(arabigo.escalaSubRuna, arabigo.escalaSubRuna, arabigo.escalaSubRuna), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
                                bpy.data.objects[arabigo.nombre + 'Runa'].keyframe_insert(data_path="scale", frame = indiceCarta * self.constante)

                        self.setToTransform(arabigo.nombre)
                        # Traslacion arabigo
                        bpy.ops.transform.translate(value=(-bpy.data.objects[arabigo.nombre].location.x, -bpy.data.objects[arabigo.nombre].location.y, -bpy.data.objects[arabigo.nombre].location.z))

                        self.setToTransform(arabigo.nombre + 'Runa')
                        # Traslacion Runa
                        bpy.ops.transform.translate(value=(arabigo.orbitaPosicional, 0, arabigo.orbitaAltura))
                        # Escala Runa
                        bpy.ops.transform.resize(value=(arabigo.escalaRuna, arabigo.escalaRuna, arabigo.escalaRuna), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
                        bpy.data.objects[arabigo.nombre + 'Runa'].keyframe_insert(data_path="scale", frame = indiceCarta * self.constante)
                        if modo == 'terrestre':
                            # Rotacion Runa
                            bpy.ops.transform.rotate(value=(60 * math.pi / 180), orient_axis='Y')
                            bpy.data.objects[arabigo.nombre + 'Runa'].keyframe_insert(data_path='rotation_euler', frame = indiceCarta * self.constante)

                        # Clonacion de Platonico
                        ob = bpy.data.objects['prana' + 'Elemento'].copy()
                        ob.name = arabigo.nombre + 'Elemento'
                        ob.parent = bpy.data.objects[arabigo.nombre + 'Platonico']
                        bpy.data.collections[arabigo.nombre].objects.link(ob)
                        ob = bpy.data.objects.find(arabigo.nombre + 'Elemento.001')
                        if ob > 0:
                            bpy.ops.object.select_all(action='DESELECT')
                            bpy.data.objects[arabigo.nombre + 'Elemento.001'].select_set(True)
                            bpy.ops.object.delete()

                        self.setToTransform(arabigo.nombre + 'Platonico')
                        # Traslacion Platonico
                        bpy.ops.transform.translate(value=(arabigo.orbitaPosicional, 0, arabigo.orbitaAltura))

                        # Escala Platonico
                        bpy.ops.transform.resize(value=(arabigo.escalaPlatonico, arabigo.escalaPlatonico, arabigo.escalaPlatonico), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
                        bpy.data.objects[arabigo.nombre + 'Platonico'].keyframe_insert(data_path="scale", frame = indiceCarta * self.constante)

                        # Luces Platonico
                        #luz = bpy.data.objects['Point'].copy()
                        #luz.data = bpy.data.objects['Point'].data.copy()
                        #luz.name = arabigo.nombre + 'PlatonicoLuz'
                        #luz.parent = bpy.data.objects[arabigo.nombre + 'Platonico']
                        #bpy.data.collections[arabigo.nombre].objects.link(luz)
                        #self.setToTransform(arabigo.nombre + 'PlatonicoLuz')
                        #if modo == 'terrestre':
                        #    bpy.data.objects[arabigo.nombre + 'PlatonicoLuz'].data.type = 'POINT'
                        #    # Traslacion PlatonicoLuz
                        #    bpy.ops.transform.translate(value=(-1.5, 0, 0))
                        #    bpy.data.objects[arabigo.nombre + 'PlatonicoLuz'].data.energy = 2000
                        #    # Rotacion PlatonicoLuz
                        #    bpy.ops.transform.rotate(value=(90 * math.pi / 180), orient_axis='Y')
                        #    bpy.data.objects[arabigo.nombre + 'PlatonicoLuz'].keyframe_insert(data_path='rotation_euler', frame = indiceCarta * self.constante)
                        #elif modo == 'galactico': # Hay que ajustar
                        #    bpy.data.objects[arabigo.nombre + 'PlatonicoLuz'].data.type = 'AREA'
                        #    # Traslacion PlatonicoLuz
                        #    bpy.ops.transform.translate(value=(0, 0, 3.3))
                        #    bpy.data.objects[arabigo.nombre + 'PlatonicoLuz'].data.energy = 2000

                    # hide_viewport Mas|Menos
                    #if arabigo.sentido == 'directo':
                    #    bpy.data.objects[arabigo.nombre + 'Mas'].hide_viewport = False
                    #    bpy.data.objects[arabigo.nombre + 'Mas'].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)
                    #    bpy.data.objects[arabigo.nombre + 'Menos'].hide_viewport = True
                    #    bpy.data.objects[arabigo.nombre + 'Menos'].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)
                    #elif arabigo.sentido == 'retrogrado':
                    #    bpy.data.objects[arabigo.nombre + 'Mas'].hide_viewport = True
                    #    bpy.data.objects[arabigo.nombre + 'Mas'].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)
                    #    bpy.data.objects[arabigo.nombre + 'Menos'].hide_viewport = False
                    #    bpy.data.objects[arabigo.nombre + 'Menos'].keyframe_insert(data_path="hide_viewport", frame = indiceCarta * self.constante)

                    self.setToTransform(arabigo.nombre)
                    # Rotacion arabigo
                    bpy.ops.transform.rotate(value=((arabigo.deltaAnguloCarta) * math.pi / 180))
                    bpy.data.objects[arabigo.nombre].keyframe_insert(data_path='rotation_euler', frame = indiceCarta * self.constante)
            '''
        except Exception as e:
            import traceback
            print('ERROR en carta', indiceCarta, ':', str(e))
            traceback.print_exc()
    def sondaOrbita(self, objeto, indiceCarta: int, indiceOrbitaActual: int,
                    objetosOrdenados: list) -> int:
        """Busca recursivamente la primera órbita disponible para un objeto.

        Un objeto cabe en una órbita si su ángulo de carta se separa al menos
        ``self.tolerancia`` grados de todos los objetos que ya ocupan esa órbita.
        Si no hay espacio, intenta la órbita siguiente (indiceOrbitaActual + 1).

        Args:
            objeto: Objeto celeste a ubicar (Planeta, Asteroide, Arabigo, etc.).
            indiceCarta: Índice de la carta actual (no usado directamente, pero
                se pasa en la llamada recursiva para trazabilidad).
            indiceOrbitaActual: Índice de la órbita que se está evaluando.
            objetosOrdenados: Lista de todos los objetos ya posicionados, ordenada
                por ``anguloCarta`` ascendente.

        Returns:
            Índice de la primera órbita en que el objeto cabe sin solaparse.
        """
        hayLugar = True
        objetosEnOrbita = []
        respuesta = ""
        #if objeto.nombre == 'ascendente' or objeto.nombre == 'medioCielo':
        #    indiceOrbitaActual = 5
        #if objeto.nombre == 'nodoNorte' or objeto.nombre == 'nodoSur':
        #    indiceOrbitaActual = 5
        #if objeto.nombre == 'paz':
        #    print()
        # Recojo los objetos que ya orbitan en indiceOrbitaActual
        for i in range(len(objetosOrdenados)):
            if objeto.nombre != objetosOrdenados[i].nombre:
                if objetosOrdenados[i].indiceOrbitaCarta == indiceOrbitaActual:
                    objetosEnOrbita.append(objetosOrdenados[i])
        
        # Busco lugar entre los objeto en orbita segun su angulo de posicionamiento
        for i in range(len(objetosEnOrbita)):
            # Caso 1: existe solo un objeto orbitando en este indiceOrbitaActual
            if len(objetosEnOrbita) == 1:
                if (objeto.anguloCarta - self.tolerancia) > objetosEnOrbita[i].anguloCarta:
                    respuesta = indiceOrbitaActual
                elif objeto.anguloCarta + self.tolerancia < objetosEnOrbita[i].anguloCarta:
                    respuesta = indiceOrbitaActual
                else:
                    hayLugar = False
            # Caso 2: hay mas de 2 objetos en orbita
            elif i < len(objetosEnOrbita) - 1:
                if (objeto.anguloCarta - self.tolerancia) > (objetosEnOrbita[len(objetosEnOrbita) - 1].anguloCarta - 360) and (objeto.anguloCarta + self.tolerancia) < objetosEnOrbita[i].anguloCarta:
                    respuesta = indiceOrbitaActual
                    break
                elif (objeto.anguloCarta - self.tolerancia) > objetosEnOrbita[i].anguloCarta and (objeto.anguloCarta + self.tolerancia) < objetosEnOrbita[i + 1].anguloCarta:
                    respuesta = indiceOrbitaActual
                    break
                else:
                    hayLugar = False
        if hayLugar:
            if objeto.nombre == 'paz':
                print('Hay lugar en orbita', indiceOrbitaActual, 'para', objeto.nombre)
                print('    Datos',objeto.anguloCarta)
                print('    Orbitando', objetosEnOrbita)
            return indiceOrbitaActual
        else:
            if objeto.nombre == 'paz':
                print('No hay lugar en orbita', indiceOrbitaActual + 1, 'para', objeto.nombre)
            return self.sondaOrbita(objeto, indiceCarta, indiceOrbitaActual + 1, objetosOrdenados)

    def pasaAdelante(self, nombre: str) -> bool:
        """Indica si el arábigo con el nombre dado tiene representación visual.

        Solo los arábigos listados en ``self.objetosArr`` tienen runa y
        Platónico en la escena de Blender.

        Args:
            nombre: Nombre corto del arábigo (ej. 'fortuna', 'matanza').

        Returns:
            True si el arábigo debe animarse, False en caso contrario.
        """
        return nombre in self.objetosArr
        #gol = False
        #for objetoNombre in self.objetosArr:
            #if nombre == objetoNombre:
                #gol = True
                #break
        #return gol

    def clonar(self, objetos: list) -> list:
        """Crea una copia superficial de una lista de objetos.

        Args:
            objetos: Lista de objetos a clonar.

        Returns:
            Nueva lista con las mismas referencias.
        """
        return list(objetos)

    def selectionSort(self, aList: list) -> None:
        """Ordena una lista de objetos celestes por ``anguloCarta`` ascendente.

        Implementa Selection Sort in-place. Se usa para ordenar los objetos
        antes de asignarles órbitas con ``sondaOrbita``.

        Args:
            aList: Lista de objetos con atributo ``anguloCarta`` a ordenar.
        """
        for i in range(len(aList)):
            least = i
            for k in range(i + 1, len(aList)):
                if aList[k].anguloCarta < aList[least].anguloCarta:
                    least = k
            self.swap(aList, least, i)

    def swap(self, A: list, x: int, y: int) -> None:
        """Intercambia dos elementos de una lista in-place.

        Args:
            A: Lista en la que se realizará el intercambio.
            x: Índice del primer elemento.
            y: Índice del segundo elemento.
        """
        A[x], A[y] = A[y], A[x]

    def setToTransform(self, nombreObjeto: str) -> None:
        """Selecciona un objeto de la escena de Blender y lo prepara para transformar.

        Deselecciona todos los objetos, establece el objeto indicado como activo
        y lo selecciona. Las operaciones ``bpy.ops.transform.*`` subsiguientes
        se aplican sobre este objeto.

        Args:
            nombreObjeto: Nombre exacto del objeto en la escena de Blender.
        """
        ob = bpy.context.scene.objects[nombreObjeto]
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)