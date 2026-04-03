import streamlit as st
import pandas as pd
import os
from datetime import datetime

logo_path = 'Vector Smart Object.png'

# --- Configuración con Favicon ---
st.set_page_config(
    page_title='Yamb Café | Menú Digital', 
    layout='wide', 
    page_icon=logo_path if os.path.exists(logo_path) else "🍴"
)

# --- CSS para diseño, logo centrado y admin flotante ---
st.markdown("""<style>
    .stApp { background-color: #ffffff; }
    .category-header { 
        background-color: #e63946; 
        color: white !important; 
        padding: 15px; 
        border-radius: 10px; 
        text-align: center; 
        margin: 30px 0 20px 0; 
        font-size: 1.8rem; 
        font-weight: bold; 
    }
    .product-card { 
        background: white; 
        border: 1px solid #f0f0f0; 
        border-radius: 15px; 
        padding: 15px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); 
        text-align: center; 
        margin-bottom: 20px;
    }
    .product-name { color: #1e1e1e; font-size: 1.2rem; font-weight: bold; margin: 10px 0; }
    .price-tag { color: #e63946; font-weight: 800; font-size: 1.1rem; }
    img { border-radius: 10px; }
    /* Icono admin arriba a la derecha */
    .admin-link { position: absolute; top: 10px; right: 20px; text-decoration: none; color: #ccc !important; font-size: 20px; }
</style>""", unsafe_allow_html=True)

# --- Función para el Pop-up (Modal) ---
@st.dialog("📝 Finalizar Pedido")
def confirmar_pedido_modal(carrito, mesa):
    st.write("Por favor, ingresa tus datos para procesar la orden:")
    with st.form("form_datos_modal"):
        nombre_cli = st.text_input("Nombre Completo")
        cedula_cli = st.text_input("Cédula")
        if st.form_submit_button("HACER EL PEDIDO", use_container_width=True):
            if nombre_cli and cedula_cli:
                st.success(f"✅ ¡Gracias {nombre_cli}! Pedido enviado para la mesa {mesa}.")
                st.balloons()
                st.rerun()
            else:
                st.error("Ambos campos son obligatorios.")

tab_menu, tab_admin = st.tabs(['📋 CARTA INTERACTIVA', '🔒 ADMINISTRACIÓN'])

img_placeholder = "https://via.placeholder.com/150"

with tab_menu:
    # Icono Admin discreto en la esquina (CSS)
    st.markdown('<a href="#administraci-n" class="admin-link">⚙️</a>', unsafe_allow_html=True)

    col_l1, col_l2, col_l3 = st.columns([1,1,1])
    with col_l2:
        if os.path.exists(logo_path): 
            st.image(logo_path, use_container_width=True)
        else:
            st.markdown("<h1 style='text-align: center;'>YAMB CAFÉ</h1>", unsafe_allow_html=True)

    mesa = st.text_input("Mesa", "1")
    carrito = {}

    # --- CATEGORÍA: COMIDA ---
    st.markdown("<div class='category-header'>🍔 COMIDA</div>", unsafe_allow_html=True)
    cf1, cf2, cf3 = st.columns(3)
    comidas = [
        ("Burguer + Papas", 350, "f1"),
        ("Hot Dog Especial", 250, "f2"),
        ("Pizza Personal", 300, "f3")
    ]
    for col, (name, price, k) in zip([cf1, cf2, cf3], comidas):
        with col:
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)
            st.image(img_placeholder, use_container_width=True)
            st.markdown(f"<p class='product-name'>{name}</p><p class='price-tag'>RD${price}</p>", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 10, key=k)
            if qty > 0: carrito[name] = [qty, price]
            st.markdown("</div>", unsafe_allow_html=True)

    # --- CATEGORÍA: BEBIDA ---
    st.markdown("<div class='category-header'>☕ BEBIDA</div>", unsafe_allow_html=True)
    cb1, cb2, cb3 = st.columns(3)
    bebidas = [
        ("Cappuccino", 180, "b1"),
        ("Cerveza One", 100, "b2"),
        ("Jugo Natural", 120, "b3")
    ]
    for col, (name, price, k) in zip([cb1, cb2, cb3], bebidas):
        with col:
            st.markdown("<div class='product-card'>", unsafe_allow_html=True)
            st.image(img_placeholder, use_container_width=True)
            st.markdown(f"<p class='product-name'>{name}</p><p class='price-tag'>RD${price}</p>", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 10, key=k)
            if qty > 0: carrito[name] = [qty, price]
            st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    if carrito:
        total = sum(v[0]*v[1] for v in carrito.values())
        st.markdown(f"<h3 style='text-align: right;'>Total: RD${total}</h3>", unsafe_allow_html=True)
        if st.button("CONFIRMAR PEDIDO", use_container_width=True, type='primary'):
            confirmar_pedido_modal(carrito, mesa)

with tab_admin:
    st.info("Panel administrativo")
