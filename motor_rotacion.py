"""
Motor de rotacion: dado el dia N del mes, determina que vehiculo va
a que ruta fisica y en que posicion, siguiendo toda la logica acordada:
- Ciclo de 5 corredores
- Desplazamiento de orden interno (4 posiciones/dia)
- Particion por paridad en corredores de 2 rutas (con alternancia)
- Manejo especial de CRA33 + Nueva Flota
- Redistribucion del excedente por prioridad
"""
from config_corredores import (
    CICLO_CORREDORES,
    CORREDOR_RUTAS_FISICAS,
    CORREDOR_NUEVA_FLOTA,
    PRIORIDAD_EXCEDENTE,
    DESPLAZAMIENTO_ORDEN_DIARIO,
    TAMANO_BLOQUE_NUEVA_FLOTA,
    TAMANO_BLOQUE_REGULAR,
)

N_CORREDORES = len(CICLO_CORREDORES)


def _rotar_orden(lista, dia):
    """
    Rota la lista 'dia-1' veces en bloques de DESPLAZAMIENTO_ORDEN_DIARIO.
    Dia 1 = orden original.
    """
    n = len(lista)
    if n == 0:
        return []
    desplazamiento = (DESPLAZAMIENTO_ORDEN_DIARIO * (dia - 1)) % n
    return lista[desplazamiento:] + lista[:desplazamiento]


def _corredor_de_hoy(corredor_home, dia):
    idx_home = CICLO_CORREDORES.index(corredor_home)
    idx_hoy = (idx_home + (dia - 1)) % N_CORREDORES
    return CICLO_CORREDORES[idx_hoy]


def _numero_de_visita(corredor_home, corredor_destino, dia):
    """
    Cuantas veces (contando desde 0) el grupo 'corredor_home' ya ha estado
    en 'corredor_destino' antes del dia actual (incluyendolo).
    Se usa para alternar la paridad en corredores de 2 rutas.
    """
    idx_home = CICLO_CORREDORES.index(corredor_home)
    idx_destino = CICLO_CORREDORES.index(corredor_destino)
    offset = (idx_destino - idx_home) % N_CORREDORES  # primer dia (1-indexado) en que coincide
    primer_dia = offset + 1
    if dia < primer_dia:
        return 0
    return (dia - primer_dia) // N_CORREDORES


def _split_por_paridad(lista_ordenada, invertir):
    """
    Divide una lista ordenada en dos, por paridad de posicion (1-indexada).
    Retorna (lista_A, lista_B). Si invertir=True, se intercambian A y B.
    """
    A, B = [], []
    for i, veh in enumerate(lista_ordenada, start=1):
        if i % 2 == 1:
            A.append(veh)
        else:
            B.append(veh)
    return (B, A) if invertir else (A, B)


def calcular_asignacion_dia(dia, sorteo, topes_por_ruta_fisica):
    """
    dia: entero (1 = primer dia del mes)
    sorteo: dict corredor_home -> [internos...] (de io_data.load_sorteo), incluye 'NUEVA_FLOTA'
    topes_por_ruta_fisica: dict ruta_fisica -> tope (int), YA resuelto para el tipo de dia correspondiente

    Retorna: dict ruta_fisica -> [interno1, interno2, ...] en orden de posicion (1..tope)
             (puede tener menos elementos que el tope si no alcanzan vehiculos)
    """
    cohortes_home = [c for c in CICLO_CORREDORES]  # cada corredor tiene un grupo "home"

    # 1. Orden interno rotado de cada cohorte de hoy + corredor destino de hoy
    rotados = {}
    destino_hoy = {}
    for home in cohortes_home:
        lista = sorteo.get(home, [])
        rotados[home] = _rotar_orden(lista, dia)
        destino_hoy[home] = _corredor_de_hoy(home, dia)

    nueva_flota_rotada = _rotar_orden(sorteo.get("NUEVA_FLOTA", []), dia)

    # 2. Encontrar que cohorte le toca hoy en cada corredor (busqueda inversa)
    cohorte_en_corredor = {corredor: None for corredor in CICLO_CORREDORES}
    for home, corredor in destino_hoy.items():
        cohorte_en_corredor[corredor] = home

    asignacion = {ruta: [] for ruta in topes_por_ruta_fisica}
    excedente = []  # pool de vehiculos sin cupo, en orden, a redistribuir

    # 3. Procesar CRA33 (caso especial con Nueva Flota)
    corredor_c33 = CORREDOR_NUEVA_FLOTA
    home_c33 = cohorte_en_corredor[corredor_c33]
    lista_c33 = rotados[home_c33]
    rutas_c33 = CORREDOR_RUTAS_FISICAS[corredor_c33]
    tope_c33_total = sum(topes_por_ruta_fisica[r] for r in rutas_c33)

    merged = []
    i_nf, i_reg = 0, 0
    turno_nf = True
    while len(merged) < tope_c33_total and (i_nf < len(nueva_flota_rotada) or i_reg < len(lista_c33)):
        tomados_este_bloque = 0
        if turno_nf:
            while (tomados_este_bloque < TAMANO_BLOQUE_NUEVA_FLOTA
                   and i_nf < len(nueva_flota_rotada)
                   and len(merged) < tope_c33_total):
                merged.append(nueva_flota_rotada[i_nf]); i_nf += 1
                tomados_este_bloque += 1
            if tomados_este_bloque == 0:
                # Nueva Flota agotada: seguir llenando con el grupo regular
                while i_reg < len(lista_c33) and len(merged) < tope_c33_total:
                    merged.append(lista_c33[i_reg]); i_reg += 1
        else:
            while (tomados_este_bloque < TAMANO_BLOQUE_REGULAR
                   and i_reg < len(lista_c33)
                   and len(merged) < tope_c33_total):
                merged.append(lista_c33[i_reg]); i_reg += 1
                tomados_este_bloque += 1
            if tomados_este_bloque == 0 and i_nf < len(nueva_flota_rotada):
                while i_nf < len(nueva_flota_rotada) and len(merged) < tope_c33_total:
                    merged.append(nueva_flota_rotada[i_nf]); i_nf += 1
        turno_nf = not turno_nf

    # lo que sobro del grupo regular de CRA33 va al excedente, en su orden original
    excedente.extend(lista_c33[i_reg:])

    visita_c33 = _numero_de_visita(home_c33, corredor_c33, dia)
    ruta_a, ruta_b = rutas_c33
    lista_a, lista_b = _split_por_paridad(merged, invertir=(visita_c33 % 2 == 1))
    asignacion[ruta_a] = lista_a[: topes_por_ruta_fisica[ruta_a]]
    asignacion[ruta_b] = lista_b[: topes_por_ruta_fisica[ruta_b]]
    # si por algun ajuste sobran del propio split de CRA33 (no deberia pasar si los numeros cuadran)
    excedente.extend(lista_a[topes_por_ruta_fisica[ruta_a]:])
    excedente.extend(lista_b[topes_por_ruta_fisica[ruta_b]:])

    # 4. Procesar los demas corredores (base = su propia cohorte de hoy)
    for corredor in CICLO_CORREDORES:
        if corredor == corredor_c33:
            continue
        home = cohorte_en_corredor[corredor]
        lista = rotados[home]
        rutas = CORREDOR_RUTAS_FISICAS[corredor]

        if len(rutas) == 1:
            ruta = rutas[0]
            tope = topes_por_ruta_fisica[ruta]
            asignacion[ruta] = lista[:tope]
            excedente.extend(lista[tope:])
        else:
            visita = _numero_de_visita(home, corredor, dia)
            ruta_a, ruta_b = rutas
            lista_a, lista_b = _split_por_paridad(lista, invertir=(visita % 2 == 1))
            asignacion[ruta_a] = lista_a[: topes_por_ruta_fisica[ruta_a]]
            asignacion[ruta_b] = lista_b[: topes_por_ruta_fisica[ruta_b]]
            excedente.extend(lista_a[topes_por_ruta_fisica[ruta_a]:])
            excedente.extend(lista_b[topes_por_ruta_fisica[ruta_b]:])

    # 5. Redistribuir excedente segun prioridad, llenando cupos libres
    idx_exc = 0
    for corredor in PRIORIDAD_EXCEDENTE:
        rutas = CORREDOR_RUTAS_FISICAS[corredor]
        for ruta in rutas:
            tope = topes_por_ruta_fisica[ruta]
            libres = tope - len(asignacion[ruta])
            if libres > 0 and idx_exc < len(excedente):
                tomar = excedente[idx_exc: idx_exc + libres]
                asignacion[ruta].extend(tomar)
                idx_exc += len(tomar)

    sin_asignar = excedente[idx_exc:]
    return asignacion, sin_asignar
