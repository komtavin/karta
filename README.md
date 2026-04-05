# karta — Sistema 3D de Carta Astral en Blender

Este software genera una animación 3D de una carta astral en Blender. Dado una fecha, hora y lugar de nacimiento, calcula las posiciones de todos los planetas y puntos astrológicos y los anima durante 24.5 horas de cielo.

> ⚠️ **Importante — No modificar `cartaNatal.blend`**
> El archivo `cartaNatal.blend` es el prototipo que contiene todos los objetos 3D que el script necesita para funcionar. Modificarlo directamente puede eliminar objetos o cambiar nombres que el script espera encontrar, provocando errores difíciles de rastrear. **Nunca trabajes sobre `cartaNatal.blend` directamente.** Siempre crea una copia de ese archivo (desde el Explorador de Windows) y trabaja sobre la copia.

---

## Requisitos

- Windows 10 o superior
- Blender 5.0.1 (descargado desde blender.org)
- Python 3.11 — **ya viene incluido dentro de Blender**, no necesitas instalarlo por separado
- Las efemérides `swete64.exe` en la carpeta correcta (ver estructura más abajo)

---

## Estructura de carpetas del proyecto

El proyecto debe quedar organizado exactamente así:

```
karta/
    README.md
    cartaNatal.blend       ← prototipo — NO modificar directamente
    efemerides/
        swete64/
            swete64.exe    ← motor de efemérides
    materiales/
        *.jpg
    script/
        secuenciaNatal.py  ← script de ejecución principal
        recargar.py        ← script de recarga de módulos
        paquetes/
            Arabigo.py
            Asteroide.py
            Carta.py
            Casa.py
            Planeta.py
            Punto.py
            Query.py
            SecuenciaAstral.py
            Signo.py
            __init__.py
```

> **Nota sobre la ubicación del proyecto:** el proyecto asume por defecto que la carpeta `karta/` está en `D:\karta\`. Si guardaste el proyecto en otra unidad o ruta (por ejemplo `C:\proyectos\karta\`), debes ajustar **dos líneas en dos archivos distintos** antes de ejecutar:
>
> **Archivo 1 — `secuenciaNatal.py`**, línea:
> ```python
> sys.path.insert(0, 'D:\\karta\\script\\paquetes')
> ```
> Cámbiala a tu ruta, por ejemplo:
> ```python
> sys.path.insert(0, 'C:\\proyectos\\karta\\script\\paquetes')
> ```
>
> **Archivo 2 — `Query.py`** (dentro de `script/paquetes/`), línea:
> ```python
> self.ruta = 'D:\\karta\\efemerides\\swete64\\swete64.exe'
> ```
> Cámbiala a tu ruta, por ejemplo:
> ```python
> self.ruta = 'C:\\proyectos\\karta\\efemerides\\swete64\\swete64.exe'
> ```
>
> En ambos casos usa doble barra invertida `\\` entre cada carpeta. Si solo ajustas uno de los dos archivos, el otro seguirá buscando en `D:\karta\` y fallará.

---

## Paso 1 — Instalar Blender 5.0.1

1. Ve a [https://www.blender.org/download/releases/5-0/](https://www.blender.org/download/releases/5-0/)
2. Descarga el instalador para Windows (archivo `.msi`)
3. Ejecútalo y sigue los pasos del instalador

No necesitas instalar Python por separado. Blender 5.0.1 incluye Python 3.11 de forma interna y es exactamente esa versión la que ejecuta los scripts de este proyecto.

---

## Paso 2 — Verificar la versión de Python que usa tu Blender

Para confirmar qué versión de Python tiene tu instalación:

1. Abre Blender
2. En la barra superior haz clic en **Scripting**
3. Verás la **Consola interactiva de Python** en el área inferior. Sabrás que es la correcta porque muestra este saludo al abrirse:

```
PYTHON INTERACTIVE CONSOLE 3.11.13 (main, Sep 23 2025, 09:08:45) [MSC v.1929 64 bit (AMD64)]
Builtin Modules:       bpy, bpy.data, bpy.ops, bpy.props, bpy.types, bpy.context, bpy.utils, gpu, blf, mathutils
Convenience Imports:   from mathutils import *; from math import *
Convenience Variables: C = bpy.context, D = bpy.data
```

El número `3.11.13` confirma la versión de Python. Esa es la consola donde ejecutarás todos los scripts de este README.

---

## Paso 3 — Preparar una copia de trabajo

Como dijimos antes, nunca trabajes sobre `cartaNatal.blend` directamente. Antes de empezar:

1. Abre el Explorador de Windows y navega a la carpeta `karta/`
2. Haz clic derecho sobre `cartaNatal.blend` → **Copiar**
3. Pega la copia en el mismo lugar o en otra carpeta. Nómbrala algo como `cartaMari_20261013.blend`
4. A partir de aquí, **abre siempre tu copia**, no el original

---

## Paso 4 — Instalación de dependencias (solo la primera vez)

Esta instalación se hace una única vez. Requiere abrir Blender **con permisos de administrador**:

1. Busca Blender en el menú inicio
2. Haz clic derecho → **Ejecutar como administrador**
3. Abre tu archivo `.blend` de trabajo (tu copia)
4. Ve a la pestaña **Scripting** en la barra superior
5. En la **Consola interactiva de Python** (el área inferior que muestra el saludo `PYTHON INTERACTIVE CONSOLE 3.11.13...`), copia y pega el siguiente bloque completo:

```python
import subprocess
import sys
python_exe = sys.executable
subprocess.call([python_exe, "-m", "ensurepip"])
subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
subprocess.call([python_exe, "-m", "pip", "install", "pytz"])
```

6. Presiona **Enter** para ejecutar

La consola mostrará texto de instalación. Espera a que vuelva a aparecer el símbolo `>>>` — eso indica que terminó. Cuando termine, `pytz` estará instalado y no necesitarás repetir este paso salvo que reinstales Blender.

> Si algo falla silenciosamente durante la instalación (por ejemplo, falta de permisos), puedes verificar el resultado en la Consola del Sistema de Blender: ve al menú **Window → Toggle System Console**. Ahí aparecen todos los mensajes de error que la consola de Python no muestra.

> La segunda vez que abras Blender para trabajar en el proyecto **no necesitas permisos de administrador** ni repetir este paso.

---

## Paso 5 — Ejecutar el proyecto (cada vez que abres Blender)

Cada vez que abres Blender y quieres calcular y animar una carta:

1. Abre tu archivo `.blend` de trabajo
2. Ve a la pestaña **Scripting**
3. En la **Consola interactiva de Python**, copia y pega:

```python
import bpy
filepath = bpy.path.abspath("//script/secuenciaNatal.py")
exec(compile(open(filepath).read(), filepath, 'exec'))
```

4. Presiona **Enter**

El script tardará varios minutos (con 49 cartas de 30 minutos). Durante ese tiempo **la ventana de Blender quedará sin responder** — esto es normal, no es un error. No cierres Blender ni hagas clic en ningún lado mientras trabaja.

Cuando termine, la consola mostrará todos los mensajes de progreso juntos de una sola vez:
```
setInstantanea carta: 0 | frame: 0
setInstantanea carta: 1 | frame: 30
...
setInstantanea carta: 48 | frame: 1440
```

Y volverá a aparecer el símbolo `>>>`. Ese es el indicador de que la animación está lista. Para reproducirla:
- Mueve el cursor del mouse **sobre la vista 3D** (el área con los objetos)
- Presiona la barra **Espacio**

> Si presionas Espacio con el cursor sobre otra área (como la consola), la barra espaciadora realizará una acción diferente. El mouse debe estar sobre la vista 3D.

---

## Paso 6 — Recargar módulos tras hacer cambios en el código

Si modificaste alguno de los archivos `.py` del paquete (`SecuenciaAstral.py`, `Carta.py`, etc.) y quieres que Blender reconozca los cambios sin cerrar y reabrir todo:

1. En la **Consola interactiva de Python**, copia y pega:

```python
import bpy
exec(compile(open(bpy.path.abspath("//script/recargar.py")).read(), bpy.path.abspath("//script/recargar.py"), 'exec'))
```

2. Presiona **Enter**
3. Luego vuelve a ejecutar el script del Paso 5

---

## Parámetros que puedes cambiar en `secuenciaNatal.py`

Abre `secuenciaNatal.py` con cualquier editor de texto (Notepad, Notepad++, etc.) o desde la consola de Blender. Los parámetros están hacia el final del archivo, bajo los comentarios `# Carta activa` y `# Parámetros de consulta`.

### Carta activa — la persona cuya carta quieres calcular

```python
fecha     = '1989-11-13'   # Fecha de nacimiento → formato AÑO-MES-DÍA
hora      = '12:15:00'     # Hora local de nacimiento → formato HH:MM:SS
longitud  = longitudTalca  # Longitud del lugar de nacimiento
latitud   = latitudTalca   # Latitud del lugar de nacimiento
zonaHoraria = zonaHorariaChile  # Zona horaria del lugar
```

**Cambiar fecha y hora:**
```python
fecha = '1990-03-03'   # 3 de marzo de 1990
hora  = '08:45:00'     # 8:45 AM
```

---

### Coordenadas del lugar: longitud, latitud y sus orientaciones

Las coordenadas de un lugar se expresan con **cuatro valores que deben ser coherentes entre sí**:

| Variable | Qué representa | Valores posibles |
|---|---|---|
| `latitud` | Posición norte-sur en grados decimales | Positivo = Norte / Negativo = Sur |
| `orientacionLatitud` | Confirmación del hemisferio de `latitud` | `'N'` si latitud es positiva / `'S'` si es negativa |
| `longitud` | Posición este-oeste en grados decimales | Positivo = Este / Negativo = Oeste |
| `orientacionLongitud` | Confirmación del hemisferio de `longitud` | `'E'` si longitud es positiva / `'W'` si es negativa |

**Regla simple:** la orientación siempre describe el signo del número:
- Número negativo en `latitud` → `orientacionLatitud = 'S'`
- Número positivo en `latitud` → `orientacionLatitud = 'N'`
- Número negativo en `longitud` → `orientacionLongitud = 'W'`
- Número positivo en `longitud` → `orientacionLongitud = 'E'`

**Ejemplo para Bogotá, Colombia:**
```python
latitud   = '4.7110'     # positivo → Norte
longitud  = '-74.0721'   # negativo → Oeste
orientacionLatitud  = 'N'
orientacionLongitud = 'W'
```

**Ejemplo para Santiago, Chile:**
```python
latitud   = '-33.4372'   # negativo → Sur
longitud  = '-70.6506'   # negativo → Oeste
orientacionLatitud  = 'S'
orientacionLongitud = 'W'
```

Si mezclas un número negativo con `'N'` o `'E'`, el cálculo será incorrecto sin mostrar ningún error.

---

### Zona horaria y su relación con las coordenadas

La `zonaHoraria` debe corresponder **al mismo lugar geográfico** que las coordenadas de `latitud` y `longitud`. Si usas coordenadas de Bogotá pero zona horaria de Santiago, el cálculo de la hora UTC será incorrecto y la carta quedará desplazada en el tiempo.

Regla: **las coordenadas y la zona horaria deben ser del mismo lugar.**

```python
# Correcto: coordenadas y zona horaria de Bogotá
latitud     = '4.7110'
longitud    = '-74.0721'
zonaHoraria = 'America/Bogota'

# Incorrecto: coordenadas de Bogotá con zona horaria de Santiago
latitud     = '4.7110'
longitud    = '-74.0721'
zonaHoraria = 'America/Santiago'   # ← ERROR silencioso
```

---

### Cómo usar una ciudad ya definida en el archivo

El archivo ya tiene coordenadas predefinidas para Santiago, Talca, Buenos Aires y Ciudad de México:

```python
longitud    = longitudSantiago
latitud     = latitudSantiago
orientacionLongitud = 'W'
orientacionLatitud  = 'S'
zonaHoraria = zonaHorariaChile
```

### Cómo agregar una ciudad nueva

Busca las coordenadas en Google Maps: clic derecho sobre el punto exacto → aparecen dos números (latitud, longitud). Agrégalos en la sección de coordenadas de referencia del archivo:

```python
latitudBogota  = '4.7110'     # positivo = Norte
longitudBogota = '-74.0721'   # negativo = Oeste
```

Luego úsalos en la carta activa:
```python
latitud             = latitudBogota
longitud            = longitudBogota
orientacionLatitud  = 'N'
orientacionLongitud = 'W'
zonaHoraria         = 'America/Bogota'
```

### Cómo encontrar el nombre de zona horaria

Ve a [https://en.wikipedia.org/wiki/List_of_tz_database_time_zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) y usa la búsqueda del navegador (**Ctrl+F** en Windows) para buscar el **código de país de dos letras** o el **TZ Identifier** directamente. La tabla no permite buscar por el nombre del país en español — debes usar el código ISO de dos letras.

Por ejemplo, para Colombia:
- Abre la página y presiona **Ctrl+F**
- Busca `CO` (código de Colombia) o directamente `Bogota`
- Encontrarás la fila con `America/Bogota` en la columna **TZ identifier**
- Ese es el valor exacto que debes escribir en `zonaHoraria`

Tabla de zonas horarias comunes:

| País / Ciudad | Código | Valor para `zonaHoraria` |
|---|---|---|
| Chile (Santiago) | CL | `America/Santiago` |
| Argentina | AR | `America/Argentina/Buenos_Aires` |
| Colombia | CO | `America/Bogota` |
| México (Ciudad de México) | MX | `America/Mexico_City` |
| Perú | PE | `America/Lima` |
| Venezuela | VE | `America/Caracas` |
| España | ES | `Europe/Madrid` |

---

### Parámetros de consulta — duración de la animación

```python
algoritmo           = 'p'       # Sistema de casas Placidus — no cambiar
deltaPaso           = '-s30m'   # Intervalo entre cartas: 30 minutos
pasos               = '-n49'    # Número de cartas: 49 × 30 min = 24.5 horas
orientacionLongitud = 'W'       # Coherente con el signo de longitud (ver arriba)
orientacionLatitud  = 'S'       # Coherente con el signo de latitud (ver arriba)
```

**`deltaPaso`** — cada cuántos minutos se calcula una instantánea del cielo. Valores posibles: `-s5m`, `-s10m`, `-s15m`, `-s30m`, `-s60m`. Menos minutos = animación más suave, pero tarda más.

**`pasos`** — cuántas instantáneas en total. Con `-n49` y `-s30m` obtienes 24.5 horas. Si cambias `deltaPaso`, ajusta `pasos` para mantener ~24 horas:
- `-s15m` → `-n97`
- `-s60m` → `-n25`

### Cartas de referencia (historial)

Más arriba en el archivo hay un bloque entre `'''` y `'''` con otras cartas anteriores. Para usar una: sácala del bloque de comentarios y pon la carta activa actual dentro del bloque.

---

## Solución de problemas frecuentes

**El script da error `ModuleNotFoundError: No module named 'pytz'`**
→ No se ejecutó la instalación del Paso 4, o no se ejecutó como administrador. Abre Blender como administrador y repite ese paso completo.

**El script da error `FileNotFoundError` mencionando `swete64`**
→ El ejecutable no está en la ruta correcta. Verifica que exista en `D:\karta\efemerides\swete64\swete64.exe`. Si tu proyecto está en otra ruta, edita la variable `self.ruta` en `Query.py` con la ruta correcta.

**El script da error sobre un objeto de Blender que no existe (ej. `solRuna`, `sol-directo`)**
→ Estás trabajando sobre `cartaNatal.blend` directamente, o usaste una copia incompleta. Crea una copia nueva desde el original sin modificar.

**Los cambios en los archivos `.py` no tienen efecto**
→ Ejecuta el script de recarga del Paso 6 antes de volver a correr `secuenciaNatal.py`.

**Blender se congela sin mensaje de error visible en la consola**
→ El cálculo de 49 cartas tarda varios minutos. Espera. Si después de 15 minutos no aparece ningún mensaje nuevo, activa la consola del sistema de Blender: dentro de Blender ve al menú **Window → Toggle System Console**. Se abrirá una ventana separada con todos los mensajes de error que Blender registra internamente y que no aparecen en la consola de Python.

**La animación no se reproduce al presionar Espacio**
→ El cursor del mouse debe estar **sobre la vista 3D** (el área con los objetos en 3D) cuando presionas Espacio. Si el cursor está sobre la consola u otra área, la barra espaciadora realiza una acción diferente.

**La carta calculada tiene hora incorrecta**
→ Verifica que `zonaHoraria` corresponda al mismo lugar que `latitud` y `longitud`. Una zona horaria incorrecta desplaza toda la carta en el tiempo sin mostrar ningún error.

**La carta tiene las posiciones geográficas invertidas (norte/sur o este/oeste)**
→ Verifica que `orientacionLatitud` y `orientacionLongitud` sean coherentes con el signo de los números de `latitud` y `longitud`. Un número negativo en `latitud` siempre debe ir acompañado de `orientacionLatitud = 'S'`.
