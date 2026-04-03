import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# --- Configuración Inicial ---
logo_path = "Vector Smart Object.png"
file = "pedidos.csv"
whatsapp_number = "1234567890"
columns = ["Fecha", "Mesa", "Cliente", "Pedido", "Total", "Categoria"]

ROLES_CONFIG = {
    "Comida": "1111",
    "Bebida": "2222",
    "Administrador General": "3333"
}

if not os.path.exists(file):
    pd.DataFrame(columns=columns).to_csv(file, index=False)

st.set_page_config(page_title="Yamb Café | Menú Digital", layout="wide", page_icon="☕")

# --- Estilos CSS Ultra-Visibilidad ---
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    /* FUERZA COLOR NEGRO EN TODO EL APP */
    .stApp, .stMarkdown, p, label, span, div, li, input, button, select {
        font-family: 'Inter', sans-serif !important;
        color: #000000 !important;
    }

    /* SELECTOR DE ADMINISTRADORES (SELECTBOX) */
    div[data-baseweb="select"] * {
        color: #000000 !important;
        background-color: #ffffff !important;
    }

    /* BORDE PARA EL SELECTOR */
    div[data-baseweb="select"] {
        border: 2px solid #e6e6e6 !important;
        border-radius: 10px !important;
    }

    .category-title {
        background: linear-gradient(135deg, #e63946 0%, #b91d1d 100%);
        color: white !important;
        padding: 15px; border-radius: 15px; text-align: center; margin: 25px 0; font-weight: 800; font-size: 1.6rem; text-transform: uppercase;
    }

    .product-card { background: white; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.07); text-align: center; margin-bottom: 30px; border: 1px solid #f0f0f0; overflow: hidden; }
    .product-img { width: 100%; height: 220px; object-fit: cover; }
    .product-price { color: #e63946 !important; font-weight: 800; font-size: 1.4rem; }

    .admin-container { max-width: 500px; margin: 0 auto; padding: 40px; background: #ffffff; border-radius: 20px; border: 1px solid #dddddd; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
</style>""", unsafe_allow_html=True)

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

if 'auth_role' not in st.session_state: st.session_state.auth_role = None

# Iconos de navegación
c_t1, c_t2 = st.columns([10, 1])
with c_t2:
    if st.session_state.auth_role is None:
        if st.button("🔐"): st.session_state.auth_role = "login"; st.rerun()
    else:
        if st.button("📋"): st.session_state.auth_role = None; st.rerun()

if st.session_state.auth_role is None:
    # VISTA CLIENTE
    b64_logo = get_image_base64(logo_path)
    if b64_logo: st.markdown(f"<center><img src='data:image/png;base64,{b64_logo}' width='220'></center>", unsafe_allow_html=True)
    mesa = st.text_input("📍 Número de Mesa", "1")
    st.markdown("<div class='category-title'>🍔 CARTA DIGITAL</div>", unsafe_allow_html=True)
    st.info("Selecciona tus productos del menú...")
    # (Aquí iría la lógica del carrito igual que antes)

elif st.session_state.auth_role == "login":
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='admin-container'>", unsafe_allow_html=True)
        st.subheader("Acceso para Personal")
        rol_sel = st.selectbox("Seleccione su área:", ["Comida", "Bebida", "Administrador General"])
        pin = st.text_input("Introduzca su clave:", type="password")
        if st.button("Entrar al Panel", use_container_width=True):
            if pin == ROLES_CONFIG.get(rol_sel):
                st.session_state.auth_role = rol_sel; st.rerun()
            else: st.error("Clave incorrecta")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.title(f"Área: {st.session_state.auth_role}")
    df_adm = pd.read_csv(file) if os.path.exists(file) else pd.DataFrame(columns=columns)
    st.dataframe(df_adm, use_container_width=True)