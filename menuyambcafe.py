import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- Configuración Inicial ---
logo_path = 'Vector Smart Object.png'
file = 'pedidos.csv'

if not os.path.exists(file):
    pd.DataFrame(columns=['Fecha', 'Mesa', 'Cliente', 'Pedido', 'Total', 'Categoria']).to_csv(file, index=False)

st.set_page_config(page_title='Yamb Café | Menú Digital', layout='wide', page_icon="☕")

# --- Estilos Modernos (UI/UX) ---
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [class*='st-'] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #ffffff; }
    .category-title { background-color: #e63946; color: white !important; padding: 12px; border-radius: 12px; text-align: center; margin: 25px 0; font-weight: 800; font-size: 1.5rem; text-transform: uppercase; }
    .product-card { background: #ffffff; border: 1px solid #f0f0f0; border-radius: 20px; padding: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px; }
    .product-name { color: #1e1e1e; font-weight: 700; font-size: 1.1rem; margin-top: 10px; }
    .product-price { color: #e63946; font-weight: 800; font-size: 1.2rem; }
    .footer-box { background: #f9f9f9; padding: 30px; border-radius: 20px; margin-top: 50px; text-align: center; border: 1px solid #eee; }
    .footer-title { color: #e63946; font-weight: 800; margin-bottom: 10px; }
    .stButton>button { border-radius: 12px; font-weight: 700; height: 3em; transition: 0.3s; }
</style>""", unsafe_allow_html=True)

@st.dialog("📝 Finalizar Orden")
def checkout_modal(carrito, mesa):
    st.markdown("### Datos del Cliente")
    with st.form("form_final"):
        nombre = st.text_input("Nombre Completo")
        cedula = st.text_input("Cédula / ID")
        if st.form_submit_button("ENVIAR PEDIDO AHORA", use_container_width=True):
            if nombre and cedula:
                for cat in ['Comida', 'Bebida']:
                    items = [f"{n} x{v[0]}" for n,v in carrito.items() if v[2] == cat]
                    if items:
                        subtotal = sum(v[0]*v[1] for n,v in carrito.items() if v[2] == cat)
                        pd.DataFrame([{'Fecha': datetime.now().strftime('%H:%M'), 'Mesa': mesa, 'Cliente': nombre, 'Pedido': ', '.join(items), 'Total': subtotal, 'Categoria': cat}]).to_csv(file, mode='a', header=False, index=False)
                st.success("¡Pedido recibido! Estará listo pronto.")
                st.balloons()
                st.rerun()

tab_menu, tab_admin = st.tabs(['📋 CARTA DIGITAL', '🔒 PANEL ADMIN'])

with tab_menu:
    c1, c2, c3 = st.columns([1,2,1])
    with c2: 
        if os.path.exists(logo_path): st.image(logo_path, use_container_width=True)
    
    mesa = st.text_input("📍 Número de Mesa", "1")
    carrito = {}

    # SECCIÓN COMIDA
    st.markdown("<div class='category-title'>🍔 Platos & Snacks</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    items_comida = [("Burguer + Papas", 350, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400", "f1"), ("Hot Dog Especial", 250, "https://images.unsplash.com/photo-1541214113241-21578d2d9b62?w=400", "f2")]
    for col, (name, price, img, k) in zip([col1, col2], items_comida):
        with col:
            st.markdown(f"<div class='product-card'><img src='{img}' style='width:100%; border-radius:15px;'><p class='product-name'>{name}</p><p class='product-price'>RD${price}</p></div>", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 10, key=k)
            if qty > 0: carrito[name] = [qty, price, "Comida"]

    # SECCIÓN BEBIDA
    st.markdown("<div class='category-title'>☕ Bebidas & Café</div>", unsafe_allow_html=True)
    bcol1, bcol2 = st.columns(2)
    items_bebida = [("Cappuccino", 180, "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=400", "b1"), ("Cerveza Fría", 150, "https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=400", "b2")]
    for col, (name, price, img, k) in zip([bcol1, bcol2], items_bebida):
        with col:
            st.markdown(f"<div class='product-card'><img src='{img}' style='width:100%; border-radius:15px;'><p class='product-name'>{name}</p><p class='product-price'>RD${price}</p></div>", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 10, key=k)
            if qty > 0: carrito[name] = [qty, price, "Bebida"]

    if carrito: 
        if st.button("🛒 CONFIRMAR MI PEDIDO", use_container_width=True, type='primary'): checkout_modal(carrito, mesa)

    st.markdown("""<div class='footer-box'><h3 class='footer-title'>GRACIAS POR TU COMPRA</h3><p>CADA PRODUCTO DE YAMB TIENE UN PROPÓSITO. APOYAS A JÓVENES TALENTOS EN LA MÚSICA Y EL ARTE.</p><b>COMPRASTE CON PROPÓSITO. APOYASTE EL TALENTO.</b></div>""", unsafe_allow_html=True)

with tab_admin:
    a1, a2 = st.columns(2)
    with a1:
        st.markdown("### 👨‍🍳 Cocina")
        u_c = st.text_input("Usuario Cocina")
        p_c = st.text_input("Pass Cocina", type="password")
        if u_c == "admin" and p_c == "yamb123":
            st.dataframe(pd.read_csv(file).query("Categoria == 'Comida'"), use_container_width=True)
    with a2:
        st.markdown("### 🍸 Bar")
        u_b = st.text_input("Usuario Bar")
        p_b = st.text_input("Pass Bar", type="password")
        if u_b == "admin" and p_b == "yamb456":
            st.dataframe(pd.read_csv(file).query("Categoria == 'Bebida'"), use_container_width=True)
