import numpy as np
import pandas as pd
import streamlit as st

st.title("Meu App Streamlit")

linhas = st.slider("Quantidade de linhas", 10, 200, 50)

df = pd.DataFrame(np.random.randn(linhas, 3), columns=["A", "B", "C"])

st.subheader("Dados")
st.dataframe(df, width="stretch")

st.subheader("Gráfico")
st.line_chart(df)

st.subheader("Estatísticas")
st.dataframe(df.describe(), width="stretch")
