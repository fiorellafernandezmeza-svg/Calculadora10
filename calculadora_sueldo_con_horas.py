import streamlit as st
from datetime import datetime, timedelta

# Datos de AFP combinados
afp_dict = {
    "HABITAT": 0.1284,
    "INTEGRA": 0.1292,
    "PRIMA": 0.1297,
    "PROFUTURO": 0.1306,
    "HABITAT MIXTA": 0.1137,
    "INTEGRA MIXTA": 0.1137,
    "PRIMA MIXTA": 0.1137,
    "PROFUTURO MIXTA": 0.1137,
    "ONP": 0.13,
    "Prima": 0.1147,
    "Integra": 0.1146,
    "Profuturo": 0.1145,
    "Habitat": 0.1149
}

# Función para calcular horas trabajadas descontando 45 minutos de refrigerio
def calcular_horas_trabajadas(hora_ingreso, hora_salida):
    if hora_salida < hora_ingreso:
        hora_salida += timedelta(days=1)
    horas_trabajadas = (hora_salida - hora_ingreso).total_seconds() / 3600 - 0.75
    return max(horas_trabajadas, 0)

# Función para calcular tarifas
def calcular_tarifas(sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, turno):
    if tipo_trabajador == "Obrero" and turno == "Día":
        tipo_trabajador = "Empleado"
    if turno == "Noche - Rotativo":
        sueldo_base = max(sueldo_base, 1525.50)
    base_diaria = (sueldo_base + asignacion_familiar) / dias_mes
    tarifa_hora = (base_diaria / 8) * (1 - afp_descuento)
    if turno == "Noche - Rotativo":
        extra_25 = tarifa_hora * (1.25 if tipo_trabajador == "Empleado" else 1.40)
        extra_35 = tarifa_hora * (1.35 if tipo_trabajador == "Empleado" else 1.50)
    else:
        extra_25 = tarifa_hora * 1.25
        extra_35 = tarifa_hora * 1.35
    return tarifa_hora, extra_25, extra_35

# Función para calcular netos
def calcular_netos(horas, tarifa_hora, tarifa_25, tarifa_35):
    h_ordinarias = min(horas, 8)
    h_extra_25 = min(max(horas - 8, 0), 2)
    h_extra_35 = max(horas - 10, 0)
    neto_ordinario = h_ordinarias * tarifa_hora
    neto_25 = h_extra_25 * tarifa_25
    neto_35 = h_extra_35 * tarifa_35
    total = neto_ordinario + neto_25 + neto_35
    return neto_ordinario, neto_25, neto_35, total

# Interfaz de usuario
st.title("Calculadora de Sueldo por Turno")

tipo_trabajador = st.selectbox("Tipo de trabajador", ["Empleado", "Obrero"])
turno = st.selectbox("Turno", ["Día", "Rotativo"])
sueldo_base = st.number_input("Sueldo base", min_value=0.0)
asignacion_familiar = st.number_input("Asignación familiar", min_value=0.0)
dias_mes = st.number_input("Días del mes", min_value=1, max_value=31, value=30)
afp = st.selectbox("Tipo de AFP", ["Prima", "Integra", "Profuturo", "Habitat"])
afp_descuentos = {"Prima": 0.1147, "Integra": 0.1146, "Profuturo": 0.1145, "Habitat": 0.1149}
afp_descuento = afp_descuentos[afp]

if turno == "Día":
    st.subheader("Turno Día")
    col1, col2, col3 = st.columns(3)
    with col1:
        hora_ingreso_dia = st.time_input("Hora de ingreso (Día - Rotativo)", value=datetime.strptime("08:00", "%H:%M").time())
    with col2:
        hora_salida_dia = st.time_input("Hora de salida (Día - Rotativo)", value=datetime.strptime("17:00", "%H:%M").time())
    with col3:
        horas_dia = calcular_horas_trabajadas(datetime.combine(datetime.today(), hora_ingreso_dia),
                                              datetime.combine(datetime.today(), hora_salida_dia))
        st.metric("Horas trabajadas (Día)", f"{horas_dia:.2f}")

    tarifa_dia, extra25_dia, extra35_dia = calcular_tarifas(sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, "Día")
    neto_dia, neto25_dia, neto35_dia, total_dia = calcular_netos(horas_dia, tarifa_dia, extra25_dia, extra35_dia)

    st.write(f"Tarifa hora ordinaria: S/ {tarifa_dia:.2f}")
    st.write(f"Tarifa hora extra 25%: S/ {extra25_dia:.2f}")
    st.write(f"Tarifa hora extra 35%: S/ {extra35_dia:.2f}")
    st.write(f"Neto por 8 horas: S/ {neto_dia:.2f}")
    st.write(f"Neto por horas extra 25%: S/ {neto25_dia:.2f}")
    st.write(f"Neto por horas extra 35%: S/ {neto35_dia:.2f}")
    st.success(f"Total turno día: S/ {total_dia:.2f}")

elif turno == "Rotativo":
    col_dia, col_noche = st.columns(2)

    with col_dia:
        st.subheader("Turno Día (Rotativo)")
        c1, c2, c3 = st.columns(3)
        with c1:
            hora_ingreso_dia = st.time_input("Hora de ingreso (Día - Rotativo)", key="ingreso_dia", value=datetime.strptime("08:00", "%H:%M").time())
        with c2:
            hora_salida_dia = st.time_input("Hora de salida (Día - Rotativo)", key="salida_dia", value=datetime.strptime("17:00", "%H:%M").time())
        with c3:
            horas_dia = calcular_horas_trabajadas(datetime.combine(datetime.today(), hora_ingreso_dia),
                                                  datetime.combine(datetime.today(), hora_salida_dia))
            st.metric("Horas trabajadas (Día)", f"{horas_dia:.2f}")

        tarifa_dia, extra25_dia, extra35_dia = calcular_tarifas(sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, "Día")
        neto_dia, neto25_dia, neto35_dia, total_dia = calcular_netos(horas_dia, tarifa_dia, extra25_dia, extra35_dia)

        st.write(f"Tarifa hora ordinaria: S/ {tarifa_dia:.2f}")
        st.write(f"Tarifa hora extra 25%: S/ {extra25_dia:.2f}")
        st.write(f"Tarifa hora extra 35%: S/ {extra35_dia:.2f}")
        st.write(f"Neto por 8 horas: S/ {neto_dia:.2f}")
        st.write(f"Neto por horas extra 25%: S/ {neto25_dia:.2f}")
        st.write(f"Neto por horas extra 35%: S/ {neto35_dia:.2f}")
        st.success(f"Total turno día: S/ {total_dia:.2f}")

    with col_noche:
        st.subheader("Turno Noche (Rotativo)")
        c1, c2, c3 = st.columns(3)
        with c1:
            hora_ingreso_noche = st.time_input("Hora de ingreso (Noche - Rotativo)", key="ingreso_noche", value=datetime.strptime("22:00", "%H:%M").time())
        with c2:
            hora_salida_noche = st.time_input("Hora de salida (Noche - Rotativo)", key="salida_noche", value=datetime.strptime("07:00", "%H:%M").time())
        with c3:
            horas_noche = calcular_horas_trabajadas(datetime.combine(datetime.today(), hora_ingreso_noche),
                                                    datetime.combine(datetime.today(), hora_salida_noche))
            st.metric("Horas trabajadas (Noche)", f"{horas_noche:.2f}")

        tarifa_noche, extra25_noche, extra35_noche = calcular_tarifas(sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, "Noche - Rotativo")
        neto_noche, neto25_noche, neto35_noche, total_noche = calcular_netos(horas_noche, tarifa_noche, extra25_noche, extra35_noche)

        st.write(f"Tarifa hora ordinaria: S/ {tarifa_noche:.2f}")
        st.write(f"Tarifa hora extra 25%: S/ {extra25_noche:.2f}")
        st.write(f"Tarifa hora extra 35%: S/ {extra35_noche:.2f}")
        st.write(f"Neto por 8 horas: S/ {neto_noche:.2f}")
        st.write(f"Neto por horas extra 25%: S/ {neto25_noche:.2f}")
        st.write(f"Neto por horas extra 35%: S/ {neto35_noche:.2f}")
        st.success(f"Total turno noche: S/ {total_noche:.2f}")
