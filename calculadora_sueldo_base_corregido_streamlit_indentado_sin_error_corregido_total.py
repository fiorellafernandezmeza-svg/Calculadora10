import streamlit as st
from datetime import datetime, timedelta
import calendar
from datetime import date

# --- 🔹 Feriados oficiales Perú 2026 ---
FERIADOS_PERU_2026 = [
    "2026-01-01",  # Año Nuevo
    "2026-04-02",  # Jueves Santo
    "2026-04-03",  # Viernes Santo
    "2026-05-01",  # Día del Trabajo
    "2026-06-07",  # Nuevo
    "2026-06-29",  # Nuevo
    "2026-07-23",  # Independencia del Perú
    "2026-07-28",  # Independencia del Perú
    "2026-07-29",  # Fiestas Patrias
    "2026-08-06",  # Nuevo
    "2026-08-30",  # Santa Rosa de Lima
    "2026-10-08",  # Combate de Angamos
    "2026-11-01",  # Todos los Santos
    "2026-12-08",  # Inmaculada Concepción
    "2026-12-09",  # Batalla de Ayacucho
    "2026-12-25",  # Navidad
]


def es_feriado(fecha):
    """Verifica si una fecha es feriado en Perú."""
    return fecha.strftime("%Y-%m-%d") in FERIADOS_PERU_2026

# Datos de AFP combinados
af...