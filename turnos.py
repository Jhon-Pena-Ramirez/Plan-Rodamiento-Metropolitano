"""
A partir de la asignacion de vehiculos por ruta (motor_rotacion) y la matriz
de horarios (io_data.load_horarios), genera las filas finales:
(ruta_fisica, fecha, hora, veh_interno)
"""


def generar_filas_turnos(fecha, tipo_dia, asignacion_ruta, horarios):
    """
    asignacion_ruta: dict ruta_fisica -> [interno1, interno2, ...] (posicion 1..N)
    horarios: dict de io_data.load_horarios()

    Retorna: dict ruta_fisica -> lista de dicts:
        {'fecha': fecha, 'hora': 'HH:MM', 'veh_interno': interno, 'bloque': n}
    """
    filas_por_ruta = {}
    for ruta, lista_vehiculos in asignacion_ruta.items():
        datos_ruta = horarios[ruta][tipo_dia]
        matrix = datos_ruta["matrix"]
        bloques = datos_ruta["bloques"]

        filas = []
        for posicion, interno in enumerate(lista_vehiculos, start=1):
            horas_pos = matrix.get(posicion, {})
            for bloque in bloques:
                hora = horas_pos.get(bloque)
                if hora is None:
                    continue
                filas.append({
                    "fecha": fecha,
                    "hora": hora,
                    "veh_interno": interno,
                    "bloque": bloque,
                })
        filas_por_ruta[ruta] = filas
    return filas_por_ruta
