import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Superagri Dashboard", layout="wide", initial_sidebar_state="expanded")

# Logo Superagri no topo
st.image("superagri-logo.png", width=320)

st.markdown('<h1 style="color: #00A651; text-align: center; font-size: 2.8rem;">Dashboard de Vendas Geral</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.3rem;">Bling + Tray | Protótipo Prompt Faber Studio</p>', unsafe_allow_html=True)
st.markdown("---")

# Upload de CSV
st.sidebar.header("📤 Dados Reais do Bling")
uploaded_file = st.sidebar.file_uploader("Carregue seu CSV de estoque/vendas", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ CSV carregado com sucesso!")
else:
    # Dados simulados (parecidos com o exemplo do Excel)
    data = {
        "produto": ["Pulverizador Elétrico 20L", "Kit Mangueira 50m", "Bomba Submersa 12V", "Inoculante 5L", "Lavadora 2000 PSI"],
        "categoria": ["Pulverizadores", "Kits", "Bombas", "Inoculantes", "Lavadoras"],
        "estoque_atual": [87, 203, 56, 34, 19],
        "estoque_minimo": [30, 60, 20, 15, 10],
        "vendas_30dias": [45, 67, 29, 52, 14],
        "preco": [289.90, 89.90, 179.90, 249.90, 399.90]
    }
    df = pd.DataFrame(data)

# Filtros
st.sidebar.header("🔎 Filtros")
categorias = st.sidebar.multiselect("Categoria", options=df["categoria"].unique(), default=df["categoria"].unique())
df_filtrado = df[df["categoria"].isin(categorias)]

# KPIs grandes - estilo Excel
col1, col2, col3, col4 = st.columns(4)

col1.metric("**Vendas Realizadas**", "348", "↑ 28 vs meta")
col2.metric("**Valor Total Vendido**", "R$ 1.248.760", "↑ R$ 148k")
col3.metric("**Ticket Médio**", "R$ 248", "↑ R$ 28")
col4.metric("**Taxa de Conversão**", "34,8%", "↑ 6,8%")

st.markdown("---")

# Abas principais
tab1, tab2, tab3, tab4 = st.tabs(["📈 Vendas x Meta", "🏆 Top Produtos", "🚨 Alertas", "📊 Visão Geral"])

with tab1:
    st.subheader("Evolução de Vendas vs Meta")
    meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
    df_vendas = pd.DataFrame({
        "Mês": meses,
        "Vendas": [18,22,31,28,45,52,48,61,55,67,72,81],
        "Meta": [25,30,35,40,45,50,55,60,65,70,75,80]
    })
    fig = px.line(df_vendas, x="Mês", y=["Vendas", "Meta"], markers=True)
    fig.update_traces(line_color="#00A651", name="Vendas", line_width=4)
    fig.update_traces(line_color="#FFC107", name="Meta", line_dash="dash", line_width=4)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Top 5 Produtos Mais Vendidos")
    fig_pie = px.pie(df_filtrado, names="produto", values="vendas_30dias", title="Participação no Faturamento")
    st.plotly_chart(fig_pie, use_container_width=True)

with tab3:
    st.subheader("🚨 Alertas de Reposição Urgente")
    alertas = df_filtrado[df_filtrado["estoque_atual"] < df_filtrado["estoque_minimo"]].copy()
    alertas["Qtd. a comprar"] = alertas["estoque_minimo"] - alertas["estoque_atual"] + 25
    st.dataframe(alertas[["produto", "estoque_atual", "estoque_minimo", "Qtd. a comprar"]], use_container_width=True)

with tab4:
    st.subheader("Visão Geral de Estoque")
    fig_bar = px.bar(df_filtrado, x="produto", y="estoque_atual", color="categoria", title="Nível de Estoque Atual")
    st.plotly_chart(fig_bar, use_container_width=True)

st.caption(f"Dashboard gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} | Pronto para integração com Bling + Tray")
