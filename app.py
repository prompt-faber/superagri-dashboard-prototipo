import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Superagri Dashboard", layout="wide")

st.title("🚜 Superagri - Dashboard Inteligente")
st.success("✅ Protótipo funcionando! Desenvolvido por Carlos Eduardo Moreno (Prompt Faber)")

st.markdown("**Integração simulada com Bling + Tray**")

st.info("Se você está vendo esta mensagem, o app está rodando perfeitamente.")

st.caption(f"Deploy realizado em {datetime.now().strftime('%d/%m/%Y %H:%M')}")
