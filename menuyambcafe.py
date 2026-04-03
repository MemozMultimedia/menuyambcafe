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

if not os.path.exists(file):
    pd.DataFrame(columns=columns).to_csv(file, index=False)

st.set_page_config(page_title="Yamb Café | Menú Digital", layout="wide", page_icon="☕")

# --- Estilos CSS ---
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    [data-testid="stSidebar"] { display: none; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    html, body, [class*='st-'] { font-family: 'Inter', sans-serif; color: #1e1e1e; }
    .stApp { background-color: #ffffff; }
    .logo-container { display: flex; justify-content: center; align-items: center; width: 100%; padding-bottom: 10px; }
    .category-title { background: linear-gradient(135deg, #e63946 0%, #b91d1d 100%); color: white !important; padding: 15px; border-radius: 15px; text-align: center; margin: 20px 0; font-weight: 800; font-size: 1.6rem; text-transform: uppercase; }
    .product-card { background: white; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center; margin-bottom: 25px; border: 1px solid #eee; overflow: hidden; }
    .product-img { width: 100%; height: 200px; object-fit: cover; }
    .product-info { padding: 15px; }
    .product-name { color: #1e1e1e; font-weight: 700; font-size: 1.1rem; min-height: 2.5em; display: flex; align-items: center; justify-content: center; }
    .product-price { color: #e63946; font-weight: 800; font-size: 1.3rem; }
    .footer-premium { background: #fdfdfd; padding: 60px 20px; border-radius: 40px 40px 0 0; margin-top: 80px; text-align: center; border-top: 1px solid #eaeaea; }
    .whatsapp-float { position: fixed; width: 65px; height: 65px; bottom: 30px; right: 30px; background: #25d366; color: white !important; border-radius: 50px; text-align: center; font-size: 32px; box-shadow: 0 10px 20px rgba(0,0,0,0.2); z-index: 9999; display: flex; justify-content: center; align-items: center; text-decoration: none !important; }
</style>""", unsafe_allow_html=True)

def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --- Control de Roles ---
if 'auth_role' not in st.session_state:
    st.session_state.auth_role = None

whatsapp_link = f"https://wa.me/{whatsapp_number}?text=Hola!%20Vengo%20desde%20el%20menu%20digital."
st.markdown(f"""<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'><a href='{whatsapp_link}' class='whatsapp-float' target='_blank'><i class='fab fa-whatsapp'></i></a>""", unsafe_allow_html=True)

# Botón de cambio de vista (Esquina superior derecha)
col_t1, col_t2 = st.columns([10, 1])
with col_t2:
    if st.session_state.auth_role is None:
        if st.button("🔐"): st.session_state.auth_role = "login"; st.rerun()
    else:
        if st.button("📋"): st.session_state.auth_role = None; st.rerun()

if st.session_state.auth_role is None:
    # --- VISTA CLIENTE ---
    if os.path.exists(logo_path):
        b64_logo = get_image_base64(logo_path)
        st.markdown(f"<div class='logo-container'><img src='data:image/png;base64,{b64_logo}' width='250'></div>", unsafe_allow_html=True)
    
    mesa = st.text_input("📍 Mesa", "1")
    st.markdown("<div class='category-title'>🍔 COMIDA</div>", unsafe_allow_html=True)
    st.info("Selecciona tus productos...")
    # Aquí iría el resto del menú de cliente...

elif st.session_state.auth_role == "login":
    st.title("🔒 Autenticación")
    selected_role = st.selectbox("Acceder como:", ["Comida", "Bebida", "Administrador General"])
    pin = st.text_input("PIN de seguridad", type="password")
    if st.button("Ingresar"):
        if pin == "1234":
            st.session_state.auth_role = selected_role
            st.rerun()
        else:
            st.error("PIN inválido")

else:
    # --- VISTA ADMIN SEGMENTADA ---
    role = st.session_state.auth_role
    st.title(f"📊 Panel: {role}")
    df = pd.read_csv(file) if os.path.exists(file) else pd.DataFrame(columns=columns)

    if role == "Comida":
        st.subheader("Pedidos para Cocina")
        st.dataframe(df[df['Categoria'] == 'Comida'], use_container_width=True)
    
    elif role == "Bebida":
        st.subheader("Pedidos para Bar")
        st.dataframe(df[df['Categoria'] == 'Bebida'], use_container_width=True)

    elif role == "Administrador General":
        tab1, tab2 = st.tabs(["💰 Contabilidad", "📋 Historial Total"])
        with tab1:
            st.metric("Ventas Totales", f"RD${df['Total'].sum():,.2f}")
            st.bar_chart(df.groupby('Categoria')['Total'].sum())
        with tab2:
            st.dataframe(df, use_container_width=True)