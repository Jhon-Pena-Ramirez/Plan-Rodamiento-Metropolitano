"""
Determina si una fecha es 'habil' o 'festivo' (incluye domingos y festivos de Colombia).

Requiere la libreria 'holidays' (ver requirements.txt). Si no esta disponible
(por ejemplo, en un entorno sin internet), se usa un respaldo que solo detecta
domingos, para no detener el programa -- pero para produccion SIEMPRE debe
estar instalada la libreria 'holidays'.
"""
try:
    import holidays as _holidays_lib
    _HOLIDAYS_OK = True
except ImportError:
    _HOLIDAYS_OK = False

_cache_festivos = {}


def tipo_de_dia(fecha):
    if fecha.weekday() == 6:  # domingo
        return "festivo"

    if _HOLIDAYS_OK:
        if fecha.year not in _cache_festivos:
            _cache_festivos[fecha.year] = _holidays_lib.CO(years=fecha.year)
        if fecha in _cache_festivos[fecha.year]:
            return "festivo"
    return "habil"

