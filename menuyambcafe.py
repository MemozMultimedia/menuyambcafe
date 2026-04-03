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
    
    html, body, [class*='st-'], .stMarkdown, p, label, .stTextInput label, .stNumberInput label, .stSelectbox label { 
        font-family: 'Inter', sans-serif; 
        color: #1e1e1e !important; 
    }

    .stApp { background-color: #ffffff; }
    [data-testid="stSidebar"] { display: none; }
    .block-container { padding-top: 1.5rem; padding-bottom: 0rem; }

    .logo-container { display: flex; justify-content: center; align-items: center; width: 100%; padding-bottom: 20px; }
    
    .category-title {
        background: linear-gradient(135deg, #e63946 0%, #b91d1d 100%);
        color: white !important;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        margin: 25px 0;
        font-weight: 800;
        font-size: 1.6rem;
        text-transform: uppercase;
    }

    .product-card {
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.07);
        text-align: center;
        margin-bottom: 30px;
        border: 1px solid #f0f0f0;
        overflow: hidden;
    }

    .product-img { width: 100%; height: 220px; object-fit: cover; }
    .product-info { padding: 15px; }
    .product-name { color: #1e1e1e !important; font-weight: 700; font-size: 1.2rem; min-height: 2.5em; display: flex; align-items: center; justify-content: center; }
    .product-price { color: #e63946 !important; font-weight: 800; font-size: 1.4rem; }

    .footer-premium { 
        background: #f9f9f9; 
        padding: 60px 20px; 
        border-radius: 40px 40px 0 0; 
        margin-top: 80px; 
        text-align: center; 
        border-top: 1px solid #eee; 
    }
    .footer-brand { font-family: 'Playfair Display', serif; font-size: 2.2rem; font-weight: 800; color: #1e1e1e !important; margin-bottom: 15px; }
    .footer-text { color: #444 !important; font-size: 1.1rem; }
    .footer-tagline { font-size: 0.9rem; font-weight: 700; text-transform: uppercase; color: #e63946; letter-spacing: 2px; padding-top: 20px; border-top: 1px solid #eee; display: inline-block; }

    .whatsapp-float { 
        position: fixed; width: 65px; height: 65px; bottom: 30px; right: 30px;
        background: #25d366; color: white !important; border-radius: 50px;
        display: flex; justify-content: center; align-items: center;
        font-size: 32px; box-shadow: 0 10px 20px rgba(0,0,0,0.2); z-index: 9999;
        text-decoration: none !important;
    }
</style>""", unsafe_allow_html=True)

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

if 'auth_role' not in st.session_state: st.session_state.auth_role = None

whatsapp_link = f"https://wa.me/{whatsapp_number}?text=Hola!%20Vengo%20desde%20el%20menu%20digital."
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
    if b64_logo: st.markdown(f"<div class='logo-container'><img src='data:image/png;base64,{b64_logo}' width='250'></div>", unsafe_allow_html=True)
    
    mesa = st.text_input("📍 Número de Mesa", "1")
    carrito = {}

    st.markdown("<div class='category-title'>🍔 COMIDA</div>", unsafe_allow_html=True)
    c_col1, c_col2 = st.columns(2)
    items_c = [("Hamburguer + papas", 350, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600", "c1"), ("Hot Dog Especial", 250, "https://images.unsplash.com/photo-1541214113241-21578d2d9b62?w=600", "c2")]
    for col, (name, price, img, k) in zip([c_col1, c_col2], items_c):
        with col:
            st.markdown(f"<div class='product-card'><img src='{img}' class='product-img'><div class='product-info'><p class='product-name'>{name}</p><p class='product-price'>${price}</p></div></div>", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 10, key=k)
            if qty > 0: carrito[name] = [qty, price, "Comida"]

    st.markdown("<div class='category-title'>🍹 BEBIDAS</div>", unsafe_allow_html=True)
    b_col1, b_col2 = st.columns(2)
    items_b = [("Cuba Libre", 150, "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=600", "b1"), ("Cerveza Fria", 150, "https://images.unsplash.com/photo-1618885472179-5e474019f2a9?w=600", "b2")]
    for col, (name, price, img, k) in zip([b_col1, b_col2], items_b):
        with col:
            st.markdown(f"<div class='product-card'><img src='{img}' class='product-img'><div class='product-info'><p class='product-name'>{name}</p><p class='product-price'>${price}</p></div></div>", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 10, key=k)
            if qty > 0: carrito[name] = [qty, price, "Bebida"]
    
    if carrito:
        total = sum(v[0]*v[1] for v in carrito.values())
        if st.button(f"🛒 VER RESUMEN - ${total}", use_container_width=True): checkout_modal(carrito, mesa)

    st.markdown("""<div class='footer-premium'>
        <div class='footer-brand'><span>☕</span> Yamb Café</div>
        <div class='footer-text'>Cada producto de <b>YAMB</b> apoya a jóvenes talentos en la música y el arte.</div>
        <div class='footer-tagline'>Compra con propósito • Apoya el talento</div>
    </div>""", unsafe_allow_html=True)

elif st.session_state.auth_role == "login":
    st.title("🔒 Acceso Administrativo")
    selected_role = st.selectbox("Acceder como:", ["Comida", "Bebida", "Administrador General"])
    pin = st.text_input("PIN de seguridad", type="password")
    if st.button("Ingresar"):
        if pin == "1234":
            st.session_state.auth_role = selected_role; st.rerun()
        else: st.error("PIN inválido")

else:
    role = st.session_state.auth_role
    st.title(f"📊 Panel: {role}")
    df = pd.read_csv(file) if os.path.exists(file) else pd.DataFrame(columns=columns)
    if role == "Comida":
        st.dataframe(df[df['Categoria'] == 'Comida'], use_container_width=True)
    elif role == "Bebida":
        st.dataframe(df[df['Categoria'] == 'Bebida'], use_container_width=True)
    elif role == "Administrador General":
        t1, t2 = st.tabs(["💰 Contabilidad", "📋 Historial"])
        with t1:
            st.metric("Ventas Totales", f"RD${df['Total'].sum():,.2f}")
            if not df.empty: st.bar_chart(df.groupby('Categoria')['Total'].sum())
        with t2: st.dataframe(df, use_container_width=True)