"""
Configuracion de corredores y su relacion con las rutas fisicas.
Si en el futuro cambia la estructura de corredores, se ajusta AQUI,
sin tocar la logica del motor de rotacion.
"""

# Ciclo de rotacion de corredores (orden fijo, 5 posiciones).
# El grupo que hoy esta en la posicion N, mañana pasa a la posicion N+1 (circular).
CICLO_CORREDORES = [
    "Kennedy",
    "CRA21_Tejaditos_Terminal",
    "CRA33_Nueva_Zafiro",
    "PuenteTierra",
    "CRA21_Nueva_Zafiro",
]

# Cada corredor puede tener 1 o 2 rutas fisicas (hojas del archivo de Horarios).
# El orden de la lista importa: el primero recibe las posiciones IMPARES
# del grupo (en la paridad "normal"); el segundo recibe las PARES.
CORREDOR_RUTAS_FISICAS = {
    "Kennedy": ["Kennedy"],
    "CRA21_Tejaditos_Terminal": ["Tejaditos", "Terminal"],
    "CRA33_Nueva_Zafiro": ["33Nueva", "33Zafiro"],
    "PuenteTierra": ["Puente T"],
    "CRA21_Nueva_Zafiro": ["21Nueva", "21Zafiro"],
}

# Nombre exacto de las hojas en el archivo de Horarios (deben coincidir con el excel).
# Si el nombre de una hoja cambia, se ajusta aqui.
HOJA_HORARIOS = {
    "Kennedy": "Kennedy",
    "Tejaditos": "Tejaditos",
    "Terminal": "Terminal ",   # ojo: en el archivo actual tiene un espacio al final
    "33Nueva": "33Nueva",
    "33Zafiro": "33Zafiro",
    "Puente T": "Puente T",
    "21Nueva": "21Nueva",
    "21Zafiro": "21Zafiro",
}

# Nombre exacto de los grupos/columnas en el archivo de Sorteo.
GRUPO_SORTEO = {
    "Kennedy": "KENNEDY",
    "CRA21_Tejaditos_Terminal": "CRA 21 TEJADITOS - TERMINAL",
    "CRA33_Nueva_Zafiro": "CRA 33 NUEVA - ZAFIRO",
    "PuenteTierra": "PUENTE TIERRA",
    "CRA21_Nueva_Zafiro": "CRA 21 NUEVA - ZAFIRO",
}
GRUPO_NUEVA_FLOTA = "NUEVA FLOTA"

# El corredor que recibe primero la Nueva Flota (fija, prioridad, nunca rota).
CORREDOR_NUEVA_FLOTA = "CRA33_Nueva_Zafiro"

# Orden de prioridad para repartir el excedente de vehiculos que no
# alcanzan a entrar en CRA33 (por la prioridad de Nueva Flota).
PRIORIDAD_EXCEDENTE = [
    "Kennedy",
    "CRA21_Tejaditos_Terminal",
    "PuenteTierra",
    "CRA21_Nueva_Zafiro",
]

# Cuantas posiciones se desplaza el orden interno de un grupo cada dia.
DESPLAZAMIENTO_ORDEN_DIARIO = 4

# Tamaño de los bloques al entrelazar Nueva Flota con el grupo regular de CRA33.
# Ej: 2 y 2 -> NF,NF,reg,reg,NF,NF,reg,reg,...
TAMANO_BLOQUE_NUEVA_FLOTA = 2
TAMANO_BLOQUE_REGULAR = 2
