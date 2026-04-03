import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# --- Configuración Inicial ---
logo_path = "Vector Smart Object.png"
file_pedidos = "pedidos.csv"
file_menu = "menu.csv"
columns_p = ["Fecha", "Mesa", "Cliente", "Pedido", "Notas", "Total", "Categoria", "Estado"]
ROLES_CONFIG = {
    "Comida": "1111",
    "Bebida": "2222",
    "Administrador General": "3333"
}

# Robust initialization to prevent file errors
if not os.path.exists(file_pedidos):
    pd.DataFrame(columns=columns_p).to_csv(file_pedidos, index=False)

st.set_page_config(page_title="Yamb Café | Menú Digital", layout="wide", page_icon="☕")

# --- CSS for Centralization and Theme Adaptation ---
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

    html, body, [class*='st-'] { font-family: 'Inter', sans-serif !important; text-align: center; }
    .block-container { padding-top: 1rem !important; }
    header, footer { visibility: hidden; }

    /* Theme Colors */
    @media (prefers-color-scheme: light) {
        .stApp { background-color: #f8f9fa; color: #1e1e1e; }
        .product-card { background: white; }
    }
    @media (prefers-color-scheme: dark) {
        .stApp { background-color: #0e1117; color: white; }
        .product-card { background: #1e1e1e; border: 1px solid #333; }
    }
    
    /* Logo Styling */
    .logo-img { max-width: 100px; width: 30%; height: auto; margin: 0 auto; display: block; }

    .category-title {
        background: linear-gradient(135deg, #e63946 0%, #b91d1d 100%);
        color: white !important; padding: 12px; border-radius: 12px;
        font-weight: 800; font-size: 1.3rem; text-transform: uppercase; margin: 20px 0;
    }

    .product-card { 
        border-radius: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.1); 
        overflow: hidden; margin-bottom: 15px; 
    }
    .product-img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
    .product-price { color: #e63946 !important; font-weight: 800; font-size: 1.2rem; }

    /* Center inputs and buttons */
    .stTextInput, .stSelectbox, .stButton, div[data-testid='stNumberInput'] { margin: 0 auto !important; max-width: 400px; }

    .footer-premium { padding: 40px 20px; border-radius: 40px 40px 0 0; margin-top: 50px; background: rgba(0,0,0,0.05); }
</style>""", unsafe_allow_html=True)

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

if 'carrito' not in st.session_state: st.session_state.carrito = {}

# --- App Logic ---
logo_b64 = get_image_base64(logo_path)
if logo_b64:
    st.markdown(f'<img src="data:image/png;base64,{logo_b64}" class="logo-img">', unsafe_allow_html=True)

mesa_list = ["Sin Mesa"] + [str(i) for i in range(1, 21)]
mesa = st.selectbox("📍 Selecciona tu Mesa", mesa_list, help="Elige tu número de mesa o selecciona Sin Mesa")

if os.path.exists(file_menu):
    df_m = pd.read_csv(file_menu)
    for cat in ["Comida", "Bebida"]:
        st.markdown(f"<div class='category-title'>{cat}</div>", unsafe_allow_html=True)
        items = df_m[df_m['Categoria'] == cat]
        cols = st.columns(2)
        for i, row in enumerate(items.itertuples()):
            with cols[i % 2]:
                st.markdown(f"""<div class='product-card'>
                    <img src='{row.Imagen}' class='product-img'>
                    <div style='padding:10px;'>
                        <b>{row.Nombre}</b><br>
                        <span class='product-price'>RD${row.Precio}</span>
                    </div>
                </div>""", unsafe_allow_html=True)
                qty = st.number_input("Cantidad", 0, 20, key=f"q_{row.Index}", label_visibility="collapsed")
                if qty > 0: st.session_state.carrito[row.Nombre] = [qty, row.Precio, cat]

if st.session_state.carrito:
    total = sum(v[0]*v[1] for v in st.session_state.carrito.values())
    if st.button(f"🛒 CONFIRMAR PEDIDO - RD${total}", use_container_width=True):
        st.success("¡Pedido Enviado!")
        st.balloons()

st.markdown("""<div class='footer-premium'><b>Yamb Café</b><br>Apoyando el talento joven</div>""", unsafe_allow_html=True)
