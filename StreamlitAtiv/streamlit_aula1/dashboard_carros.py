import streamlit as st
import pandas as pd

st.set_page_config(page_title="Concessionária", page_icon="🚗", layout="wide")

CATALOGO = {
    "Fiat Mobi 1.0": {"categoria": "Hatch", "preco": 69900.00},
    "Chevrolet Onix 1.0": {"categoria": "Hatch", "preco": 89900.00},
    "Volkswagen Polo 1.0 TSI": {"categoria": "Hatch", "preco": 112900.00},
    "Hyundai HB20S 1.0": {"categoria": "Sedã", "preco": 98900.00},
    "Toyota Corolla 2.0": {"categoria": "Sedã", "preco": 164900.00},
    "Jeep Renegade 1.3 Turbo": {"categoria": "SUV", "preco": 149900.00},
    "Toyota Hilux 2.8 Diesel": {"categoria": "Picape", "preco": 289900.00},
    "Fiat Toro 1.3 Turbo": {"categoria": "Picape", "preco": 169900.00},
}

CORES = ["Branco", "Preto", "Prata", "Cinza", "Vermelho", "Azul"]
FORMAS_PAGAMENTO = ["À vista", "Financiado"]
TAXA_JUROS_MES = 0.015

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []


def formata_reais(valor: float) -> str:
    """Formata no padrão brasileiro: R$ 1.234,56"""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


st.title("🚗 Dashboard de Vendas - Concessionária")
st.markdown("---")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Seleção de Veículos")

    with st.form("form_carro", clear_on_submit=False):
        carro_nome = st.selectbox("Escolha o Veículo", list(CATALOGO.keys()))
        categoria = CATALOGO[carro_nome]["categoria"]
        preco_base = CATALOGO[carro_nome]["preco"]
        st.caption(f"Categoria: **{categoria}** | Preço de tabela: **{formata_reais(preco_base)}**")

        cor = st.selectbox("Cor", CORES)
        quantidade = st.number_input("Quantidade", min_value=1, value=1, step=1)
        desconto = st.slider("Desconto (%)", min_value=0, max_value=10, value=0)

        btn_adicionar = st.form_submit_button("Adicionar ao Pedido", use_container_width=True)

        if btn_adicionar:
            preco_final = preco_base * (1 - desconto / 100)
            st.session_state.carrinho.append({
                "Veículo": carro_nome,
                "Categoria": categoria,
                "Cor": cor,
                "Preço Tabela (R$)": preco_base,
                "Desconto (%)": desconto,
                "Qtd": quantidade,
                "Subtotal (R$)": preco_final * quantidade,
            })
            st.success(f"**{carro_nome}** ({cor}) adicionado ao pedido!")

    st.subheader("Pedido Atual")
    if st.session_state.carrinho:
        df_pedido = pd.DataFrame(st.session_state.carrinho)

        st.dataframe(
            df_pedido,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Preço Tabela (R$)": st.column_config.NumberColumn("Preço Tabela", format="R$ %.2f"),
                "Desconto (%)": st.column_config.NumberColumn("Desconto", format="%d%%"),
                "Subtotal (R$)": st.column_config.NumberColumn("Subtotal", format="R$ %.2f"),
            },
        )

        if st.button("Limpar Pedido", use_container_width=True):
            st.session_state.carrinho = []
            st.rerun()
    else:
        st.info("O pedido está vazio. Adicione veículos acima.")


with col2:
    st.subheader("Pagamento e Fechamento")

    total_venda = sum(item["Subtotal (R$)"] for item in st.session_state.carrinho)
    qtd_veiculos = sum(item["Qtd"] for item in st.session_state.carrinho)

    m1, m2 = st.columns(2)
    m1.metric(label="VEÍCULOS NO PEDIDO", value=qtd_veiculos)
    m2.metric(label="TOTAL DA VENDA", value=formata_reais(total_venda))

    st.markdown("---")

    forma = st.selectbox("Forma de Pagamento", FORMAS_PAGAMENTO)

    if total_venda == 0:
        st.warning("Adicione veículos ao pedido antes de prosseguir com o pagamento.")

    elif forma == "À vista":
        valor_recebido = st.number_input(
            "Valor Pago pelo Cliente (R$)",
            min_value=0.0,
            value=0.0,
            step=1000.0,
            format="%.2f",
        )

        if valor_recebido == 0:
            st.info("Aguardando o pagamento...")
        elif valor_recebido < total_venda:
            falta = total_venda - valor_recebido
            st.error(f"**Valor insuficiente!** Faltam **{formata_reais(falta)}** para concluir a venda.")
        else:
            troco = valor_recebido - total_venda
            st.success("**Pagamento Concluído!**")
            st.metric(label="TROCO A DEVOLVER", value=formata_reais(troco))

            with st.expander("Ver Comprovante da Venda"):
                st.write(f"**Veículos:** {qtd_veiculos}")
                st.write(f"**Forma de pagamento:** À vista")
                st.write(f"**Total:** {formata_reais(total_venda)}")
                st.write(f"**Valor pago:** {formata_reais(valor_recebido)}")
                st.write(f"**Troco:** {formata_reais(troco)}")

            if st.button("Finalizar Venda e Novo Cliente", type="primary", use_container_width=True):
                st.session_state.carrinho = []
                st.rerun()

    else: 
        entrada_minima = total_venda * 0.20
        st.caption(f"Entrada mínima (20%): **{formata_reais(entrada_minima)}**")

        entrada = st.number_input(
            "Valor da Entrada (R$)",
            min_value=0.0,
            value=0.0,
            step=1000.0,
            format="%.2f",
        )
        parcelas = st.selectbox("Número de Parcelas", [12, 24, 36, 48, 60], index=2)

        if entrada == 0:
            st.info("Aguardando o valor da entrada...")
        elif entrada < entrada_minima:
            falta = entrada_minima - entrada
            st.error(f"**Entrada insuficiente!** Faltam **{formata_reais(falta)}** para atingir os 20%.")
        elif entrada >= total_venda:
            st.warning("A entrada cobre o valor total. Use a opção **À vista**.")
        else:
            saldo = total_venda - entrada
            i = TAXA_JUROS_MES
            valor_parcela = saldo * i / (1 - (1 + i) ** -parcelas)
            total_financiado = valor_parcela * parcelas

            st.success("**Financiamento Aprovado!**")
            f1, f2 = st.columns(2)
            f1.metric(label="SALDO FINANCIADO", value=formata_reais(saldo))
            f2.metric(label=f"PARCELA ({parcelas}x)", value=formata_reais(valor_parcela))

            with st.expander("Ver Comprovante da Venda"):
                st.write(f"**Veículos:** {qtd_veiculos}")
                st.write(f"**Forma de pagamento:** Financiado")
                st.write(f"**Total do pedido:** {formata_reais(total_venda)}")
                st.write(f"**Entrada:** {formata_reais(entrada)}")
                st.write(f"**Saldo financiado:** {formata_reais(saldo)}")
                st.write(f"**Parcelas:** {parcelas}x de {formata_reais(valor_parcela)}")
                st.write(f"**Taxa de juros:** {TAXA_JUROS_MES * 100:.1f}% ao mês")
                st.write(f"**Total pago ao final:** {formata_reais(entrada + total_financiado)}")

            if st.button("Finalizar Venda e Novo Cliente", type="primary", use_container_width=True):
                st.session_state.carrinho = []
                st.rerun()
