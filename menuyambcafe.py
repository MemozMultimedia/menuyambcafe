import streamlit as st
import pandas as pd
from datetime import datetime
import os

logo_path = 'Vector Smart Object.png'

st.set_page_config(
    page_title='Yamb Café | Menú Digital',
    page_icon=logo_path,
    layout='wide',
    initial_sidebar_state='collapsed'
)

# CSS optimizado para legibilidad (Alto Contraste)
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    .stApp {
        background-color: #ffffff !important;
        color: #1e1e1e !important;
    }

    /* Forzar color de texto en todos los elementos de Streamlit */
    h1, h2, h3, h4, p, span, label, .stMarkdown {
        color: #1e1e1e !important;
        font-family: 'Inter', sans-serif;
    }

    .menu-card {
        background-color: #ffffff;
        border: 2px solid #f0f0f0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: center;
    }

    .category-header {
        color: #e63946 !important;
        border-bottom: 3px solid #e63946;
        padding-bottom: 8px;
        margin: 40px 0 25px 0;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 1.5px;
    }

    .price-tag {
        font-weight: 700;
        font-size: 1.2rem;
        color: #e63946 !important;
    }

    /* Inputs y Botones */
    .stNumberInput div div input {
        color: #1e1e1e !important;
        background-color: #f9f9f9 !important;
    }

    .stButton>button {
        background-color: #e63946 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        border: none;
        padding: 10px 20px;
    }
</style>""", unsafe_allow_html=True)

# Lógica de Datos
ORDERS_FILE = 'pedidos.csv'
if not os.path.exists(ORDERS_FILE):
    pd.DataFrame(columns=['Fecha', 'Cliente', 'Cedula', 'Mesa', 'Pedido', 'Total', 'Status']).to_csv(ORDERS_FILE, index=False)

# Pestañas Superiores
tab_menu, tab_admin = st.tabs(['📋 CARTA INTERACTIVA', '🔒 ADMINISTRACIÓN'])

with tab_menu:
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if os.path.exists(logo_path): st.image(logo_path, use_container_width=True)

    st.markdown("<h1 style='text-align: center;'>Menú Yamb Café</h1>", unsafe_allow_html=True)
    mesa = st.text_input('Número de mesa', value='1')

    # Categoría: Comidas
    st.markdown("<h3 class='category-header'>🍔 Comidas Sugeridas</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='menu-card'><h4>Burguer + Papas</h4><p class='price-tag'>RD$350</p></div>", unsafe_allow_html=True)
        st.number_input('Cantidad', 0, 10, key='prod_1')
    with col2:
        st.markdown("<div class='menu-card'><h4>Hot Dog Especial</h4><p class='price-tag'>RD$250</p></div>", unsafe_allow_html=True)
        st.number_input('Cantidad', 0, 10, key='prod_2')

    # Categoría: Bebidas
    st.markdown("<h3 class='category-header'>☕ Bebidas y Cafés</h3>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("<div class='menu-card'><h4>Cappuccino</h4><p class='price-tag'>RD$180</p></div>", unsafe_allow_html=True)
        st.number_input('Cantidad', 0, 10, key='prod_3')
    with col4:
        st.markdown("<div class='menu-card'><h4>Cerveza Nacional</h4><p class='price-tag'>RD$150</p></div>", unsafe_allow_html=True)
        st.number_input('Cantidad', 0, 10, key='prod_4')

    st.markdown("--- settings ---")
    if st.button("CONFIRMAR Y ENVIAR PEDIDO"):
        st.balloons()
        st.success("¡Pedido recibido! Lo estamos preparando.")

with tab_admin:
    st.subheader("Panel de Control")
    st.info("El acceso está restringido a personal autorizado.")
