"""
Orquestador: junta io_data + calendario + motor_rotacion + turnos + exportar
para generar el plan de rodamiento de un mes completo.
"""
import calendar as calendar_lib
from datetime import date

from io_data import load_vehiculos, load_horarios, load_sorteo
from calendario import tipo_de_dia
from motor_rotacion import calcular_asignacion_dia
from turnos import generar_filas_turnos
from exportar import exportar_plan


def generar_plan_mensual(path_vehiculos, path_horarios, path_sorteo,
                          anio, mes, path_salida):
    vehiculos = load_vehiculos(path_vehiculos)
    horarios = load_horarios(path_horarios)
    sorteo = load_sorteo(path_sorteo)

    rutas_fisicas = list(horarios.keys())
    todas_las_filas = {ruta: [] for ruta in rutas_fisicas}

    _, dias_en_mes = calendar_lib.monthrange(anio, mes)

    resumen_sin_asignar = []

    for dia_num in range(1, dias_en_mes + 1):
        fecha = date(anio, mes, dia_num)
        tipo_dia = tipo_de_dia(fecha)

        topes_dia = {ruta: horarios[ruta][tipo_dia]["tope"] for ruta in rutas_fisicas}
        asignacion, sin_asignar = calcular_asignacion_dia(dia_num, sorteo, topes_dia)

        if sin_asignar:
            resumen_sin_asignar.append((fecha, sin_asignar))

        filas_dia = generar_filas_turnos(fecha, tipo_dia, asignacion, horarios)
        for ruta, filas in filas_dia.items():
            for f in filas:
                f["tipo_dia"] = tipo_dia
            todas_las_filas[ruta].extend(filas)

    exportar_plan(todas_las_filas, vehiculos, horarios, path_salida)

    return {
        "path_salida": path_salida,
        "dias_generados": dias_en_mes,
        "sin_asignar": resumen_sin_asignar,
    }


if __name__ == "__main__":
    resultado = generar_plan_mensual(
        path_vehiculos="../data/Base_vehiculos.xlsx",
        path_horarios="../data/Horarios_planrodamiento_132vh_2026.xlsx",
        path_sorteo="../data/Sorteo.xlsx",
        anio=2026,
        mes=8,
        path_salida="../output/plan_rodamiento_2026_08.xlsx",
    )
    print("Plan generado en:", resultado["path_salida"])
    print("Dias generados:", resultado["dias_generados"])
    print("Dias con vehiculos sin asignar:", len(resultado["sin_asignar"]))
    if resultado["sin_asignar"]:
        fecha, sin_asig = resultado["sin_asignar"][0]
        print("Ejemplo:", fecha, "->", sin_asig)
