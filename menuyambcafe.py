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

# Robust CSV Check: Ensure file exists and has all required columns
if not os.path.exists(file):
    pd.DataFrame(columns=columns).to_csv(file, index=False)
else:
    try:
        df_check = pd.read_csv(file)
        # If 'Categoria' is missing (common cause of your error), recreate or fix it
        if "Categoria" not in df_check.columns:
            for col in columns:
                if col not in df_check.columns:
                    df_check[col] = "Desconocido"
            df_check.to_csv(file, index=False)
    except:
        pd.DataFrame(columns=columns).to_csv(file, index=False)

st.set_page_config(page_title="Yamb Café | Menú Digital", layout="wide", page_icon="☕")

# --- Estilos CSS Modernos ---
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

    [data-testid="stSidebar"] { display: none; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    
    html, body, [class*='st-'] { font-family: 'Inter', sans-serif; color: #1e1e1e; }
    .stApp { background-color: #ffffff; }

    .logo-container { display: flex; justify-content: center; align-items: center; width: 100%; padding-bottom: 10px; }

    .admin-toggle { position: fixed; top: 20px; right: 20px; z-index: 1000; cursor: pointer; background: white; padding: 10px; border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border: 1px solid #eee; transition: 0.3s; }
    .admin-toggle:hover { transform: scale(1.1); }

    .category-title { background: linear-gradient(135deg, #e63946 0%, #b91d1d 100%); color: white !important; padding: 15px; border-radius: 15px; text-align: center; margin: 20px 0; font-weight: 800; font-size: 1.6rem; text-transform: uppercase; }
    .product-card { background: white; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center; margin-bottom: 25px; border: 1px solid #eee; overflow: hidden; }
    .product-img { width: 100%; height: 200px; object-fit: cover; }
    .product-info { padding: 15px; }
    .product-name { color: #1e1e1e; font-weight: 700; font-size: 1.1rem; min-height: 2.5em; display: flex; align-items: center; justify-content: center; }
    .product-price { color: #e63946; font-weight: 800; font-size: 1.3rem; }

    .footer-premium { background: #fdfdfd; padding: 60px 20px; border-radius: 40px 40px 0 0; margin-top: 80px; text-align: center; border-top: 1px solid #eaeaea; }
    .footer-brand { font-family: 'Playfair Display', serif; font-size: 2.2rem; font-weight: 800; color: #1e1e1e; letter-spacing: -1px; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; gap: 15px; }
    .footer-tagline { font-size: 0.9rem; font-weight: 700; text-transform: uppercase; color: #e63946; letter-spacing: 2px; padding-top: 20px; border-top: 1px solid #eee; display: inline-block; }

    .whatsapp-float { position: fixed; width: 65px; height: 65px; bottom: 30px; right: 30px; background: #25d366; color: white !important; border-radius: 50px; text-align: center; font-size: 32px; box-shadow: 0 10px 20px rgba(0,0,0,0.2); z-index: 9999; display: flex; justify-content: center; align-items: center; text-decoration: none !important; }
</style>""", unsafe_allow_html=True)

def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

if 'admin_mode' not in st.session_state:
    st.session_state.admin_mode = False

whatsapp_link = f"https://wa.me/{whatsapp_number}?text=Hola!%20Vengo%20desde%20el%20menu%20digital."
st.markdown(f"""<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'><a href='{whatsapp_link}' class='whatsapp-float' target='_blank'><i class='fab fa-whatsapp'></i></a>""", unsafe_allow_html=True)

# Icon Toggle Button
col_t1, col_t2 = st.columns([10, 1])
with col_t2:
    if not st.session_state.admin_mode:
        if st.button("🔐"):
            st.session_state.admin_mode = True
            st.rerun()
    else:
        if st.button("📋"):
            st.session_state.admin_mode = False
            st.rerun()

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
                st.success("¡Pedido enviado! Gracias por preferirnos.")
                st.balloons()
                st.rerun()

if not st.session_state.admin_mode:
    if os.path.exists(logo_path):
        b64_logo = get_image_base64(logo_path)
        st.markdown(f"<div class='logo-container'><img src='data:image/png;base64,{b64_logo}' width='250'></div>", unsafe_allow_html=True)

    mesa = st.text_input("📍 Número de Mesa", "1")
    carrito = {}

    st.markdown("<div class='category-title'>🍔 COMIDA</div>", unsafe_allow_html=True)
    items_comida = [
        ("Hamburguer + papas fritas", 350, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500", "c1"),
        ("Hot Dog", 200, "https://images.unsplash.com/photo-1541214113241-21578d2d9b62?w=500", "c2"),
        ("Hot Dog + papas fritas", 250, "https://images.unsplash.com/photo-1612392062631-94dd858cba88?w=500", "c3")
    ]
    cols_c = st.columns(2)
    for i, (name, price, img, k) in enumerate(items_comida):
        with cols_c[i % 2]:
            st.markdown(f"<div class='product-card'><img src='{img}' class='product-img'><div class='product-info'><p class='product-name'>{name}</p><p class='product-price'>${price}</p></div></div>", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 20, key=k)
            if qty > 0: carrito[name] = [qty, price, "Comida"]

    st.markdown("<div class='category-title'>🍹 BEBIDAS</div>", unsafe_allow_html=True)
    items_bebida = [
        ("Cuba Libre (ron con Coca Cola)", 150, "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=500", "b1"),
        ("Vodka con jugo de naranja", 150, "https://images.unsplash.com/photo-1536935338788-846bb9981813?w=500", "b2"),
        ("Cerveza Presidente pequeña", 150, "https://images.unsplash.com/photo-1618885472179-5e474019f2a9?w=500", "b3"),
        ("Cerveza One", 100, "https://images.unsplash.com/photo-1584225064785-c62a8b43d148?w=500", "b4"),
        ("Refresco", 60, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500", "b6")
    ]
    cols_b = st.columns(2)
    for i, (name, price, img, k) in enumerate(items_bebida):
        with cols_b[i % 2]:
            st.markdown(f"<div class='product-card'><img src='{img}' class='product-img'><div class='product-info'><p class='product-name'>{name}</p><p class='product-price'>${price}</p></div></div>", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 20, key=k)
            if qty > 0: carrito[name] = [qty, price, "Bebida"]

    if carrito:
        total = sum(v[0]*v[1] for v in carrito.values())
        if st.button(f"🛒 VER RESUMEN - ${total}", use_container_width=True): checkout_modal(carrito, mesa)

    st.markdown("""<div class='footer-premium'>
        <div class='footer-brand'><span>☕</span> Yamb Café</div>
        <div class='footer-text'>Cada producto de <b>YAMB</b> apoya a jóvenes talentos en la música y el arte.</div>
        <div class='footer-tagline'>Compra con propósito • Apoya el talento</div>
    </div>""", unsafe_allow_html=True)
else:
    st.title("🔒 Panel de Administración")
    tab_comida, tab_bebida = st.tabs(["🍔 Comida", "🍹 Bebida"])
    if os.path.exists(file):
        df_admin = pd.read_csv(file)
        if not df_admin.empty and "Categoria" in df_admin.columns:
            with tab_comida:
                st.subheader("Pedidos de Comida")
                st.dataframe(df_admin[df_admin['Categoria'] == 'Comida'], use_container_width=True)
            with tab_bebida:
                st.subheader("Pedidos de Bebida")
                st.dataframe(df_admin[df_admin['Categoria'] == 'Bebida'], use_container_width=True)
        else:
            st.info("No hay pedidos registrados con categorías válidas todavía.")