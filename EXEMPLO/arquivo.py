from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Tabela 1.1.2", layout="wide")

colunas = [
    "Local",
    "Total", "Total Homem", "Total Mulher",
    "14 a 29 Total", "14 a 29 Homem", "14 a 29 Mulher",
    "30 a 49 Total", "30 a 49 Homem", "30 a 49 Mulher",
    "50 a 59 Total", "50 a 59 Homem", "50 a 59 Mulher",
    "60 ou mais Total", "60 ou mais Homem", "60 ou mais Mulher",
]


@st.cache_data
def carregar():
    df = pd.read_excel(Path(__file__).parent / "Tabela 1.1.2.xls", header=None, skiprows=7, nrows=33)
    df.columns = colunas
    df["Local"] = df["Local"].str.strip()
    return df


df = carregar()

regioes = ["Brasil", "Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste"]
estados = df[~df["Local"].isin(regioes)]

st.title("Horas semanais dedicadas a cuidados de pessoas e afazeres domésticos - 2022")

st.subheader("Tabela")
st.dataframe(df.round(1), width="stretch", hide_index=True)

st.subheader("Média por sexo nas regiões")
reg = df[df["Local"].isin(regioes)].melt(
    id_vars="Local", value_vars=["Total Homem", "Total Mulher"], var_name="Sexo", value_name="Horas"
)
reg["Sexo"] = reg["Sexo"].str.replace("Total ", "")
st.plotly_chart(px.bar(reg, x="Local", y="Horas", color="Sexo", barmode="group"), width="stretch")

st.subheader("Comparação por estado")
coluna = st.selectbox("Indicador", colunas[1:])
st.plotly_chart(
    px.bar(estados.sort_values(coluna), x=coluna, y="Local", orientation="h", height=750),
    width="stretch",
)

st.subheader("Grupos de idade")
local = st.selectbox("Local", df["Local"])
linha = df[df["Local"] == local].iloc[0]
grupos = ["14 a 29", "30 a 49", "50 a 59", "60 ou mais"]
idade = pd.DataFrame(
    [{"Grupo": g, "Sexo": s, "Horas": linha[f"{g} {s}"]} for g in grupos for s in ["Homem", "Mulher"]]
)
st.plotly_chart(px.line(idade, x="Grupo", y="Horas", color="Sexo", markers=True), width="stretch")
