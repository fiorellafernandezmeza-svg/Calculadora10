import streamlit as st
from datetime import datetime, timedelta
import calendar
from datetime import date

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

# Datos de AFP combinados
afp_dict = {
    "HABITAT FLUJO": 0.1284,
    "INTEGRA FLUJO": 0.1292,
    "PRIMA FLUJO": 0.1297,
    "PROFUTURO FLUJO": 0.1306,
    "AFP MIXTA": 0.1137,
    "ONP": 0.13,
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
    
def calcular_tarifas(sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, turno):
# Ajustes especiales por tipo de trabajador y turno
    if tipo_trabajador == "Obrero" and turno == "Día":
        tipo_trabajador = "Empleado"
    if turno == "Noche - Rotativo":
        sueldo_base = max(sueldo_base, 1525.50)
    
    # --- 1️⃣ Cálculo de tarifa ordinaria (igual que antes) ---
    base_diaria_ordinaria = (sueldo_base + asignacion_familiar) / dias_mes
    tarifa_hora = (base_diaria_ordinaria / 8) * (1 - afp_descuento)

    # --- 2️⃣ Cálculo de base para horas extra (siempre sobre 30 días) ---
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

st.warning("""
⚠️ **Importante:**  
El cálculo mostrado es solo una guía. No considera descuentos de 5ta categoría, préstamos, comedor ni otros.  
Incluye únicamente el descuento de AFP u ONP.
""")

tipo_trabajador = st.selectbox("Tipo de trabajador", ["Empleado", "Obrero"])
turno = st.selectbox("Turno", ["Día", "Rotativo"])
sueldo_base = st.number_input("Sueldo base", min_value=0.0)
asignacion_familiar = st.number_input("Asignación familiar", min_value=0.0)
dias_mes = st.number_input("Días del mes", min_value=1, max_value=31, value=30)
afp = st.selectbox("Tipo de AFP", list(afp_dict.keys()))
afp_descuento = afp_dict[afp]

if turno == "Día":
    st.subheader("Turno Día")
    col1, col2, col3 = st.columns(3)
    with col1:
        hora_ingreso_dia = st.time_input("Hora de ingreso (Día - Rotativo)", value=datetime.strptime("08:00", "%H:%M").time())
    with col2:
        hora_salida_dia = st.time_input("Hora de salida (Día - Rotativo)", value=datetime.strptime("17:00", "%H:%M").time())
    with col3:
        horas_dia = calcular_horas_trabajadas(
            datetime.combine(datetime.today(), hora_ingreso_dia),
            datetime.combine(datetime.today(), hora_salida_dia)
        )
        st.metric("Horas trabajadas (Día)", f"{horas_dia:.2f}")

    tarifa_dia, extra25_dia, extra35_dia = calcular_tarifas(
        sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, "Día"
    )
    neto_dia, neto25_dia, neto35_dia, total_dia = calcular_netos(
        horas_dia, tarifa_dia, extra25_dia, extra35_dia
    )
    st.write(f"Tarifa hora ordinaria: S/ {tarifa_dia:.2f}")
    _ = f"Tarifa hora extra 25%: S/ {extra25_dia:.2f}"
    _ = f"Tarifa hora extra 35%: S/ {extra35_dia:.2f}"
    st.success(f"Neto por 8 horas: S/ {neto_dia:.2f}")
    _ = f"Neto por horas extra 25%: S/ {neto25_dia:.2f}"
    _ = f"Neto por horas extra 35%: S/ {neto35_dia:.2f}"
    st.success(f"Total turno día: S/ {total_dia:.2f}")

elif turno == "Rotativo":
    col_dia, col_noche = st.columns(2)

    with col_dia:
        st.subheader("Turno Día (Rotativo)")
        c1, c2, c3 = st.columns(3)
        with c1:
            hora_ingreso_dia = st.time_input("Hora de ingreso", key="ingreso_dia", value=datetime.strptime("08:00", "%H:%M").time())
        with c2:
            hora_salida_dia = st.time_input("Hora de salida", key="salida_dia", value=datetime.strptime("17:00", "%H:%M").time())
        with c3:
            horas_dia = calcular_horas_trabajadas(
                datetime.combine(datetime.today(), hora_ingreso_dia),
                datetime.combine(datetime.today(), hora_salida_dia)
            )
            st.metric("Horas trabajadas (Día)", f"{horas_dia:.2f}")
        tarifa_dia, extra25_dia, extra35_dia = calcular_tarifas(
            sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, "Día"
        )
        neto_dia, neto25_dia, neto35_dia, total_dia = calcular_netos(
            horas_dia, tarifa_dia, extra25_dia, extra35_dia
        )
        st.write(f"Tarifa hora ordinaria: S/ {tarifa_dia:.2f}")
        _ = f"Tarifa hora extra 25%: S/ {extra25_dia:.2f}"
        _ = f"Tarifa hora extra 35%: S/ {extra35_dia:.2f}"
        st.success(f"Neto por 8 horas: S/ {neto_dia:.2f}")
        _ = f"Neto por horas extra 35%: S/ {neto35_dia:.2f}"
        _ = f"Neto por horas extra 35%: S/ {neto35_dia:.2f}"
        st.success(f"Total turno día: S/ {total_dia:.2f}")

    with col_noche:
        st.subheader("Turno Noche (Rotativo)")
        c1, c2, c3 = st.columns(3)
        with c1:
            hora_ingreso_noche = st.time_input("Hora de ingreso", key="ingreso_noche", value=datetime.strptime("22:00", "%H:%M").time())
        with c2:
            hora_salida_noche = st.time_input("Hora de salida", key="salida_noche", value=datetime.strptime("07:00", "%H:%M").time())
        with c3:
            horas_noche = calcular_horas_trabajadas(
                datetime.combine(datetime.today(), hora_ingreso_noche),
                datetime.combine(datetime.today(), hora_salida_noche)
            )
            st.metric("Horas trabajadas (Noche)", f"{horas_noche:.2f}")
        tarifa_noche, extra25_noche, extra35_noche = calcular_tarifas(
            sueldo_base, asignacion_familiar, dias_mes, afp_descuento, tipo_trabajador, "Noche - Rotativo"
        )
        neto_noche, neto25_noche, neto35_noche, total_noche = calcular_netos(
            horas_noche, tarifa_noche, extra25_noche, extra35_noche
        )
        st.write(f"Tarifa hora ordinaria: S/ {tarifa_noche:.2f}")
        _ = f"Tarifa hora extra 25%: S/ {extra25_noche:.2f}"
        _ = f"Tarifa hora extra 35%: S/ {extra35_noche:.2f}"
        st.success(f"Neto por 8 horas: S/ {neto_noche:.2f}")
        _ = f"Neto por horas extra 25%: S/ {neto25_noche:.2f}"
        _ = f"Neto por horas extra 35%: S/ {neto35_noche:.2f}"
        st.success(f"Total turno noche: S/ {total_noche:.2f}")

    # Nuevas opciones de pago
    st.markdown("### 🗓️ Información de pago")
    tipo_pago = st.selectbox("Tipo de pago", ["Semanal", "Quincenal"])
    turno_inicio_pago = st.selectbox("Turno del primer día de pago", ["Día", "Noche"])
    mes_pago = st.selectbox("Mes de pago", [calendar.month_name[i] for i in range(1, 13)])

    # Función para obtener nombre del día
    def nombre_dia(fecha):
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        return dias[fecha.weekday()]

    # Mostrar cuadro según selección
        
    if tipo_pago == "Semanal":
        st.markdown("### 📅 Calculo semanal (mes completo)")
        year = 2025
        mes_num = list(calendar.month_name).index(mes_pago)
        dias_mes = calendar.monthrange(year, mes_num)[1]
        
        pagos = []
        turno_semana = turno_inicio_pago
        pago_semana = 0
        dias_semana = []
        
        st.write("**Día | Nombre | Turno | Pago diario**")
        
        for dia in range(1, dias_mes + 1):
            fecha = date(year, mes_num, dia)
            nombre = nombre_dia(fecha)

            # 🔁 Cambio de turno cada lunes (excepto el primer día)
            if nombre == "lunes" and dia != 1:
                turno_semana = "Noche" if turno_semana == "Día" else "Día"

            # 💰 Cálculo del pago diario
            if es_feriado(fecha):
                pago = neto_dia  # feriado se paga como día neto (8 horas turno día)
                feriado_flag = "🟥"
            else:
                if nombre == "domingo":
                    pago = neto_dia if turno_semana == "Día" else neto_noche
                    feriado_flag = ""
                else:
                    pago = total_dia if turno_semana == "Día" else total_noche
                    feriado_flag = ""

            pagos.append(pago)
            dias_semana.append((dia, nombre, turno_semana, pago, feriado_flag))
            pago_semana += pago

            # 📅 Cierre semanal cada viernes o fin de mes
            if nombre == "viernes" or dia == dias_mes:
             
                st.markdown(f"**Semana que termina el viernes {dia:02d} de {mes_pago}:**")
                for d, n, t, p, f in dias_semana:
                    st.write(f"{d:02d} | {n.capitalize()} | {t} | {f} S/ {p:.2f}")
                st.success(f"**Total semana ({dias_semana[0][0]:02d}–{dia:02d}): S/ {pago_semana:.2f}**")

                pago_semana = 0
                dias_semana = []

        total_mes = sum(pagos)
        st.markdown("---")
        st.success(f"💰 **Total mensual ({mes_pago}): S/ {total_mes:.2f}**")

    elif tipo_pago == "Quincenal":
        st.markdown("### 📅 Cálculo quincenal (mes completo)")

        year = 2025
        mes_num = list(calendar.month_name).index(mes_pago)
        dias_en_mes = calendar.monthrange(year, mes_num)[1]

        pagos = []
        st.write("**Día | Nombre | Pago diario**")
        turno_semana = turno_inicio_pago

        total_quincena_1 = 0
        total_quincena_2 = 0

        for dia in range(1, dias_en_mes + 1):
            fecha = date(year, mes_num, dia)
            nombre = nombre_dia(fecha)

            # 🔁 Cambio de turno cada lunes (excepto el primer día)
            if nombre == "lunes" and dia != 1:
                turno_semana = "Noche" if turno_semana == "Día" else "Día"

            # 💰 Feriado: pago fijo día
            if es_feriado(fecha):
                pago = neto_dia
                feriado_flag = "🟥"
            else:
                # Domingo paga neto según turno actual
                if nombre == "domingo":
                    pago = neto_dia if turno_semana == "Día" else neto_noche
                    feriado_flag = ""
                else:
                    pago = total_dia if turno_semana == "Día" else total_noche
                    feriado_flag = ""

            pagos.append(pago)
            st.write(f"{dia:02d} | {nombre.capitalize()} {feriado_flag} | S/ {pago:.2f}")

            # 🔹 Suma automática al final de cada quincena
            if dia == 15:
                total_quincena_1 = sum(pagos)
                st.success(f"**🟦 Total primera quincena: S/ {total_quincena_1:.2f}**")
                st.markdown("---")

            if dia == dias_en_mes:
                total_quincena_2 = sum(pagos[15:])  # del 16 en adelante
                st.success(f"**🟩 Total segunda quincena: S/ {total_quincena_2:.2f}**")
                st.markdown("---")

        # 🔸 Total general del mes
        total_mes = total_quincena_1 + total_quincena_2
        st.info(f"💰 **Total mes completo: S/ {total_mes:.2f}**")
