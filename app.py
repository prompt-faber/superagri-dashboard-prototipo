import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Superagri Dashboard", layout="wide", initial_sidebar_state="expanded")

# ====================== LOGO SUPERAGRI + CORES ======================
st.image("superagri-logo.png", width=280)

st.markdown('<h1 style="color: #00A651; text-align: center; font-size: 2.8rem;">🚜 Dashboard Inteligente</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #FFC107; text-align: center; font-size: 1.4rem;">Bling + Tray | Protótipo Prompt Faber Studio</p>', unsafe_allow_html=True)
st.markdown("---")

# ====================== UPLOAD DE CSV ======================
st.sidebar.header("📤 Inserção de Dados")
uploaded_file = st.sidebar.file_uploader("Carregue seu CSV do Bling (estoque/vendas)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ CSV carregado com sucesso!")
else:
    # Dados simulados (se não subir CSV)
    data = {
        "produto": ["Pulverizador Elétrico 20L", "Pulverizador Manual 10L", "Bomba Submersa 12V", "Kit Mangueira 50m", "Inoculante 5L", "Lavadora 2000 PSI", "Pulverizador Costal 16L", "Bomba Manual 8L"],
        "categoria": ["Pulverizadores", "Pulverizadores", "Bombas", "Kits", "Inoculantes", "Lavadoras", "Pulverizadores", "Bombas"],
        "estoque_atual": [87, 124, 56, 203, 34, 19, 92, 145],
        "estoque_minimo": [30, 40, 20, 60, 15, 10, 35, 50],
        "vendas_30dias": [45, 38, 29, 67, 52, 14, 31, 22],
        "preco": [289.90, 149.90, 179.90, 89.90, 249.90, 399.90, 219.90, 69.90]
    }
    df = pd.DataFrame(data)

# ====================== FILTROS ======================
st.sidebar.header("🔎 Filtros")
categorias = st.sidebar.multiselect("Categoria", options=df["categoria"].unique(), default=df["categoria"].unique())
df_filtrado = df[df["categoria"].isin(categorias)]

# ====================== KPIs ======================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Vendas 30 dias", "348", "↑ 42")
col2.metric("Valor Total", "R$ 1.248.760", "↑ R$ 187k")
col3.metric("Ticket Médio", "R$ 248", "↑ R$ 31")
col4.metric("Conversão", "34.8%", "↑ 6.2%")

st.markdown("---")

# Abas completas (mesmo layout anterior, só mais limpo)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Visão Geral", "🚨 Alertas", "📈 Vendas x Meta", "🏆 Top Produtos", "🔥 Upsell"])

with tab1:
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("Estoque Atual")
        fig_bar = px.bar(df_filtrado, x="produto", y="estoque_atual", color="categoria")
        st.plotly_chart(fig_bar, use_container_width=True)
    with col_g2:
        st.subheader("Vendas Últimos 30 dias")
        fig_vendas = px.bar(df_filtrado, x="produto", y="vendas_30dias", color="categoria")
        st.plotly_chart(fig_vendas, use_container_width=True)

with tab2:
    st.subheader("🚨 Alertas de Reposição")
    alertas = df_filtrado[df_filtrado["estoque_atual"] < df_filtrado["estoque_minimo"]].copy()
    alertas["Qtd. a comprar"] = alertas["estoque_minimo"] - alertas["estoque_atual"] + 25
    st.dataframe(alertas, use_container_width=True)

with tab3:
    st.subheader("📈 Vendas vs Meta")
    meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
    df_vendas = pd.DataFrame({"Mês": meses, "Vendas": [18,22,31,28,45,52,48,61,55,67,72,81], "Meta": [25,30,35,40,45,50,55,60,65,70,75,80]})
    fig_linha = px.line(df_vendas, x="Mês", y=["Vendas","Meta"], markers=True)
    st.plotly_chart(fig_linha, use_container_width=True)

with tab4:
    st.subheader("🏆 Top Produtos")
    fig_pie = px.pie(df_filtrado, names="produto", values="vendas_30dias")
    st.plotly_chart(fig_pie, use_container_width=True)

with tab5:
    st.subheader("🔥 Recomendações de Upsell")
    st.success("Pulverizador Elétrico 20L + Kit Mangueira 50m → 68% das vendas juntas")
    st.success("Bomba 12V + Inoculante 5L → combo ideal")

st.caption(f"Dashboard gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} | Upload de CSV ativado")categorias = st.sidebar.multiselect("Categoria", options=df["categoria"].unique(), default=df["categoria"].unique())
df_filtrado = df[df["categoria"].isin(categorias)]

# ====================== KPIs GRANDES ======================
col1, col2, col3, col4 = st.columns(4)
col1.metric("**Vendas Realizadas (30 dias)**", "348", "↑ 42 vs meta")
col2.metric("**Valor Total Vendido**", "R$ 1.248.760", "↑ R$ 187k")
col3.metric("**Ticket Médio**", "R$ 248", "↑ R$ 31")
col4.metric("**Taxa de Conversão**", "34.8%", "↑ 6.2%")

st.markdown("---")

# ====================== ABAS (mais completo) ======================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Visão Geral", "🚨 Alertas de Estoque", "📈 Vendas x Meta", "🏆 Top Produtos", "🔥 Recomendações"])

with tab1:
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("Estoque Atual")
        fig_bar = px.bar(df_filtrado, x="produto", y="estoque_atual", color="categoria", title="Nível de Estoque por Produto")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col_g2:
        st.subheader("Vendas Últimos 30 dias")
        fig_vendas = px.bar(df_filtrado, x="produto", y="vendas_30dias", color="categoria")
        st.plotly_chart(fig_vendas, use_container_width=True)

with tab2:
    st.subheader("🚨 Produtos que precisam de reposição urgente")
    alertas = df_filtrado[df_filtrado["estoque_atual"] < df_filtrado["estoque_minimo"]].copy()
    alertas["Qtd. a comprar"] = alertas["estoque_minimo"] - alertas["estoque_atual"] + 25
    st.dataframe(alertas[["produto", "estoque_atual", "estoque_minimo", "Qtd. a comprar"]], use_container_width=True, height=400)

with tab3:
    st.subheader("📈 Evolução de Vendas vs Meta")
    meses = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
    df_vendas = pd.DataFrame({
        "Mês": meses,
        "Vendas": [18,22,31,28,45,52,48,61,55,67,72,81],
        "Meta": [25,30,35,40,45,50,55,60,65,70,75,80]
    })
    fig_linha = px.line(df_vendas, x="Mês", y=["Vendas","Meta"], markers=True, title="Vendas Mensal × Meta")
    fig_linha.update_traces(line_color="#00A651", selector=dict(name="Vendas"))
    fig_linha.update_traces(line_color="#FFC107", line_dash="dash", selector=dict(name="Meta"))
    st.plotly_chart(fig_linha, use_container_width=True)

with tab4:
    st.subheader("🏆 Top 5 Produtos Mais Vendidos")
    fig_pie = px.pie(df_filtrado, names="produto", values="vendas_30dias", title="Participação no Faturamento")
    st.plotly_chart(fig_pie, use_container_width=True)

with tab5:
    st.subheader("🔥 Recomendações de Upsell / Kits")
    st.success("Pulverizador Elétrico 20L + Kit Mangueira 50m → vendido junto em 68% das vendas")
    st.success("Bomba 12V + Inoculante 5L → combo ideal para produtores pequenos")
    st.success("Lavadora 2000 PSI + Pulverizador Costal → pacote completo para limpeza + aplicação")

st.caption(f"Dashboard gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} | Protótipo 100% funcional - Pronto para conectar com Bling + Tray")
