# Plan de Rodamiento — Generador automático

## ¿Qué hace?
A partir de 3 archivos Excel (Base de vehículos, Horarios/topes, Sorteo inicial),
genera el plan de rodamiento mensual completo: qué vehículo va en qué ruta,
en qué turno y a qué hora, cada día del mes — respetando la rotación de
corredores, la partición Tejaditos/Terminal, Nueva Flota en CRA33, la
redistribución de excedentes y los días festivos/dominicales.

## Instalación (una sola vez)

1. Instala Python 3.10 o superior.
2. Abre esta carpeta en Visual Studio Code.
3. En la terminal de VS Code:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Mac/Linux
   pip install -r requirements.txt
   ```

## Probar localmente (en tu computador)

```bash
streamlit run app.py
```
Esto abre una página en tu navegador (`http://localhost:8501`) donde puedes
subir los 3 archivos, elegir el mes, generar y descargar el plan.

## Probar el motor sin interfaz (línea de comandos)

```bash
cd src
python generar_plan.py
```
Genera un plan de prueba usando los archivos de `data/` (edítalo para
apuntar a tus propios archivos).

## Publicar para que tus compañeros lo usen por un enlace

La forma más rápida y gratuita es **Streamlit Community Cloud**:

1. Sube esta carpeta a un repositorio de GitHub (puede ser privado).
2. Entra a https://share.streamlit.io con tu cuenta de GitHub.
3. Selecciona el repositorio, la rama, y como archivo principal `app.py`.
4. Streamlit te da un enlace público (`https://tuapp.streamlit.app`) que
   tus compañeros pueden abrir desde cualquier navegador, sin instalar nada.

Si tu empresa prefiere un servidor propio/interno en vez de la nube pública,
la misma app se puede desplegar igual con `streamlit run app.py --server.port 8501`
en cualquier servidor con Python, y exponerlo en la red interna.

## Estructura del proyecto

```
rodamiento/
├── app.py                    # Interfaz web (Streamlit)
├── requirements.txt
├── data/                     # Archivos de prueba (los que compartiste)
├── output/                   # Salida de pruebas por línea de comandos
└── src/
    ├── config_corredores.py  # Mapeo de corredores <-> rutas físicas (AJUSTAR AQUÍ si cambia la estructura)
    ├── io_data.py             # Lectura de los 3 Excel de entrada
    ├── calendario.py          # Determina día hábil / festivo-dominical
    ├── motor_rotacion.py      # Lógica de rotación, partición y redistribución
    ├── turnos.py               # Cruza asignación de vehículos con horarios exactos
    ├── exportar.py             # Genera el .xlsx final (una hoja por ruta)
    └── generar_plan.py         # Orquesta todo el proceso para un mes completo
```

## Mantenimiento: ingreso de vehículos nuevos

Cuando entra un vehículo nuevo a la flota, ANTES de generar el plan del
siguiente mes:

1. Agrégalo a `Base_vehiculos.xlsx` (Interno, Placa, NUI, Tarjeta de
   operación, Tipo).
2. Si el corredor al que entra necesita más cupos, actualiza
   `Horarios_...xlsx` agregando la fila correspondiente en la tabla de
   recorridos de esa ruta (el programa lee el tope automáticamente
   contando filas, no hay que tocar código).
3. En `Sorteo.xlsx`, insértalo en la columna del corredor que le
   corresponda, en la posición donde tú decidas dentro de esa lista.

El programa no tiene ningún tope "hardcodeado": todo sale de estos 3
archivos, así que estos cambios son suficientes para el mes siguiente.

## Notas importantes

- El proyecto usa la librería `holidays` para detectar festivos de Colombia
  automáticamente (además de los domingos). Necesita conexión a internet la
  primera vez que se usa cada año, para descargar el calendario oficial.
- Si un día no alcanzan vehículos para llenar todos los cupos de un corredor,
  la app te avisa cuántos días del mes quedaron con cupos sin cubrir.
