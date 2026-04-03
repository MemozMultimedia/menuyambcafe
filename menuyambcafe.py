import streamlit as st
import pandas as pd
from datetime import datetime
import os

logo_path = 'Vector Smart Object.png'

st.set_page_config(
    page_title='Yamb Café | Menú Digital',
    page_icon=logo_path if os.path.exists(logo_path) else None,
    layout='wide',
    initial_sidebar_state='collapsed'
)

# Estilos CSS
st.markdown("""<style>
    .stApp { background-color: #ffffff; }
    h1, h2, h3, p, span, label { color: #1a1a1a !important; font-weight: 500 !important; }
    .category-title { 
        background-color: #e63946; 
        color: white !important; 
        padding: 10px 20px; 
        border-radius: 10px; 
        margin: 30px 0 15px 0;
        text-align: center;
    }
    .menu-card {
        background-color: #ffffff; border-radius: 20px; margin-bottom: 25px; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; 
        overflow: hidden; border: 1px solid #f0f0f0;
    }
    .menu-img { width: 100%; height: 160px; object-fit: cover; }
    .card-content { padding: 10px; }
    .price-tag { color: #e63946 !important; font-size: 1.1rem; font-weight: bold !important; }
    .stButton>button { 
        background-color: #e63946 !important; color: white !important; 
        border-radius: 12px !important; width: 100%; height: 50px; 
        font-size: 18px !important; font-weight: bold !important; 
    }
</style>""", unsafe_allow_html=True)

if not os.path.exists('pedidos.csv'):
    pd.DataFrame(columns=['Fecha', 'Cliente', 'Cedula', 'Mesa', 'Pedido', 'Total']).to_csv('pedidos.csv', index=False)

tab_menu, tab_admin = st.tabs(['📋 CARTA INTERACTIVA', '🔒 ACCESO ADMIN'])

with tab_menu:
    st.title("🍽️ Nuestro Menú")
    mesa = st.text_input("Número de Mesa", "1")
    carrito = {}

    # --- SECCIÓN BEBIDAS ---
    st.markdown("<h2 class='category-title'>☕ BEBIDAS Y CAFETERÍA</h2>", unsafe_allow_html=True)
    col_b1, col_b2, col_b3 = st.columns(3)
    
    with col_b1:
        st.markdown("<div class='menu-card'><img src='https://images.unsplash.com/photo-1541167760496-162955ed8a9f?q=80&w=400' class='menu-img'><div class='card-content'><h3>Café Americano</h3><p class='price-tag'>RD$120</p></div></div>", unsafe_allow_html=True)
        carrito['Café Americano'] = [st.number_input("Cantidad", 0, 10, key='b1'), 120]

    with col_b2:
        st.markdown("<div class='menu-card'><img src='https://images.unsplash.com/photo-1572490122747-3968b75cc699?q=80&w=400' class='menu-img'><div class='card-content'><h3>Jugo Natural</h3><p class='price-tag'>RD$150</p></div></div>", unsafe_allow_html=True)
        carrito['Jugo Natural'] = [st.number_input("Cantidad", 0, 10, key='b2'), 150]

    with col_b3:
        st.markdown("<div class='menu-card'><img src='https://images.unsplash.com/photo-1556679343-c7306c1976bc?q=80&w=400' class='menu-img'><div class='card-content'><h3>Té Frío</h3><p class='price-tag'>RD$100</p></div></div>", unsafe_allow_html=True)
        carrito['Té Frío'] = [st.number_input("Cantidad", 0, 10, key='b3'), 100]

    # --- SECCIÓN COMIDA ---
    st.markdown("<h2 class='category-title'>🍔 COMIDAS Y SNACKS</h2>", unsafe_allow_html=True)
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("<div class='menu-card'><img src='https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=400' class='menu-img'><div class='card-content'><h3>Hamburguesa Yamb</h3><p class='price-tag'>RD$350</p></div></div>", unsafe_allow_html=True)
        carrito['Hamburguesa Yamb'] = [st.number_input("Cantidad", 0, 10, key='c1'), 350]
    with col_c2:
        st.markdown("<div class='menu-card'><img src='https://images.unsplash.com/photo-1513104890138-7c749659a591?q=80&w=400' class='menu-img'><div class='card-content'><h3>Pizza Personal</h3><p class='price-tag'>RD$300</p></div></div>", unsafe_allow_html=True)
        carrito['Pizza Personal'] = [st.number_input("Cantidad", 0, 10, key='c2'), 300]

    total_general = sum(v[0] * v[1] for v in carrito.values())
    if total_general > 0:
        st.markdown(f"<h2 style='text-align:right;'>Total: RD${total_general}</h2>", unsafe_allow_html=True)
        st.subheader("📝 Completa tu pedido")
        nombre = st.text_input("Nombre Completo")
        cedula = st.text_input("Cédula")
        if st.button("CONFIRMAR Y ENVIAR"):
            if nombre and cedula:
                st.success("¡Pedido enviado!")
                st.balloons()
            else: st.error("Faltan datos.")

with tab_admin:
    st.subheader("Panel Admin")
    if os.path.exists('pedidos.csv'): st.dataframe(pd.read_csv('pedidos.csv'))
