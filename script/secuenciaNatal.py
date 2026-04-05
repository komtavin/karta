#!/usr/bin/python
"""Script de ejecución principal para calcular y animar una carta natal en Blender.

Flujo de uso:
1. Ajustar los parámetros de la carta (fecha, hora, lugar) en la sección
   de configuración activa al final del archivo.
2. Verificar que ``pasos`` tenga el valor correcto ('-n49' para animación completa).
3. Ejecutar desde la consola de scripting de Blender.

Para recargar los módulos tras cambios en el paquete, ejecutar recargar.py primero.

Notas:
    - Las fechas comentadas dentro del bloque '''...''' son cartas de referencia
      usadas durante el desarrollo. Descomenta la que necesites y comenta la activa.
    - ``deltaPaso = '-s30m'`` genera 49 cartas de 30 minutos = 24.5 horas de cielo.
    - El sistema de casas utilizado es Placidus (algoritmo='p').
"""

import sys
from importlib import reload

# Agrega el directorio de paquetes al path. Ajustar según el sistema operativo.
#WIN#sys.path.insert(0, 'D:\\karta\\script\\paquetes')
sys.path.insert(0, '/Users/komtavin/Desktop/Proyectos/rukaLab/karta/script/')

from SecuenciaAstral import SecuenciaAstral
from Query import Query

# Recarga de módulos (necesario en Blender tras modificar el paquete)
from sys import modules
reload(modules['Query'])
reload(modules['SecuenciaAstral'])
reload(modules['Planeta'])
reload(modules['Casa'])
reload(modules['Punto'])
reload(modules['Asteroide'])
reload(modules['Signo'])
reload(modules['Carta'])
reload(modules['Arabigo'])

# ---------------------------------------------------------------------------
# Coordenadas de referencia
# ---------------------------------------------------------------------------
zonaHorariaChile     = 'America/Santiago'
zonaHorariaArgentina = 'America/Argentina/Buenos_Aires'
zonaHorariaMexico    = ''
zonaHorariaColombia  = ''

latitudSantiago  = '-33.4372'
longitudSantiago = '-70.6506'

latitudTalca  = '-35.430758'
longitudTalca = '-71.654115'

latitudCaballito  = '-58.446202'   # Buenos Aires, Argentina
longitudCaballito = '-34.607259'

latitudMexico  = '19.381029'
longitudMexico = '-99.139041'

latitudPuebla  = '19.032884'
longitudPuebla = '-98.210986'

# ---------------------------------------------------------------------------
# Cartas de referencia (descomenta la que necesites)
# ---------------------------------------------------------------------------
'''
fecha     = '1985-01-18'   # Evian — 18/01/1985 15:30 (-03)
hora      = '15:30:00'
longitud  = longitudCaballito
latitud   = latitudCaballito
zonaHoraria = zonaHorariaArgentina

fecha     = '1991-10-31'   # Mexico (Ciudad de Mexico) - 31/10/1991 05:00 (+05)
hora      = '05:00:00'
longitud  = longitudMexico
latitud   = latitudMexico
zonaHoraria = zonaHorariaMexico

fecha     = '2020-05-05'   # Mexico (Puebla) - 05/05/2020 05:00 (+05)
hora      = '05:00:00'
longitud  = longitudPuebla
latitud   = latitudPuebla
zonaHoraria = zonaHorariaMexico

fecha     = '1991-11-18'   # Achicoria - 18/11/1991 04:00 (+04)
hora      = '04:00:00'
longitud  = longitudSantiago
latitud   = latitudSantiago
zonaHoraria = zonaHorariaChile

fecha     = '2020-06-19'   # Otras fechas - 19/06/2020 06:00 (+03)
hora      = '06:00:00'
longitud  = longitudSantiago
latitud   = latitudSantiago
zonaHoraria = zonaHorariaChile

fecha     = '1974-10-02'   # Yo? - 02/30/1974 10:30 (+04)
hora      = '10:30:00'
longitud  = longitudSantiago
latitud   = latitudSantiago
zonaHoraria = zonaHorariaChile

fecha     = '1995-10-08'   # Pauli - 08/10/1995 13:15 (+04)
hora      = '13:15:00'
longitud  = longitudSantiago
latitud   = latitudSantiago
zonaHoraria = zonaHorariaChile
'''

# ---------------------------------------------------------------------------
# Carta activa
# ---------------------------------------------------------------------------
fecha     = '1989-11-13'   # Mari - 13/11/1989 12:15 (+04)
hora      = '12:15:00'
longitud  = longitudTalca
latitud   = latitudTalca
zonaHoraria = zonaHorariaChile

# ---------------------------------------------------------------------------
# Parámetros de consulta
# ---------------------------------------------------------------------------
algoritmo           = 'p'       # Placidus
deltaPaso           = '-s30m'   # Intervalo entre cartas: 30 minutos
pasos               = '-n49'    # 49 cartas × 30 min = 24.5 horas de cielo
orientacionLongitud = 'W'
orientacionLatitud  = 'S'

# ---------------------------------------------------------------------------
# Ejecución
# ---------------------------------------------------------------------------
secuenciaAstral = SecuenciaAstral(
    Query(
        fecha, hora,
        longitud, orientacionLongitud,
        latitud, orientacionLatitud,
        algoritmo, pasos, deltaPaso, zonaHoraria,
    )
)
#indiceCarta = 0

#print(secuenciaAstral.getCartas('casa 1.signo.nombre')[indiceCarta], secuenciaAstral.getCartas('casa 1.signo.anguloInicialReal')[indiceCarta], secuenciaAstral.getCartas('casa 1.nombre')[indiceCarta], secuenciaAstral.getCartas('casa 1.anguloReal')[indiceCarta])
#print(secuenciaAstral.getCartas('ascendente.signo.nombre')[indiceCarta], secuenciaAstral.getCartas('casa 1.signo.anguloInicialReal')[indiceCarta], secuenciaAstral.getCartas('ascendente.nombre')[indiceCarta], secuenciaAstral.getCartas('ascendente.anguloReal')[indiceCarta])
#print(secuenciaAstral.getCartas('casa 5.signo.nombre')[indiceCarta], secuenciaAstral.getCartas('casa 5.signo.anguloInicialReal')[indiceCarta])
#print(secuenciaAstral.getCartas('casa 1.signo.nombre')[indiceCarta], secuenciaAstral.getCartas('casa 1.signo.anguloInicialReal')[indiceCarta])
#print(secuenciaAstral.getCartas('casa 2.signo.nombre')[indiceCarta], secuenciaAstral.getCartas('casa 2.signo.anguloInicialReal')[indiceCarta])
#print(secuenciaAstral.getCartas('casa 3.signo.nombre')[indiceCarta], secuenciaAstral.getCartas('casa 3.signo.anguloInicialReal')[indiceCarta])
#print(secuenciaAstral.getCartas('casa 4.signo.nombre')[indiceCarta], secuenciaAstral.getCartas('casa 4.signo.anguloInicialReal')[indiceCarta])
#print(secuenciaAstral.getCartas('casa 5.signo.nombre')[indiceCarta], secuenciaAstral.getCartas('casa 5.signo.anguloInicialReal')[indiceCarta])
#print(secuenciaAstral.getCartas('casa 6.signo.nombre')[indiceCarta], secuenciaAstral.getCartas('casa 6.signo.anguloInicialReal')[indiceCarta])
#print(secuenciaAstral.getCartas('casa 7.signo.nombre')[indiceCarta], secuenciaAstral.getCartas('casa 7.signo.anguloInicialReal')[indiceCarta])
#print(secuenciaAstral.getCartas('casa 8.signo.nombre')[indiceCarta], secuenciaAstral.getCartas('casa 8.signo.anguloInicialReal')[indiceCarta])
#print(secuenciaAstral.getCartas('casa 9.signo.nombre')[indiceCarta], secuenciaAstral.getCartas('casa 9.signo.anguloInicialReal')[indiceCarta])
#print(secuenciaAstral.getCartas('casa 10.signo.nombre')[indiceCarta], secuenciaAstral.getCartas('casa 10.signo.anguloInicialReal')[indiceCarta])
#print(secuenciaAstral.getCartas('casa 11.signo.nombre')[indiceCarta], secuenciaAstral.getCartas('casa 11.signo.anguloInicialReal')[indiceCarta])
#print(secuenciaAstral.getCartas('casa 12.signo.nombre')[indiceCarta], secuenciaAstral.getCartas('casa 12.signo.anguloInicialReal')[indiceCarta])
#indiceCarta += 1
#print(secuenciaAstral.cartas[0])
#print(secuenciaAstral.cartas[0].idFecha)
#print(secuenciaAstral.cartas[1].idFecha)
#print(secuenciaAstral.cartas[0].planetas[5].signo.nombre)
'''
print(  secuenciaAstral.getCartas('luna.nombre')[0], 
        secuenciaAstral.getCartas('luna.anguloReal')[0])
print(  secuenciaAstral.getCartas('casa 1.nombre')[0], 
        secuenciaAstral.getCartas('casa 1.anguloReal')[0])
print(  secuenciaAstral.getCartas('casa 1.nombre')[0])
print(  secuenciaAstral.getCartas('casa 1.nombre')[0], 
        secuenciaAstral.getCartas('casa 1.anguloReal')[0], 
        secuenciaAstral.getCartas('casa 1.signo.nombre')[0])
# casa 1 esta en cero grados
# moverla a su lugar
print(  secuenciaAstral.getCartas('ascendente.nombre')[0], 
        secuenciaAstral.getCartas('ascendente.anguloReal')[0], 
        secuenciaAstral.getCartas('ascendente.signo.nombre')[0])
anguloAscendente = secuenciaAstral.getCartas('ascendente.anguloReal')[0]
indiceSignoAscendente = secuenciaAstral.getCartas('ascendente.signo.indice')[0]
'''
#bpy.context.scene.frame_current = 100
#print(bpy.context.scene.frame_current)
# un signo pertenece solo a un planeta
# un signo pertenece a mas de una casa => CHASH-KAPUT

#print(matrizConsola)
#signo = Signo('sa')
#print(signo.nombre)

#for obj in bpy.data.objects:
#    print(obj.name)

#object = bpy.data.objects['aries']
#print(object.name)
#bpy.context.scene.objects.active = object

#bpy.context.scene.objects["aries"].select = True
#bpy.context.scene.objects.active = bpy.data.objects['aries']
#bpy.ops.object.editmode_toggle()

#from array import *

#http://www.astrodestino.com.ar/cmps_index.php?pageid=cursocarta5
'''for nombreCasa in casas:
    #print(i)
    ob = bpy.context.scene.objects[nombreCasa]
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.transform.rotate(value=(21.5*pi/180))'''
