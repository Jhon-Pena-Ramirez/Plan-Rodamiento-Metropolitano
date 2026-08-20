"""
App web para generar el Plan de Rodamiento mensual.
Ejecutar localmente con:  streamlit run app.py
"""
import sys
import os
import tempfile
from datetime import datetime

import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from generar_plan import generar_plan_mensual  # noqa: E402

st.set_page_config(page_title="Plan de Rodamiento", page_icon="🚌", layout="centered")

st.title("🚌 Generador de Plan de Rodamiento")
st.write(
    "Sube los 3 archivos base, elige el mes a generar y descarga el plan "
    "de rodamiento completo en Excel."
)

st.header("1. Archivos base")
col1, col2, col3 = st.columns(3)
with col1:
    f_vehiculos = st.file_uploader("Base de vehículos", type=["xlsx"])
with col2:
    f_horarios = st.file_uploader("Horarios (topes y recorridos)", type=["xlsx"])
with col3:
    f_sorteo = st.file_uploader("Sorteo (orden inicial)", type=["xlsx"])

st.header("2. Mes a generar")
meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]
col_a, col_b = st.columns(2)
with col_a:
    mes_nombre = st.selectbox("Mes", meses, index=datetime.now().month - 1)
    mes = meses.index(mes_nombre) + 1
with col_b:
    anio = st.number_input("Año", min_value=2024, max_value=2035, value=datetime.now().year, step=1)

st.header("3. Generar")
listo = f_vehiculos and f_horarios and f_sorteo

if st.button("Generar plan de rodamiento", type="primary", disabled=not listo):
    with tempfile.TemporaryDirectory() as tmp:
        path_veh = os.path.join(tmp, "vehiculos.xlsx")
        path_hor = os.path.join(tmp, "horarios.xlsx")
        path_sor = os.path.join(tmp, "sorteo.xlsx")
        path_out = os.path.join(tmp, f"plan_rodamiento_{anio}_{mes:02d}.xlsx")

        with open(path_veh, "wb") as fh:
            fh.write(f_vehiculos.getbuffer())
        with open(path_hor, "wb") as fh:
            fh.write(f_horarios.getbuffer())
        with open(path_sor, "wb") as fh:
            fh.write(f_sorteo.getbuffer())

        try:
            with st.spinner("Calculando rotación, turnos y horarios..."):
                resultado = generar_plan_mensual(
                    path_veh, path_hor, path_sor, anio, mes, path_out
                )
            with open(path_out, "rb") as fh:
                datos = fh.read()

            st.success(f"Plan generado: {resultado['dias_generados']} días procesados.")

            if resultado["sin_asignar"]:
                dias_afectados = len(resultado["sin_asignar"])
                st.warning(
                    f"⚠️ En {dias_afectados} día(s) del mes quedaron vehículos "
                    "sin ruta asignada (no había cupo suficiente ese día)."
                )

            st.download_button(
                "⬇️ Descargar plan de rodamiento (.xlsx)",
                data=datos,
                file_name=f"plan_rodamiento_{anio}_{mes:02d}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        except Exception as e:
            st.error(f"Ocurrió un error generando el plan: {e}")
elif not listo:
    st.info("Sube los 3 archivos para habilitar la generación.")
