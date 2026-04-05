# karta — Sistema 3D de Carta Astral en Blender

Este software genera una animación 3D de una carta astral en Blender. Dado una fecha, hora y lugar de nacimiento, calcula las posiciones de todos los planetas y puntos astrológicos y los anima durante 24.5 horas de cielo.

---

## Requisitos

- Windows 10 o superior
- Blender 4.x o superior
- Python 3.11 (el que usa Blender internamente)
- Las efemérides `swete64.exe` instaladas en `D:\karta\efemerides\swete64\`
- Los scripts del paquete instalados en `D:\karta\script\paquetes\`

---

## Paso 1 — Instalar Blender

1. Ve a [https://www.blender.org/download/](https://www.blender.org/download/)
2. Descarga la versión más reciente para Windows (el archivo `.msi` o `.zip`)
3. Si descargaste `.msi`, ejecútalo y sigue los pasos del instalador
4. Si descargaste `.zip`, descomprímelo donde quieras y ejecuta `blender.exe`

No necesitas instalar nada más para Blender en sí.

---

## Paso 2 — Verificar qué versión de Python usa Blender

Blender incluye su propio Python. Para saber qué versión es:

1. Abre Blender
2. En la barra superior, haz clic en **Scripting** (o busca la pestaña "Scripting" en el menú de espacios de trabajo)
3. En la consola de Python que aparece abajo, escribe:

```python
import sys
print(sys.version)
```

4. Presiona **Enter**. Verás algo como `3.11.x (...)`. Esa es la versión de Python de Blender.

> No necesitas instalar Python por separado. Blender ya lo trae incluido.

---

## Paso 3 — Instalar la librería `pytz` en el Python de Blender

El script necesita la librería `pytz` para manejar zonas horarias. Para instalarla en el Python de Blender:

1. Encuentra dónde está instalado Blender en tu computador. Por ejemplo: `C:\Program Files\Blender Foundation\Blender 4.x\`
2. Dentro de esa carpeta hay una subcarpeta llamada `4.x\python\bin\` (donde `4.x` es la versión de Blender)
3. Abre una ventana de **Símbolo del sistema** (busca "cmd" en el menú inicio) **como administrador**
4. Escribe el siguiente comando (ajusta la ruta según tu instalación):

```
"C:\Program Files\Blender Foundation\Blender 4.x\4.x\python\bin\python.exe" -m pip install pytz
```

5. Presiona **Enter** y espera a que termine la instalación

---

## Paso 4 — Estructura de carpetas requerida

Crea estas carpetas en tu disco `D:\`:

```
D:\
└── karta\
    ├── efemerides\
    │   └── swete64\
    │       └── swete64.exe        ← el motor de efemérides
    └── script\
        └── paquetes\
            ├── Arabigo.py
            ├── Asteroide.py
            ├── Carta.py
            ├── Casa.py
            ├── Planeta.py
            ├── Punto.py
            ├── Query.py
            ├── SecuenciaAstral.py
            ├── Signo.py
            └── __init__.py
```

Copia los archivos `.py` del paquete (todos excepto `secuenciaNatal.py` y `recargar.py`) dentro de `D:\karta\script\paquetes\`.

Los archivos `secuenciaNatal.py` y `recargar.py` los usarás directamente desde la consola de Blender.

---

## Paso 5 — Abrir el archivo de escena 3D en Blender

1. Abre Blender
2. Ve a **File → Open** y abre el archivo `.blend` del proyecto de carta astral
3. La escena 3D ya contiene todos los objetos (signos, planetas, casas, etc.) listos para ser animados

---

## Paso 6 — Ejecutar el script por primera vez

1. Dentro de Blender, haz clic en la pestaña **Scripting** en la barra superior
2. Haz clic en **Open** (botón en el editor de texto) y abre el archivo `secuenciaNatal.py`
3. Antes de ejecutar, revisa los parámetros de la carta (ver sección siguiente)
4. Haz clic en el botón **▶ Run Script** (triángulo de reproducción en la barra del editor de texto)

El script tardará varios minutos. En la consola de abajo verás mensajes de progreso como:
```
setInstantanea carta: 0 | frame: 0
setInstantanea carta: 1 | frame: 30
...
```

Cuando termine, la animación estará lista en la línea de tiempo de Blender. Presiona **Espacio** para reproducirla.

---

## Paso 7 — Recargar módulos tras hacer cambios

Si modificas algún archivo del paquete (como `SecuenciaAstral.py` o `Carta.py`) y quieres que Blender reconozca los cambios sin cerrar y reabrir todo:

1. Abre `recargar.py` en el editor de texto de Blender
2. Haz clic en **▶ Run Script**
3. Vuelve a `secuenciaNatal.py` y ejecútalo de nuevo

---

## Parámetros que puedes cambiar en `secuenciaNatal.py`

Abre `secuenciaNatal.py` en cualquier editor de texto (o en el editor de Blender). La sección que te interesa está hacia el final, bajo los comentarios `# Carta activa` y `# Parámetros de consulta`.

### Carta activa — la persona cuya carta quieres calcular

```python
fecha     = '1989-11-13'   # Fecha de nacimiento en formato AÑO-MES-DÍA
hora      = '12:15:00'     # Hora local de nacimiento en formato HH:MM:SS
longitud  = longitudTalca  # Longitud del lugar de nacimiento
latitud   = latitudTalca   # Latitud del lugar de nacimiento
zonaHoraria = zonaHorariaChile  # Zona horaria del lugar
```

**Cómo cambiar la fecha y hora:**
Modifica `fecha` y `hora` directamente. Por ejemplo, para una persona nacida el 3 de marzo de 1990 a las 8:45 AM:
```python
fecha = '1990-03-03'
hora  = '08:45:00'
```

**Cómo cambiar el lugar:**
Hay dos opciones:

*Opción A — usar una ciudad ya definida en el archivo:*
El archivo ya tiene coordenadas para Santiago, Talca, Buenos Aires (Caballito), Ciudad de México y Puebla. Solo cambia las variables `longitud` y `latitud`:
```python
longitud  = longitudSantiago
latitud   = latitudSantiago
zonaHoraria = zonaHorariaChile
```

*Opción B — agregar una ciudad nueva:*
En la sección de coordenadas de referencia, agrega las líneas con las coordenadas de la ciudad. Puedes obtener latitud y longitud de Google Maps (clic derecho sobre el punto → copia las coordenadas):
```python
latitudNuevaCiudad  = '-34.6037'   # número negativo = Sur
longitudNuevaCiudad = '-58.3816'   # número negativo = Oeste
```
Luego úsalas abajo:
```python
longitud  = longitudNuevaCiudad
latitud   = latitudNuevaCiudad
zonaHoraria = 'America/Argentina/Buenos_Aires'  # nombre de zona horaria pytz
```

Los nombres de zona horaria válidos los encuentras en: [https://en.wikipedia.org/wiki/List_of_tz_database_time_zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) — columna "TZ identifier".

### Parámetros de consulta — duración y resolución de la animación

```python
algoritmo           = 'p'       # Sistema de casas. 'p' = Placidus. No cambiar.
deltaPaso           = '-s30m'   # Intervalo entre cartas: 30 minutos
pasos               = '-n49'    # Número de cartas: 49 × 30 min = 24.5 horas
orientacionLongitud = 'W'       # 'W' para Oeste, 'E' para Este
orientacionLatitud  = 'S'       # 'S' para Sur, 'N' para Norte
```

**`deltaPaso`** — define cada cuántos minutos se calcula una instantánea del cielo. Valores posibles: `-s5m`, `-s10m`, `-s15m`, `-s30m`, `-s60m`. Valores más pequeños generan animaciones más suaves pero tardan más en calcularse.

**`pasos`** — define cuántas instantáneas se calculan en total. Con `-n49` y `-s30m` obtienes exactamente 24.5 horas de cielo (un día completo). Si cambias `deltaPaso`, ajusta `pasos` para mantener ~24 horas: por ejemplo, `-s15m` y `-n97`.

**`orientacionLongitud` y `orientacionLatitud`** — indican el hemisferio. Para América del Sur y Central usarás siempre `'W'` y `'S'` (o `'N'` para México y América Central).

### Cartas de referencia (historial de cartas calculadas)

Más arriba en el archivo hay un bloque entre `'''` y `'''` con otras cartas comentadas. Son ejemplos que puedes descomentar para calcular esas cartas en lugar de la activa. Solo tienes que mover la carta que quieras fuera del bloque de comentarios y poner la carta activa actual dentro.

---

## Solución de problemas frecuentes

**El script da error `ModuleNotFoundError: No module named 'pytz'`**
→ Sigue el Paso 3 para instalar pytz en el Python de Blender.

**El script da error `FileNotFoundError` con la ruta de swete64**
→ Verifica que `swete64.exe` esté en `D:\karta\efemerides\swete64\swete64.exe` exactamente. Si lo tienes en otra ubicación, edita la variable `self.ruta` en `Query.py`.

**El script da error sobre un objeto de Blender que no existe**
→ Algún objeto esperado (por ejemplo `solRuna` o `sol-directo`) no está en la escena. Verifica que el archivo `.blend` sea el correcto y que la escena esté completa.

**Blender se congela sin mensaje de error**
→ El cálculo de 49 cartas puede tardar varios minutos. Espera con paciencia. Si después de 15 minutos no avanza, revisa la consola del sistema (la ventana de comandos desde donde abriste Blender, si la hay) por mensajes de error.

**Los cambios en los archivos `.py` no tienen efecto**
→ Ejecuta `recargar.py` antes de volver a correr `secuenciaNatal.py`.
