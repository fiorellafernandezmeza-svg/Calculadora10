
import streamlit as st

# Datos de AFP
afp_dict = {
    "HABITAT": 0.1284,
    "INTEGRA": 0.1292,
    "PRIMA": 0.1297,
    "PROFUTURO": 0.1306,
    "HABITAT MIXTA": 0.1137,
    "INTEGRA MIXTA": 0.1137,
    "PRIMA MIXTA": 0.1137,
    "PROFUTURO MIXTA": 0.1137,
    "ONP": 0.13
}

st.title("Calculadora de Sueldo - Fiorella")

# Entrada de datos
sueldo_base = st.number_input("Sueldo base (mínimo S/ 1130)", min_value=1130.0, value=1130.0, step=0.1)
asignacion_familiar = st.selectbox("Asignación familiar", [0.0, 113.0])
afp_tipo = st.selectbox("Tipo de AFP", list(afp_dict.keys()))
dias_mes = st.selectbox("Total días del mes", [28, 30, 31])
turno = st.selectbox("Turno", ["Día", "Rotativo"])
tipo_trabajador = st.selectbox("Tipo de trabajador", ["Empleado", "Obrero"])

# Ajuste de sueldo base según turno
if turno == "Rotativo":
    sueldo_base_calculo = max(sueldo_base, 1525.50)
else:
    sueldo_base_calculo = sueldo_base

# Cálculo de tarifa por hora ordinaria neto
afp_descuento = afp_dict[afp_tipo]
tarifa_hora_neta = ((sueldo_base_calculo + asignacion_familiar) / dias_mes / 8) * (1 - afp_descuento)
st.write(f"Tarifa por hora ordinaria neto: S/ {tarifa_hora_neta:.2f}")

# Cálculo de tarifa hora extra al 25% y 35% (si obrero y rotativo, usar 1.40 y 1.50)
if tipo_trabajador == "Obrero":
    tarifa_25 = (((sueldo_base_calculo + asignacion_familiar) / 30 / 8) * (1 - afp_descuento)) * 1.40
    tarifa_35 = (((sueldo_base_calculo + asignacion_familiar) / 30 / 8) * (1 - afp_descuento)) * 1.50
else:
    tarifa_25 = (((sueldo_base_calculo + asignacion_familiar) / 30 / 8) * (1 - afp_descuento)) * 1.25
    tarifa_35 = (((sueldo_base_calculo + asignacion_familiar) / 30 / 8) * (1 - afp_descuento)) * 1.35

st.write(f"Tarifa hora extra al 25% (Día): S/ {tarifa_25:.2f}")
st.write(f"Tarifa hora extra al 35% (Día): S/ {tarifa_35:.2f}")
