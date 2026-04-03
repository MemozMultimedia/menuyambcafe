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

# --- Estilos CSS Profesionales con Fix de Visibilidad ---
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

    /* Fondo Blanco y Texto Negro General */
    .stApp { background-color: #ffffff !important; }
    html, body, [class*='st-'], p, label, span, div, input { 
        font-family: 'Inter', sans-serif !important; 
        color: #000000 !important; 
    }

    /* FORZAR VISIBILIDAD EN SELECTBOX */
    div[data-baseweb="select"] { 
        background-color: white !important; 
        border: 1px solid #cccccc !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="select"] * { 
        color: black !important;
        background-color: white !important;
    }

    /* Eliminar espacios superiores */
    .block-container { padding-top: 1rem !important; }
    [data-testid="stSidebar"] { display: none; }

    /* Títulos de Categoría */
    .category-title {
        background: #e63946;
        color: white !important;
        padding: 12px; border-radius: 10px; text-align: center; margin: 25px 0;
        font-weight: 800; font-size: 1.4rem; text-transform: uppercase;
    }

    /* Cards de Productos */
    .product-card { 
        background: white; border-radius: 15px; border: 1px solid #f0f0f0; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px; overflow: hidden; 
    }
    .product-img { width: 100%; height: 180px; object-fit: cover; }
    .product-price { color: #e63946 !important; font-weight: 800; font-size: 1.2rem; }

    /* Login Admin Profesional */
    .admin-box {
        max-width: 400px; margin: 0 auto; padding: 30px; 
        border: 1px solid #eee; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }

    /* Footer Premium */
    .footer-premium { 
        background: #f9f9f9; padding: 50px 20px; text-align: center; 
        border-top: 1px solid #eee; margin-top: 50px; border-radius: 30px 30px 0 0;
    }
    .footer-brand { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 800; }
    .footer-tagline { font-size: 0.85rem; font-weight: 700; text-transform: uppercase; color: #e63946 !important; letter-spacing: 1px; }

    /* WhatsApp */
    .whatsapp-float { 
        position: fixed; width: 60px; height: 60px; bottom: 30px; right: 30px; 
        background: #25d366; color: white !important; border-radius: 50px; 
        display: flex; justify-content: center; align-items: center; font-size: 30px; z-index: 9999; 
    }
</style>""", unsafe_allow_html=True)

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

if 'auth_role' not in st.session_state: st.session_state.auth_role = None

# WhatsApp Icon
whatsapp_link = f"https://wa.me/{whatsapp_number}"
st.markdown(f"""<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'><a href='{whatsapp_link}' class='whatsapp-float' target='_blank'><i class='fab fa-whatsapp'></i></a>""", unsafe_allow_html=True)

# Botón Toggle Admin
c_t1, c_t2 = st.columns([12, 1])
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
    # VISTA CARTA
    b64_logo = get_image_base64(logo_path)
    if b64_logo: st.markdown(f"<center><img src='data:image/png;base64,{b64_logo}' width='180'></center>", unsafe_allow_html=True)

    mesa = st.text_input("📍 Mesa", "1")
    carrito = {}

    st.markdown("<div class='category-title'>🍔 COMIDA</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    items_c = [("Hamburguer + papas", 350, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600", "c1"), ("Hot Dog Especial", 250, "https://images.unsplash.com/photo-1541214113241-21578d2d9b62?w=600", "c2")]
    for col, (name, price, img, k) in zip([col1, col2], items_c):
        with col:
            st.markdown(f"<div class='product-card'><img src='{img}' class='product-img'><div style='padding:10px'><p><b>{name}</b></p><p class='product-price'>${price}</p></div></div>", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 10, key=k)
            if qty > 0: carrito[name] = [qty, price, "Comida"]

    st.markdown("<div class='category-title'>🍹 BEBIDAS</div>", unsafe_allow_html=True)
    bcol1, bcol2 = st.columns(2)
    items_b = [("Cuba Libre", 150, "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=600", "b1"), ("Cerveza Fria", 150, "https://images.unsplash.com/photo-1618885472179-5e474019f2a9?w=600", "b2")]
    for col, (name, price, img, k) in zip([bcol1, bcol2], items_b):
        with col:
            st.markdown(f"<div class='product-card'><img src='{img}' class='product-img'><div style='padding:10px'><p><b>{name}</b></p><p class='product-price'>${price}</p></div></div>", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 10, key=k)
            if qty > 0: carrito[name] = [qty, price, "Bebida"]

    if carrito:
        total = sum(v[0]*v[1] for v in carrito.values())
        if st.button(f"🛒 FINALIZAR - ${total}", use_container_width=True): checkout_modal(carrito, mesa)

    st.markdown("""<div class='footer-premium'><div class='footer-brand'>☕ Yamb Café</div><div style='margin:15px 0'>Cada producto apoya a jóvenes talentos en la música y el arte.</div><div class='footer-tagline'>Compra con propósito • Apoya el talento</div></div>""", unsafe_allow_html=True)

elif st.session_state.auth_role == "login":
    # LOGIN ADMIN
    st.markdown("<br><br>", unsafe_allow_html=True)
    # Aquí aplicamos la clase admin-box envolviendo el contenido
    with st.container():
        st.markdown("<div class='admin-box'>", unsafe_allow_html=True)
        st.subheader("🔒 Acceso Personal")
    rol_sel = st.selectbox("Seleccione su Rol", ["Comida", "Bebida", "Administrador General"])
    pin = st.text_input("Ingrese su PIN", type="password")
    if st.button("Entrar", use_container_width=True):
        if pin == ROLES_CONFIG.get(rol_sel): st.session_state.auth_role = rol_sel; st.rerun()
        else: st.error("PIN incorrecto")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # PANEL ADMIN
    st.title(f"📊 Panel: {st.session_state.auth_role}")
    df_adm = pd.read_csv(file) if os.path.exists(file) else pd.DataFrame(columns=columns)
    if st.session_state.auth_role == "Administrador General":
        t1, t2 = st.tabs(["💰 Ventas", "📋 Pedidos"])
        with t1: st.metric("Total", f"RD${df_adm['Total'].sum()}")
        with t2: st.dataframe(df_adm, use_container_width=True)
    else:
        st.dataframe(df_adm[df_adm['Categoria'] == st.session_state.auth_role], use_container_width=True)