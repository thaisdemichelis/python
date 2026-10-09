import streamlit as st
import pandas as pd

itens = [
    "Pão Francês (kg)",
    "Pão de Queijo (un)",
    "Leite Integral (L)",
    "Queijo Mussarela (g)",
    "Presunto (g)",
    "Café Espresso (un)",
    "Bolo de Cenoura (fatia)"
]

precos = [
    14.90,
    2.50,
    5.80,
    12.50,
    9.80,
    6.00,
    8.50
]

df = pd.DataFrame({
    "Item": itens,
    "Preço (R$)": precos
})

st.title("Meu primeiro dash")

st.subheader("Vendas da Padaria")

st.write(df)

item_escolhido = st.selectbox("Escolha um item:", df["Item"])

preco = df.loc[df["Item"] == item_escolhido, "Preço (R$)"].values[0]
st.write(f"O preço de **{item_escolhido}** é **R$ {preco:.2f}**")