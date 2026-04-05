"""
Utilidad de recarga de módulos del paquete karta para uso en Blender.

Ejecutar este script desde la consola de Blender cada vez que se modifique
algún módulo del paquete, para que los cambios surtan efecto sin reiniciar.
"""

import importlib
import sys

MODULOS = [
    'Arabigo',
    'Signo',
    'Carta',
    'Punto',
    'Casa',
    'Asteroide',
    'Planeta',
    'Query',
    'SecuenciaAstral',
]

for nombre in MODULOS:
    if nombre in sys.modules:
        importlib.reload(sys.modules[nombre])
        print(f'Recargado: {nombre}')
    else:
        print(f'No estaba cargado: {nombre}')

print('--- Recarga completa ---')
