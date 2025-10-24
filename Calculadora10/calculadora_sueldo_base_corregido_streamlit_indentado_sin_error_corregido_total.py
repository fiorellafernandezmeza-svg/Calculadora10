import streamlit as st
from datetime import datetime, timedelta, date
import calendar

# --- 🔹 Feriados oficiales Perú 2025 ---
FERIADOS_PERU_2025 = [
    "2025-01-01",  # Año Nuevo
    "2025-03-03",  # Lunes de Carnaval
    "2025-03-04",  # Martes de Carnaval
    "2025-04-17",  # Jueves Santo
    "2025-04-18",  # Viernes Santo
    "2025-05-01",  # Día del Trabajo
    "2025-06-07",  # Nuevo
    "2025-06-29",  # San Pedro y San Pablo
    "2025-07-23",  # Nuevo
    "2025-07-28",  # Independencia del Perú
    "2025-07-29",  # Fiestas Patrias
    "2025-08-06",  # Nuevo
    "2025-08-30",  # Santa Rosa de Lima
    "2025-10-08",  # Combate de Angamos
    "2025-11-01",  # Todos los Santos
    "2025-12-08",  # Inmaculada Concepción
    "2025-12-09",  # Batalla de Ayacucho
    "2025-12-25",  # Navidad
]

def es_feriado(fecha):
    """Verifica si una fecha es feriado en Perú."""
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

# --- Cálculo de horas trabajadas ---
def calcular_horas_trabajadas(hora_ingreso, hora_salida):
    if hora_salida < hora_ingreso:
        hora_salida += timedelta(days=1)
    horas_trabajadas = (hora_salida - hora_ingreso).total_seconds() / 3600 - 0.75
    return max(horas_trabajadas, 0)

# --- Función para calcular tarifas ---
def calcular_tarifas(sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, turno):
    # Ajustes especiales por tipo de trabajador y turno
    if tipo_trabajador == "Obrero" and turno == "Día":
        tipo_trabajador = "Empleado"
    if turno == "Noche - Rotativo":
        sueldo_base = max(sueldo_base, 1525.50)

    # --- 1️⃣ Cálculo de tarifa ordinaria ---
    base_diaria_ordinaria = (sueldo_base + asignacion_familiar) / dias_mes
    tarifa_hora = (base_diaria_ordinaria / 8) * (1 - afp_descuento)

    # --- 2️⃣ Cálculo de base para horas extra ---
    base_diaria_extra = (sueldo_base + asignacion_familiar) / 30
    tarifa_base_extra = (base_diaria_extra / 8) * (1 - afp_descuento)

    # --- 3️⃣ Cálculo de tarifas de horas extra ---
    if turno == "Noche - Rotativo":
        extra_25 = tarifa_base_extra * (1.25 if tipo_trabajador == "Empleado" else 1.40)
        extra_35 = tarifa_base_extra * (1.35 if tipo_trabajador == "Empleado" else 1.50)
    else:
        extra_25 = tarifa_base_extra * 1.25
        extra_35 = tarifa_base_extra * 1.35

    return tarifa_hora, extra_25, extra_35

# --- Cálculo de netos ---
def calcular_netos(horas, tarifa_hora, tarifa_25, tarifa_35):
    h_ordinarias = min(horas, 8)
    h_extra_25 = min(max(horas - 8, 0), 2)
    h_extra_35 = max(horas - 10, 0)
    neto_ordinario = h_ordinarias * tarifa_hora
    neto_25 = h_extra_25 * tarifa_25
    neto_35 = h_extra_35 * tarifa_35
    total = neto_ordinario + neto_25 + neto_35
    return neto_ordinario, neto_25, neto_35, total

# --- INTERFAZ PRINCIPAL ---
st.title("💼 Calculadora de Sueldo por Turno")

st.warning("""
⚠️ **Nota Importante:**
Los cálculos mostrados son solo referenciales.
No incluyen descuentos de 5ta categoría, préstamos, retenciones judiciales, comedor u otros.
Solo se aplica el descuento de AFP u ONP según horario y turno.
""")

# --- Selección inicial ---
tipo_trabajador = st.selectbox("Tipo de trabajador", ["Empleado", "Obrero"])
turno = st.selectbox("Turno", ["Día", "Rotativo"])
sueldo_base = st.number_input("Sueldo base (S/)", min_value=0.0)
asignacion_familiar = st.number_input("Asignación familiar (S/)", min_value=0.0)
dias_mes = st.number_input("Días del mes", min_value=1, max_value=31, value=30)
afp = st.selectbox("Tipo de AFP", list(afp_dict.keys()))
afp_descuento = afp_dict[afp]

# --- Cálculo para EMPLEADO ---
if tipo_trabajador == "Empleado":
    st.markdown("### 👔 Cálculo de Pago Mensual - Empleado")

    ingreso_bruto = sueldo_base + asignacion_familiar
    st.write(f"**Ingreso bruto mensual:** S/ {ingreso_bruto:.2f}")

    tipo_aporte = "AFP" if afp != "ONP" else "ONP"
    descuento = ingreso_bruto * afp_descuento
    st.write(f"**Descuento {tipo_aporte}:** S/ {descuento:.2f}")

    pago_neto = ingreso_bruto - descuento
    st.success(f"💰 **Pago neto del mes:** S/ {pago_neto:.2f}")

    st.markdown("""
    > 🔹 Cálculo basado en jornada completa de 8 horas diarias.  
    > 🔹 No considera descuentos adicionales ni beneficios extras.
    """)

# --- Cálculo para OBRERO ---
elif tipo_trabajador == "Obrero":

    if turno == "Día":
        st.subheader("☀️ Turno Día")

        col1, col2, col3 = st.columns(3)
        with col1:
            hora_ingreso_dia = st.time_input("Hora ingreso", value=datetime.strptime("08:00", "%H:%M").time())
        with col2:
            hora_salida_dia = st.time_input("Hora salida", value=datetime.strptime("17:00", "%H:%M").time())
        with col3:
            horas_dia = calcular_horas_trabajadas(
                datetime.combine(datetime.today(), hora_ingreso_dia),
                datetime.combine(datetime.today(), hora_salida_dia)
            )
            st.metric("Horas trabajadas", f"{horas_dia:.2f}")

        tarifa_dia, extra25_dia, extra35_dia = calcular_tarifas(
            sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, "Día"
        )

        neto_dia, neto25_dia, neto35_dia, total_dia = calcular_netos(
            horas_dia, tarifa_dia, extra25_dia, extra35_dia
        )

        st.write(f"Tarifa hora ordinaria: S/ {tarifa_dia:.2f}")
        st.success(f"Total turno día: S/ {total_dia:.2f}")

        # --- Información de pago ---
        st.markdown("### 🗓️ Información de pago")
        tipo_pago = st.selectbox("Tipo de pago", ["Semanal", "Quincenal"])
        mes_pago = st.selectbox("Mes de pago", [calendar.month_name[i] for i in range(1, 13)])

        def nombre_dia(fecha):
            dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
            return dias[fecha.weekday()]

        year = 2025
        mes_num = list(calendar.month_name).index(mes_pago)
        dias_en_mes = calendar.monthrange(year, mes_num)[1]

        # --- SEMANAL ---
        if tipo_pago == "Semanal":
            st.markdown("### 📅 Cálculo Semanal (Turno Día)")
            pagos, dias_semana, pago_semana = [], [], 0

            for dia in range(1, dias_en_mes + 1):
                fecha = date(year, mes_num, dia)
                nombre = nombre_dia(fecha)
                if es_feriado(fecha) or nombre == "domingo":
                    pago = neto_dia
                    feriado_flag = "🟥" if es_feriado(fecha) else ""
                else:
                    pago = total_dia
                    feriado_flag = ""
                pagos.append(pago)
                dias_semana.append((dia, nombre, pago, feriado_flag))
                pago_semana += pago

                if nombre == "viernes" or dia == dias_en_mes:
                    st.markdown(f"**Semana que termina el {dia:02d} {mes_pago}:**")
                    for d, n, p, f in dias_semana:
                        st.write(f"{d:02d} | {n.capitalize()} {f} | S/ {p:.2f}")
                    st.success(f"**Total semana: S/ {pago_semana:.2f}**")
                    dias_semana, pago_semana = [], 0

            st.markdown("---")
            st.success(f"💰 **Total mensual ({mes_pago}): S/ {sum(pagos):.2f}**")

        # --- QUINCENAL ---
        elif tipo_pago == "Quincenal":
            st.markdown("### 📅 Cálculo Quincenal (Turno Día)")
            pagos = []

            # Primera quincena
            for dia in range(1, 16):
                fecha = date(year, mes_num, dia)
                nombre = nombre_dia(fecha)
                pago = neto_dia if (es_feriado(fecha) or nombre == "domingo") else total_dia
                pagos.append(pago)
            total_q1 = sum(pagos)
            st.success(f"**Total primera quincena: S/ {total_q1:.2f}**")

            # Segunda quincena
            pagos2 = []
            for dia in range(16, dias_en_mes + 1):
                fecha = date(year, mes_num, dia)
                nombre = nombre_dia(fecha)
                pago = neto_dia if (es_feriado(fecha) or nombre == "domingo") else total_dia
                pagos2.append(pago)
            total_q2 = sum(pagos2)

            st.success(f"**Total segunda quincena: S/ {total_q2:.2f}**")
            st.markdown("---")
            st.success(f"💰 **Total mensual ({mes_pago}): S/ {total_q1 + total_q2:.2f}**")
