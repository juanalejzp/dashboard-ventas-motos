import streamlit as st
import pandas as pd
import plotly.express as px

def mostrar():
    st.title("Dashboard de Ventas - Impulsa Digital")

    archivo = "OportunidadesComerciales_completo.xlsx"

    try:
        df = pd.read_excel(archivo)
        st.success("Archivo cargado correctamente.")

        # Filtros
        st.sidebar.subheader("Filtros")
        regiones = st.sidebar.multiselect("Filtrar por región", df["Ciudad"].dropna().unique())
        modelos = st.sidebar.multiselect("Filtrar por modelo", df["Modelo"].dropna().unique())

        if regiones:
            df = df[df["Ciudad"].isin(regiones)]
        if modelos:
            df = df[df["Modelo"].isin(modelos)]

        st.subheader("1. Perfiles de clientes más comunes")
        if "Edad" in df.columns and "Genero" in df.columns:
                df_filtrado = df[(df["Edad"] >= 20) & (df["Edad"] <= 70)]
                fig1 = px.histogram(df_filtrado, x="Edad", color="Genero", nbins=20,
                    title="Distribución por edad y género")
                st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("Faltan las columnas 'Edad' y/o 'Genero'.")

        st.subheader("2. Modelos de motos más populares por región")
        if "Modelo" in df.columns and "Ciudad" in df.columns:
            fig2 = px.histogram(df, x="Ciudad", color="Modelo", title="Popularidad de modelos por ciudad")
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("3. Tiempo promedio de conversión")
        if "Fecha de creación" in df.columns and "Fecha Compra" in df.columns:
            df["Fecha de creación"] = pd.to_datetime(df["Fecha de creación"], errors='coerce')
            df["Fecha Compra"] = pd.to_datetime(df["Fecha Compra"], errors='coerce')
            df["Tiempo de conversión"] = (df["Fecha Compra"] - df["Fecha de creación"]).dt.days
            fig3 = px.histogram(df, x="Tiempo de conversión", nbins=20, title="Distribución del tiempo de conversión")
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("Faltan las columnas de fechas.")

        st.subheader("4. Canales de origen más rentables")
        if "Canal" in df.columns and "Precio Venta" in df.columns:
            ingresos = df.groupby("Canal")["Precio Venta"].sum().reset_index()
            fig4 = px.bar(ingresos, x="Canal", y="Precio Venta", title="Ingresos por canal de origen")
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.warning("Faltan las columnas 'Canal' y/o 'Precio Venta'.")

        st.subheader("5. Retención y recompra")
        if "ID_Cliente" in df.columns:
            df_ret = df.groupby("ID_Cliente").size().reset_index(name="Cantidad de compras")
            fig5 = px.histogram(df_ret, x="Cantidad de compras", nbins=10, title="Frecuencia de recompra")
            st.plotly_chart(fig5, use_container_width=True)
        else:
            st.warning("Falta la columna 'ID_Cliente'.")

    except FileNotFoundError:
        st.error(f"No se encontró el archivo {archivo}. Asegúrate de subirlo.")
