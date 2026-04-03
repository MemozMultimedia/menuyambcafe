import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title='Yamb Café | Menú Digital', layout='wide')

# --- CSS para diseño limpio con separación clara ---
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
</style>""", unsafe_allow_html=True)

tab_menu, tab_admin = st.tabs(['📋 CARTA INTERACTIVA', '🔒 ADMINISTRACIÓN'])

# Simulación de rutas de imágenes (deben existir en el repo)
img_placeholder = "https://via.placeholder.com/150"

with tab_menu:
    st.markdown("<h1 style='text-align: center; color: #1e1e1e;'>Menú Yamb Café</h1>", unsafe_allow_html=True)
    mesa = st.text_input("Número de Mesa", "1")
    
    carrito = {}

    # --- SECCIÓN EXCLUSIVA: COMIDAS ---
    st.markdown("<div class='category-header'>🍔 SECCIÓN COMIDAS</div>", unsafe_allow_html=True)
    cf1, cf2, cf3 = st.columns(3)
    
    with cf1:
        st.markdown("<div class='product-card'>", unsafe_allow_html=True)
        st.image(img_placeholder, use_container_width=True) # Reemplazar con ruta real
        st.markdown("<p class='product-name'>Burguer + Papas</p><p class='price-tag'>RD$350</p>", unsafe_allow_html=True)
        qty1 = st.number_input("Cantidad", 0, 10, key='f1')
        if qty1 > 0: carrito['Burguer + Papas'] = [qty1, 350]
        st.markdown("</div>", unsafe_allow_html=True)

    with cf2:
        st.markdown("<div class='product-card'>", unsafe_allow_html=True)
        st.image(img_placeholder, use_container_width=True)
        st.markdown("<p class='product-name'>Hot Dog Especial</p><p class='price-tag'>RD$250</p>", unsafe_allow_html=True)
        qty2 = st.number_input("Cantidad", 0, 10, key='f2')
        if qty2 > 0: carrito['Hot Dog Especial'] = [qty2, 250]
        st.markdown("</div>", unsafe_allow_html=True)

    with cf3:
        st.markdown("<div class='product-card'>", unsafe_allow_html=True)
        st.image(img_placeholder, use_container_width=True)
        st.markdown("<p class='product-name'>Pizza Personal</p><p class='price-tag'>RD$300</p>", unsafe_allow_html=True)
        qty3 = st.number_input("Cantidad", 0, 10, key='f3')
        if qty3 > 0: carrito['Pizza Personal'] = [qty3, 300]
        st.markdown("</div>", unsafe_allow_html=True)

    # --- SECCIÓN EXCLUSIVA: BEBIDAS ---
    st.markdown("<div class='category-header'>☕ SECCIÓN BEBIDAS</div>", unsafe_allow_html=True)
    cb1, cb2, cb3 = st.columns(3)

    with cb1:
        st.markdown("<div class='product-card'>", unsafe_allow_html=True)
        st.image(img_placeholder, use_container_width=True)
        st.markdown("<p class='product-name'>Cappuccino</p><p class='price-tag'>RD$180</p>", unsafe_allow_html=True)
        qty_b1 = st.number_input("Cantidad", 0, 10, key='b1')
        if qty_b1 > 0: carrito['Cappuccino'] = [qty_b1, 180]
        st.markdown("</div>", unsafe_allow_html=True)

    with cb2:
        st.markdown("<div class='product-card'>", unsafe_allow_html=True)
        st.image(img_placeholder, use_container_width=True)
        st.markdown("<p class='product-name'>Cerveza One</p><p class='price-tag'>RD$100</p>", unsafe_allow_html=True)
        qty_b2 = st.number_input("Cantidad", 0, 10, key='b2')
        if qty_b2 > 0: carrito['Cerveza One'] = [qty_b2, 100]
        st.markdown("</div>", unsafe_allow_html=True)

    with cb3:
        st.markdown("<div class='product-card'>", unsafe_allow_html=True)
        st.image(img_placeholder, use_container_width=True)
        st.markdown("<p class='product-name'>Jugo Natural</p><p class='price-tag'>RD$120</p>", unsafe_allow_html=True)
        qty_b3 = st.number_input("Cantidad", 0, 10, key='b3')
        if qty_b3 > 0: carrito['Jugo Natural'] = [qty_b3, 120]
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    if carrito:
        st.subheader("🛒 Resumen del Pedido")
        total = sum(v[0]*v[1] for v in carrito.values())
        st.write(f"Total: RD${total}")
        if st.button("CONFIRMAR PEDIDO", use_container_width=True, type='primary'):
            st.success("✅ Pedido enviado exitosamente")

with tab_admin:
    st.header("Acceso Administrativo")
    # Lógica de admin simplificada por brevedad
    st.info("Ingrese clave para ver pedidos")
