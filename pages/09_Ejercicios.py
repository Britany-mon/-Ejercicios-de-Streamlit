import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Limpieza y Análisis", layout="wide")

st.title("Misión de Limpieza y Análisis")
st.markdown(
    "Esta app genera un conjunto de datos sintético, aplica limpieza básica y muestra un análisis descriptivo con gráficos."
)

@st.cache_data
def crear_datos(n=20):
    np.random.seed(42)
    data = {
        "Edad": np.random.randint(18, 70, size=n).astype(float),
        "Ingresos": np.random.normal(45000, 12000, size=n),
        "Gastos": np.random.normal(22000, 7000, size=n),
        "Ciudad": np.random.choice(["Madrid", "Barcelona", "Valencia", "Sevilla"], size=n),
        "Activo": np.random.choice(["Sí", "No"], size=n),
    }
    df = pd.DataFrame(data)

    indices_nulos = np.random.choice(df.index, size=4, replace=False)
    df.loc[indices_nulos, "Ingresos"] = np.nan
    df.loc[indices_nulos[:2], "Ciudad"] = np.nan
    df.loc[indices_nulos[2:], "Edad"] = np.nan

    return df


def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    df_limpio = df.copy()
    df_limpio["Edad"] = df_limpio["Edad"].fillna(df_limpio["Edad"].median())
    df_limpio["Ingresos"] = df_limpio["Ingresos"].fillna(df_limpio["Ingresos"].mean())
    df_limpio["Ciudad"] = df_limpio["Ciudad"].fillna("Desconocida")
    return df_limpio


def analizar_datos(df: pd.DataFrame) -> pd.DataFrame:
    resumen = df.describe(include="all").transpose()
    resumen["missing"] = df.isna().sum()
    return resumen


df = crear_datos(30)

st.subheader("Datos Originales")
st.dataframe(df)

if st.button("Limpiar datos"):
    df_limpio = limpiar_datos(df)
    st.subheader("Datos Limpiados")
    st.dataframe(df_limpio)

    st.markdown("---")
    st.subheader("Análisis descriptivo")
    st.dataframe(analizar_datos(df_limpio))

    st.markdown("### Promedio de Ingresos y Gastos")
    promedio_df = (
        df_limpio[["Ingresos", "Gastos"]]
        .mean()
        .reset_index()
        .rename(columns={"index": "Variable", 0: "Valor"})
        .set_index("Variable")
    )
    st.bar_chart(promedio_df)

    st.markdown("### Ingresos por Ciudad")
    st.bar_chart(df_limpio.groupby("Ciudad")["Ingresos"].mean())
else:
    st.info("Presiona el botón para limpiar los datos y ver el análisis.")
