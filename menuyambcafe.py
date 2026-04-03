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
    st.markdown("<h2 class='category-title'>☕ BEBIDAS</h2>", unsafe_allow_html=True)
    cb1, cb2, cb3 = st.columns(3)
    
    with cb1:
        st.markdown("<div class='menu-card'><img src='https://images.unsplash.com/photo-1574096079513-d8259312b785?q=80&w=400' class='menu-img'><div class='card-content'><h3>Cuba Libre (RON/COLA)</h3><p class='price-tag'>RD$150</p></div></div>", unsafe_allow_html=True)
        carrito['Cuba Libre'] = [st.number_input("Cant.", 0, 20, key='dr1'), 150]

    with cb2:
        st.markdown("<div class='menu-card'><img src='https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?q=80&w=400' class='menu-img'><div class='card-content'><h3>Vodka Naranja</h3><p class='price-tag'>RD$150</p></div></div>", unsafe_allow_html=True)
        carrito['Vodka Naranja'] = [st.number_input("Cant.", 0, 20, key='dr2'), 150]

    with cb3:
        st.markdown("<div class='menu-card'><img src='https://images.unsplash.com/photo-1535958636474-b021ee887b13?q=80&w=400' class='menu-img'><div class='card-content'><h3>Pz Presidente</h3><p class='price-tag'>RD$150</p></div></div>", unsafe_allow_html=True)
        carrito['Pz Presidente'] = [st.number_input("Cant.", 0, 20, key='dr3'), 150]

    cb4, cb5, cb6 = st.columns(3)
    with cb4:
        st.markdown("<div class='menu-card'><img src='https://images.unsplash.com/photo-1618885472179-5e4aa4a37ff1?q=80&w=400' class='menu-img'><div class='card-content'><h3>Cerveza One</h3><p class='price-tag'>RD$100</p></div></div>", unsafe_allow_html=True)
        carrito['Cerveza One'] = [st.number_input("Cant.", 0, 20, key='dr4'), 100]
    with cb5:
        st.markdown("<div class='menu-card'><img src='https://images.unsplash.com/photo-1608270586620-248524c67de9?q=80&w=400' class='menu-img'><div class='card-content'><h3>Heineken</h3><p class='price-tag'>RD$180</p></div></div>", unsafe_allow_html=True)
        carrito['Heineken'] = [st.number_input("Cant.", 0, 20, key='dr5'), 180]
    with cb6:
        st.markdown("<div class='menu-card'><img src='https://images.unsplash.com/photo-1560023907-5f339617ea30?q=80&w=400' class='menu-img'><div class='card-content'><h3>Agua/Refresco</h3><p class='price-tag'>RD$50</p></div></div>", unsafe_allow_html=True)
        carrito['Agua/Refresco'] = [st.number_input("Cant.", 0, 20, key='dr6'), 50]

    # --- SECCIÓN COMIDA ---
    st.markdown("<h2 class='category-title'>🍔 COMIDAS</h2>", unsafe_allow_html=True)
    cf1, cf2, cf3 = st.columns(3)

    with cf1:
        st.markdown("<div class='menu-card'><img src='https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=400' class='menu-img'><div class='card-content'><h3>Burguer + Papas</h3><p class='price-tag'>RD$350</p></div></div>", unsafe_allow_html=True)
        carrito['Burguer + Papas'] = [st.number_input("Cant.", 0, 20, key='fd1'), 350]

    with cf2:
        st.markdown("<div class='menu-card'><img src='https://images.unsplash.com/photo-1541214113241-21578d2d9b62?q=80&w=400' class='menu-img'><div class='card-content'><h3>Hot Dog Solo</h3><p class='price-tag'>RD$150</p></div></div>", unsafe_allow_html=True)
        carrito['Hot Dog Solo'] = [st.number_input("Cant.", 0, 20, key='fd2'), 150]

    with cf3:
        st.markdown("<div class='menu-card'><img src='https://images.unsplash.com/photo-1623238913973-21e45cced554?q=80&w=400' class='menu-img'><div class='card-content'><h3>Hot Dog + Papas</h3><p class='price-tag'>RD$250</p></div></div>", unsafe_allow_html=True)
        carrito['Hot Dog + Papas'] = [st.number_input("Cant.", 0, 20, key='fd3'), 250]

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
