import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- Configuración Inicial ---
logo_path = "Vector Smart Object.png"
file = "pedidos.csv"
whatsapp_number = "1234567890"

if not os.path.exists(file):
    pd.DataFrame(columns=["Fecha", "Mesa", "Cliente", "Pedido", "Total", "Categoria"]).to_csv(file, index=False)

st.set_page_config(page_title="Yamb Café | Menú Digital", layout="wide", page_icon="☕")

st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [class*='st-'] { font-family: 'Inter', sans-serif; color: #1e1e1e; }
    .stApp { background-color: #ffffff; }
    label, .stMarkdown p { color: #1e1e1e !important; font-weight: 600 !important; }
    .category-title { background: linear-gradient(135deg, #e63946 0%, #b91d1d 100%); color: white !important; padding: 15px; border-radius: 15px; text-align: center; margin: 30px 0 20px 0; font-weight: 800; font-size: 1.6rem; text-transform: uppercase; }
    .product-card { background: white; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center; margin-bottom: 25px; border: 1px solid #eee; overflow: hidden; }
    .product-img { width: 100%; height: 200px; object-fit: cover; }
    .product-info { padding: 15px; }
    .product-name { color: #1e1e1e; font-weight: 700; font-size: 1.2rem; }
    .product-price { color: #e63946; font-weight: 800; font-size: 1.3rem; }
    .footer-box { background: #f9f9f9; padding: 40px; border-radius: 25px; margin-top: 60px; text-align: center; border: 1px solid #eee; }
    .whatsapp-float { position: fixed; width: 65px; height: 65px; bottom: 30px; right: 30px; background: #25d366; color: white !important; border-radius: 50px; text-align: center; font-size: 32px; box-shadow: 0 10px 20px rgba(0,0,0,0.2); z-index: 9999; display: flex; justify-content: center; align-items: center; text-decoration: none !important; }
</style>""", unsafe_allow_html=True)

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
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if os.path.exists(logo_path): st.image(logo_path, width="stretch")
    mesa = st.text_input("📍 Número de Mesa", "1")
    carrito = {}
    st.markdown("<div class='category-title'>🍔 Platos & Snacks</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    items_comida = [("Burguer + Papas", 350, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400", "f1"), ("Hot Dog Especial", 250, "https://images.unsplash.com/photo-1541214113241-21578d2d9b62?w=400", "f2")]
    for col, (name, price, img, k) in zip([col1, col2], items_comida):
        with col:
            st.markdown(f"<div class='product-card'><img src='{img}' class='product-img'><div class='product-info'><p class='product-name'>{name}</p><p class='product-price'>RD${price}</p></div></div>", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 10, key=k)
            if qty > 0: carrito[name] = [qty, price, "Comida"]
    st.markdown("<div class='category-title'>☕ Bebidas & Café</div>", unsafe_allow_html=True)
    bcol1, bcol2 = st.columns(2)
    items_bebida = [("Cappuccino", 180, "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=400", "b1"), ("Cerveza Fría", 150, "https://images.unsplash.com/photo-1518173946687-a4c8892bbd9f?w=400", "b2")]
    for col, (name, price, img, k) in zip([bcol1, bcol2], items_bebida):
        with col:
            st.markdown(f"<div class='product-card'><img src='{img}' class='product-img'><div class='product-info'><p class='product-name'>{name}</p><p class='product-price'>RD${price}</p></div></div>", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 10, key=k)
            if qty > 0: carrito[name] = [qty, price, "Bebida"]
    if carrito:
        total = sum(v[0]*v[1] for v in carrito.values())
        if st.button(f"🛒 VER RESUMEN - RD${total}", width="stretch"): checkout_modal(carrito, mesa)
    st.markdown("<div class='footer-box'><h3 style='color:#e63946'>☕ Yamb Café</h3><p>¡Gracias por elegirnos! Tu pedido llegará a tu mesa en unos minutos.</p><p style='font-size: 0.8rem; color: #888;'>© 2024 Yamb Café - Menú Digital</p></div>", unsafe_allow_html=True)

with tab_admin:
    st.title("Pedidos Recibidos")
    if os.path.exists(file): st.dataframe(pd.read_csv(file), width="stretch")