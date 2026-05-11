import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Superagri Dashboard", layout="wide", initial_sidebar_state="expanded")

st.title("🚜 Superagri - Dashboard Inteligente de Estoque e Vendas")
st.markdown("**Protótipo desenvolvido por Carlos Eduardo Moreno** | Prompt Faber®")

# Dados simulados (realmente conectaria com Bling + Tray via API)
data = {
    "produto": ["Pulverizador Elétrico 20L", "Pulverizador Manual 10L", "Bomba Submersa 12V 100PSI", "Kit Mangueira + Conexões 50m", "Inoculante Líquido 5L", "Lavadora Elétrica 2000 PSI", "Pulverizador Costal 16L", "Bomba Manual 8L"],
    "sku": ["PULV-20L", "PULV-10M", "BOMBA-12V", "KIT-50M", "INOC-5L", "LAV-2000", "PULV-16C", "BOMBA-8M"],
    "estoque_atual": [87, 124, 56, 203, 34, 19, 92, 145],
    "estoque_minimo": [30, 40, 20, 60, 15, 10, 35, 50],
    "vendas_ultimos_30dias": [45, 38, 29, 67, 52, 14, 31, 22],
    "preco_unitario": [289.90, 149.90, 179.90, 89.90, 249.90, 399.90, 219.90, 69.90],
    "categoria": ["Pulverizadores", "Pulverizadores", "Bombas", "Kits", "Inoculantes", "Lavadoras", "Pulverizadores", "Bombas"]
}
df = pd.DataFrame(data)

# Sidebar
st.sidebar.header("Filtros")
categoria = st.sidebar.multiselect("Categoria", options=df["categoria"].unique(), default=df["categoria"].unique())
df_filtrado = df[df["categoria"].isin(categoria)]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Itens em Estoque", len(df_filtrado))
col2.metric("Valor Total em Estoque", f"R$ {(df_filtrado['estoque_atual'] * df_filtrado['preco_unitario']).sum():,.0f}")
col3.metric("🚨 Alertas de Reposição", len(df_filtrado[df_filtrado["estoque_atual"] < df_filtrado["estoque_minimo"]]))
col4.metric("Ticket Médio (30 dias)", "R$ 218,40")

# Abas completas
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "🚨 Alertas", "📈 Previsão", "🔥 Upsell"])

with tab1:
    st.subheader("Estoque Atual por Produto")
    fig = px.bar(df_filtrado, x="produto", y="estoque_atual", color="categoria", title="Nível de Estoque Atual")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Vendas Últimos 30 dias")
    fig2 = px.bar(df_filtrado, x="produto", y="vendas_ultimos_30dias", color="categoria")
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("🚨 Produtos que precisam de reposição urgente")
    alertas = df_filtrado[df_filtrado["estoque_atual"] < df_filtrado["estoque_minimo"]].copy()
    alertas["quantidade_a_comprar"] = alertas["estoque_minimo"] - alertas["estoque_atual"] + 20
    st.dataframe(alertas[["produto", "estoque_atual", "estoque_minimo", "quantidade_a_comprar"]], use_container_width=True)

with tab3:
    st.subheader("📈 Previsão de Demanda (próximos 30 dias)")
    df_filtrado = df_filtrado.copy()
    df_filtrado["previsao_30dias"] = (df_filtrado["vendas_ultimos_30dias"] * 1.15).astype(int)
    fig3 = px.bar(df_filtrado, x="produto", y=["vendas_ultimos_30dias", "previsao_30dias"], barmode="group", title="Vendas passadas × Previsão")
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    st.subheader("🔥 Recomendações de Upsell / Kits")
    st.success("Pulverizador Elétrico 20L + Kit Mangueira 50m (68% das vendas juntas)")
    st.success("Bomba 12V + Inoculante 5L (combo ideal para lavoura pequena)")
    st.success("Lavadora 2000 PSI + Pulverizador Costal (pacote completo)")

st.caption(f"Protótipo gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} | Pronto para integração real com API do Bling + Tray")
