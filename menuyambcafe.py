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

# --- CSS Dinámico (Media Queries para Temas) ---
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

    /* Estilos Base Comunes */
    html, body, [class*='st-'] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Tema Dinámico: AUTO DETECCIÓN */
    @media (prefers-color-scheme: light) {
        .stApp { background-color: #ffffff !important; }
        p, label, span, div, input, .stMarkdown { color: #1e1e1e !important; }
        .product-card { background: white; border: 1px solid #eee; }
        .admin-box { background: #fdfdfd; border: 1px solid #eee; }
    }

    @media (prefers-color-scheme: dark) {
        .stApp { background-color: #0e1117 !important; }
        p, label, span, div, input, .stMarkdown { color: #ffffff !important; }
        .product-card { background: #1e1e1e; border: 1px solid #333; }
        .admin-box { background: #1e1e1e; border: 1px solid #444; }
    }

    .category-title {
        background: linear-gradient(135deg, #e63946 0%, #b91d1d 100%);
        color: white !important;
        padding: 15px; border-radius: 15px; text-align: center; margin: 25px 0;
        font-weight: 800; font-size: 1.6rem; text-transform: uppercase;
    }

    .product-card {
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center; margin-bottom: 30px; overflow: hidden;
    }

    .product-img { width: 100%; height: 220px; object-fit: cover; }
    .product-price { color: #e63946 !important; font-weight: 800; font-size: 1.4rem; }

    .whatsapp-float {
        position: fixed; width: 65px; height: 65px; bottom: 30px; right: 30px;
        background: #25d366; color: white !important; border-radius: 50px;
        display: flex; justify-content: center; align-items: center; font-size: 32px; z-index: 9999;
    }
</style>""", unsafe_allow_html=True)

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

if 'auth_role' not in st.session_state: st.session_state.auth_role = None

whatsapp_link = f"https://wa.me/{whatsapp_number}"
st.markdown(f"""<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'><a href='{whatsapp_link}' class='whatsapp-float' target='_blank'><i class='fab fa-whatsapp'></i></a>""", unsafe_allow_html=True)

c_t1, c_t2 = st.columns([10, 1])
with c_t2:
    if st.session_state.auth_role is None:
        if st.button("🔐"): st.session_state.auth_role = "login"; st.rerun()
    else:
        if st.button("📋"): st.session_state.auth_role = None; st.rerun()

@st.dialog("📝 Finalizar Orden")
def checkout_modal(carrito, mesa):
    st.markdown("### Datos del Cliente")
    with st.form("form_final"):
        nombre = st.text_input("Nombre Completo")
        cedula = st.text_input("Cédula / ID")
        if st.form_submit_button("ENVIAR PEDIDO AHORA", use_container_width=True):
            if nombre and cedula:
                for cat in ["Comida", "Bebida"]:
                    items = [f"{n} x{v[0]}" for n,v in carrito.items() if v[2] == cat]
                    if items:
                        subtotal = sum(v[0]*v[1] for n,v in carrito.items() if v[2] == cat)
                        pd.DataFrame([{"Fecha": datetime.now().strftime("%H:%M"), "Mesa": mesa, "Cliente": nombre, "Pedido": ", ".join(items), "Total": subtotal, "Categoria": cat}]).to_csv(file, mode="a", header=False, index=False)
                st.success("¡Pedido enviado!"); st.balloons(); st.rerun()

if st.session_state.auth_role is None:
    b64_logo = get_image_base64(logo_path)
    if b64_logo: st.markdown(f"<center><img src='data:image/png;base64,{b64_logo}' width='220'></center>", unsafe_allow_html=True)
    mesa = st.text_input("📍 Mesa", "1")
    carrito = {}
    st.markdown("<div class='category-title'>🍔 COMIDA</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    items_c = [("Hamburguer + papas", 350, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600", "c1"), ("Hot Dog Especial", 250, "https://images.unsplash.com/photo-1541214113241-21578d2d9b62?w=600", "c2")]
    for col, (name, price, img, k) in zip([col1, col2], items_c):
        with col:
            st.markdown(f"<div class='product-card'><img src='{img}' class='product-img'><div style='padding:15px'><p><b>{name}</b></p><p class='product-price'>${price}</p></div></div>", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 10, key=k)
            if qty > 0: carrito[name] = [qty, price, "Comida"]
    if carrito:
        total = sum(v[0]*v[1] for v in carrito.values())
        if st.button(f"🛒 FINALIZAR - RD${total}", use_container_width=True): checkout_modal(carrito, mesa)
    st.markdown("""<div style='text-align: center; padding: 40px; border-top: 1px solid #eee; margin-top: 50px;'><h3>☕ Yamb Café</h3><p>Compra con propósito • Apoya el talento</p></div>""", unsafe_allow_html=True)

elif st.session_state.auth_role == "login":
    st.markdown("<br><div class='admin-box'>", unsafe_allow_html=True)
    st.subheader("🔒 Acceso Personal")
    rol_sel = st.selectbox("Rol", ["Comida", "Bebida", "Administrador General"])
    pin = st.text_input("PIN", type="password")
    if st.button("Entrar", use_container_width=True):
        if pin == ROLES_CONFIG.get(rol_sel): st.session_state.auth_role = rol_sel; st.rerun()
        else: st.error("PIN incorrecto")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.title(f"📊 Panel: {st.session_state.auth_role}")
    df_adm = pd.read_csv(file) if os.path.exists(file) else pd.DataFrame(columns=columns)
    st.dataframe(df_adm, use_container_width=True)