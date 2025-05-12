import streamlit as st
from secciones import quienes_somos, objetivo, contacto, dashboard

st.set_page_config(page_title="Impulsa Digital Dashboard", layout="wide")

# Barra de navegación
secciones = {
    "Quiénes somos": quienes_somos.mostrar,
    "Nuestro objetivo": objetivo.mostrar,
    "Contacto": contacto.mostrar,
    "Dashboard": dashboard.mostrar,
}

st.sidebar.title("Impulsa Digital")
opcion = st.sidebar.radio("Navegación", list(secciones.keys()))

# Mostrar la sección elegida
secciones[opcion]()