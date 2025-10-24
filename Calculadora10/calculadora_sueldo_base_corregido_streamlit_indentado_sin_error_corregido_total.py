import streamlit as st
from datetime import datetime, timedelta, date
import calendar

# --- 🔹 Feriados oficiales Perú 2025 ---
FERIADOS_PERU_2025 = [
    "2025-01-01", "2025-03-03", "2025-03-04", "2025-04-17", "2025-04-18",
    "2025-05-01", "2025-06-07", "2025-06-29", "2025-07-23", "2025-07-28",
    "2025-07-29", "2025-08-06", "2025-08-30", "2025-10-08", "2025-11-01",
    "2025-12-08", "2025-12-09", "2025-12-25"
]

def es_feriado(fecha):
    return fecha.strftime("%Y-%m-%d") in FERIADOS_PERU_2025

# --- AFP y ONP ---
afp_dict = {
    "HABITAT FLUJO": 0.1284,
    "INTEGRA FLUJO": 0.1292,
    "PRIMA FLUJO": 0.1297,
    "PROFUTURO FLUJO": 0.1306,
    "AFP MIXTA": 0.1137,
    "ONP": 0.13,
}

# --- Cálculo de horas ---
def calcular_horas_trabajadas(hora_ingreso, hora_salida):
    if hora_salida < hora_ingreso:
        hora_salida += timedelta(days=1)
    horas = (hora_salida - hora_ingreso).total_seconds() / 3600 - 0.75
    return max(horas, 0)

# --- Tarifas ---
def calcular_tarifas(sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, turno):
    if tipo_trabajador == "Obrero" and turno == "Día":
        tipo_trabajador = "Empleado"
    if turno == "Noche - Rotativo":
        sueldo_base = max(sueldo_base, 1525.50)

    base_diaria_ordinaria = (sueldo_base + asignacion_familiar) / dias_mes
    tarifa_hora = (base_diaria_ordinaria / 8) * (1 - afp_descuento)

    base_diaria_extra = (sueldo_base + asignacion_familiar) / 30
    tarifa_base_extra = (base_diaria_extra / 8) * (1 - afp_descuento)

    if turno == "Noche - Rotativo":
        extra_25 = tarifa_base_extra * (1.25 if tipo_trabajador == "Empleado" else 1.40)
        extra_35 = tarifa_base_extra * (1.35 if tipo_trabajador == "Empleado" else 1.50)
    else:
        extra_25 = tarifa_base_extra * 1.25
        extra_35 = tarifa_base_extra * 1.35

    return tarifa_hora, extra_25, extra_35

# --- Netos ---
def calcular_netos(horas, tarifa_hora, tarifa_25, tarifa_35):
    h_ordinarias = min(horas, 8)
    h_extra_25 = min(max(horas - 8, 0), 2)
    h_extra_35 = max(horas - 10, 0)
    neto_ordinario = h_ordinarias * tarifa_hora
    neto_25 = h_extra_25 * tarifa_25
    neto_35 = h_extra_35 * tarifa_35
    total = neto_ordinario + neto_25 + neto_35
    return neto_ordinario, neto_25, neto_35, total

# --- Interfaz principal ---
st.title("🧮 Calculadora de Sueldo por Turno")

st.info("""
🔹 **Nota importante:**  
Los cálculos mostrados **no incluyen descuentos adicionales** como 5ta categoría, retenciones judiciales, préstamos, comedor ni sobregiros.  
Solo se considera el **descuento de AFP u ONP** según el tipo seleccionado y el horario trabajado.
""")

# --- Entradas generales ---
tipo_trabajador = st.selectbox("Tipo de trabajador", ["Empleado", "Obrero"])
turno = st.selectbox("Turno", ["Día", "Rotativo"])
sueldo_base = st.number_input("Sueldo base (S/)", min_value=0.0)
asignacion_familiar = st.number_input("Asignación familiar (S/)", min_value=0.0)
dias_mes = st.number_input("Días del mes", min_value=1, max_value=31, value=30)
afp = st.selectbox("Tipo de AFP", list(afp_dict.keys()))
afp_descuento = afp_dict[afp]

# --- 👔 Empleado ---
if tipo_trabajador == "Empleado":
    st.subheader("👔 Cálculo de Pago Mensual - Empleado")

    ingreso_bruto = sueldo_base + asignacion_familiar
    st.write(f"**Ingreso bruto mensual:** S/ {ingreso_bruto:.2f}")

    tipo_aporte = "AFP" if afp != "ONP" else "ONP"
    descuento = ingreso_bruto * afp_descuento
    st.write(f"**Descuento {tipo_aporte}:** S/ {descuento:.2f}")

    pago_neto = ingreso_bruto - descuento
    st.success(f"💰 **Pago neto del mes:** S/ {pago_neto:.2f}")

    st.markdown("> 🟢 Jornada completa de 8 horas diarias.\n> 🟢 Solo aplica descuento de AFP u ONP.\n> 🟢 No incluye otros descuentos.")

# --- 👷 Obrero ---
elif tipo_trabajador == "Obrero":

    # Turno Día
    if turno == "Día":
        st.subheader("👷 Turno Día")

        col1, col2 = st.columns(2)
        with col1:
            hora_ingreso = st.time_input("Hora de ingreso", value=datetime.strptime("08:00", "%H:%M").time())
        with col2:
            hora_salida = st.time_input("Hora de salida", value=datetime.strptime("17:00", "%H:%M").time())

        horas_dia = calcular_horas_trabajadas(
            datetime.combine(datetime.today(), hora_ingreso),
            datetime.combine(datetime.today(), hora_salida)
        )
        st.metric("Horas trabajadas (Día)", f"{horas_dia:.2f}")

        tarifa_dia, extra25, extra35 = calcular_tarifas(
            sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, "Día"
        )
        neto_dia, neto25, neto35, total_dia = calcular_netos(horas_dia, tarifa_dia, extra25, extra35)

        st.write(f"**Tarifa hora ordinaria:** S/ {tarifa_dia:.2f}")
        st.success(f"**Total turno día:** S/ {total_dia:.2f}")

        # Información de pago
        tipo_pago = st.selectbox("Tipo de pago", ["Semanal", "Quincenal"])
        mes_pago = st.selectbox("Mes de pago", [calendar.month_name[i] for i in range(1, 13)])

        def nombre_dia(fecha):
            dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
            return dias[fecha.weekday()]

        year = 2025
        mes_num = list(calendar.month_name).index(mes_pago)
        dias_mes = calendar.monthrange(year, mes_num)[1]

        # Pago Semanal
        if tipo_pago == "Semanal":
            st.markdown("### 📅 Cuadro Semanal (Turno Día)")
            pagos, dias_semana = [], []
            pago_semana = 0

            for dia in range(1, dias_mes + 1):
                fecha = date(year, mes_num, dia)
                nombre = nombre_dia(fecha)
                if es_feriado(fecha) or nombre == "domingo":
                    pago = neto_dia
                    flag = "🟥"
                else:
                    pago = total_dia
                    flag = ""
                pagos.append(pago)
                dias_semana.append((dia, nombre, pago, flag))
                pago_semana += pago

                if nombre == "viernes" or dia == dias_mes:
                    st.markdown(f"**Semana que termina el {dia:02d}:**")
                    for d, n, p, f in dias_semana:
                        st.write(f"{d:02d} | {n.capitalize()} {f} | S/ {p:.2f}")
                    st.success(f"Total semana: S/ {pago_semana:.2f}")
                    pago_semana = 0
                    dias_semana = []

            st.success(f"💰 **Total mensual ({mes_pago}): S/ {sum(pagos):.2f}**")

        # Pago Quincenal
        elif tipo_pago == "Quincenal":
            st.markdown("### 📅 Cuadro Quincenal (Turno Día)")

            # Primera quincena
            pagos_q1 = []
            for dia in range(1, 16):
                fecha = date(year, mes_num, dia)
                nombre = nombre_dia(fecha)
                pago = neto_dia if es_feriado(fecha) or nombre == "domingo" else total_dia
                pagos_q1.append(pago)
            st.success(f"**Total primera quincena:** S/ {sum(pagos_q1):.2f}")

            # Segunda quincena
            pagos_q2 = []
            for dia in range(16, dias_mes + 1):
                fecha = date(year, mes_num, dia)
                nombre = nombre_dia(fecha)
                pago = neto_dia if es_feriado(fecha) or nombre == "domingo" else total_dia
                pagos_q2.append(pago)
            st.success(f"**Total segunda quincena:** S/ {sum(pagos_q2):.2f}")

            st.success(f"💰 **Total mensual ({mes_pago}): S/ {sum(pagos_q1) + sum(pagos_q2):.2f}**")

    # Turno Rotativo
    elif turno == "Rotativo":
        st.subheader("🌙 Turno Rotativo")
        col1, col2 = st.columns(2)
        with col1:
            hora_ingreso = st.time_input("Hora de ingreso (rotativo)", value=datetime.strptime("19:00", "%H:%M").time())
        with col2:
            hora_salida = st.time_input("Hora de salida (rotativo)", value=datetime.strptime("07:00", "%H:%M").time())

        horas_trab = calcular_horas_trabajadas(
            datetime.combine(datetime.today(), hora_ingreso),
            datetime.combine(datetime.today(), hora_salida)
        )
        st.metric("Horas trabajadas (Turno noche)", f"{horas_trab:.2f}")

        tarifa_rot, extra25, extra35 = calcular_tarifas(
            sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, "Noche - Rotativo"
        )
        neto_rot, neto25, neto35, total_rot = calcular_netos(horas_trab, tarifa_rot, extra25, extra35)

        st.write(f"**Tarifa hora ordinaria:** S/ {tarifa_rot:.2f}")
        st.success(f"**Total turno rotativo:** S/ {total_rot:.2f}")

        st.markdown("> 🔄 Aplica pago por turno noche con recargo y AFP/ONP correspondiente.")
