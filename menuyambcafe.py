import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# --- Configuración Inicial ---
logo_path = "Vector Smart Object.png"
file = "pedidos.csv"
whatsapp_number = "1234567890"

if not os.path.exists(file):
    pd.DataFrame(columns=["Fecha", "Mesa", "Cliente", "Pedido", "Total", "Categoria"]).to_csv(file, index=False)

st.set_page_config(page_title="Yamb Café | Menú Digital", layout="wide", page_icon="☕")

# --- Estilos CSS ---
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [class*='st-'] { font-family: 'Inter', sans-serif; color: #1e1e1e; }
    .stApp { background-color: #ffffff; }
    
    /* Contenedor para centrado absoluto del logo */
    .logo-container { display: flex; justify-content: center; align-items: center; width: 100%; padding: 20px 0; }

    label, .stMarkdown p { color: #1e1e1e !important; font-weight: 600 !important; }
    .category-title { background: linear-gradient(135deg, #e63946 0%, #b91d1d 100%); color: white !important; padding: 15px; border-radius: 15px; text-align: center; margin: 30px 0 20px 0; font-weight: 800; font-size: 1.6rem; text-transform: uppercase; }
    .product-card { background: white; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center; margin-bottom: 25px; border: 1px solid #eee; overflow: hidden; }
    .product-img { width: 100%; height: 200px; object-fit: cover; }
    .product-info { padding: 15px; }
    .product-name { color: #1e1e1e; font-weight: 700; font-size: 1.1rem; min-height: 2.5em; display: flex; align-items: center; justify-content: center; }
    .product-price { color: #e63946; font-weight: 800; font-size: 1.3rem; }
    .footer-box { background: #f9f9f9; padding: 40px; border-radius: 25px; margin-top: 60px; text-align: center; border: 1px solid #eee; }
    .whatsapp-float { position: fixed; width: 65px; height: 65px; bottom: 30px; right: 30px; background: #25d366; color: white !important; border-radius: 50px; text-align: center; font-size: 32px; box-shadow: 0 10px 20px rgba(0,0,0,0.2); z-index: 9999; display: flex; justify-content: center; align-items: center; text-decoration: none !important; }
</style>""", unsafe_allow_html=True)

def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

whatsapp_link = f"https://wa.me/{whatsapp_number}?text=Hola!%20Vengo%20desde%20el%20menu%20digital."
st.markdown(f"""<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'><a href='{whatsapp_link}' class='whatsapp-float' target='_blank'><i class='fab fa-whatsapp'></i></a>""", unsafe_allow_html=True)

@st.dialog("📝 Finalizar Orden")
def checkout_modal(carrito, mesa):
    st.markdown("### Datos del Cliente")
    with st.form("form_final"):
        nombre = st.text_input("Nombre Completo")
        cedula = st.text_input("Cédula / ID")
        if st.form_submit_button("ENVIAR PEDIDO AHORA", width="stretch"):
            if nombre and cedula:
                for cat in ["Comida", "Bebida"]:
                    items = [f"{n} x{v[0]}" for n,v in carrito.items() if v[2] == cat]
                    if items:
                        subtotal = sum(v[0]*v[1] for n,v in carrito.items() if v[2] == cat)
                        pd.DataFrame([{"Fecha": datetime.now().strftime("%H:%M"), "Mesa": mesa, "Cliente": nombre, "Pedido": ", ".join(items), "Total": subtotal, "Categoria": cat}]).to_csv(file, mode="a", header=False, index=False)
                st.success("¡Gracias por elegirnos! Tu pedido llegará a tu mesa en unos minutos.")
                st.balloons()
                st.rerun()

tab_menu, tab_admin = st.tabs(["📋 CARTA DIGITAL", "🔒 PANEL ADMIN"])

with tab_menu:
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
        ("Cerveza Heineken mediana", 230, "https://images.unsplash.com/photo-1613215049641-81495014a582?w=500", "b5"),
        ("Refresco", 60, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500", "b6"),
        ("Agua", 25, "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=500", "b7")
    ]
    cols_b = st.columns(2)
    for i, (name, price, img, k) in enumerate(items_bebida):
        with cols_b[i % 2]:
            st.markdown(f"<div class='product-card'><img src='{img}' class='product-img'><div class='product-info'><p class='product-name'>{name}</p><p class='product-price'>${price}</p></div></div>", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 20, key=k)
            if qty > 0: carrito[name] = [qty, price, "Bebida"]

    if carrito:
        total = sum(v[0]*v[1] for v in carrito.values())
        if st.button(f"🛒 VER RESUMEN - ${total}", width="stretch"): checkout_modal(carrito, mesa)

    st.markdown("<div class='footer-box'><h3 style='color:#e63946'>☕ Yamb Café</h3><p>¡Gracias por elegirnos! Tu pedido llegará a tu mesa en unos minutos.</p><p style='font-size: 0.8rem; color: #888;'>© 2024 Yamb Café - Menú Digital</p></div>", unsafe_allow_html=True)

with tab_admin:
    st.title("Pedidos Recibidos")
    if os.path.exists(file): st.dataframe(pd.read_csv(file), width="stretch")