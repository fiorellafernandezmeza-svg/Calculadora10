
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
    if turno == "Noche - Rotativo":
        sueldo_base = max(sueldo_base, 1525.50)
    base_diaria = (sueldo_base + asignacion_familiar) / dias_mes
    tarifa_hora = (base_diaria / 8) * (1 - afp_descuento)
    if turno == "Noche - Rotativo":
        extra_25 = tarifa_hora * (1.25 if tipo_trabajador == "Empleado" else 1.40)
        extra_35 = tarifa_hora * (1.35 if tipo_trabajador == "Empleado" else 1.50)
    else:
        if tipo_trabajador == "Obrero":
            extra_25 = tarifa_hora * 1.25
            extra_35 = tarifa_hora * 1.35
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
