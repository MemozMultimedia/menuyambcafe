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

# CSS para Fondo Blanco y Estilo Elegante
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

    .stApp {
        background-color: #ffffff;
        color: #333333;
    }
    
    html, body, [class*='css'] { font-family: 'Inter', sans-serif; }

    .main-container {
        max-width: 900px;
        margin: auto;
        padding: 20px;
    }

    .menu-card {
        background-color: #ffffff;
        border: 1px solid #eeeeee;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
    }

    .category-header {
        color: #1a1a1a;
        border-bottom: 2px solid #e63946;
        padding-bottom: 10px;
        margin: 40px 0 20px 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    .order-section {
        background-color: #f9f9f9;
        border-radius: 20px;
        padding: 25px;
        border: 1px dashed #cccccc;
        margin-top: 30px;
    }

    .stButton>button {
        background-color: #e63946 !important;
        color: white !important;
        width: 100%;
        border-radius: 10px !important;
        height: 50px;
        font-weight: 600 !important;
    }
</style>""", unsafe_allow_html=True)

# Lógica de Datos
ORDERS_FILE = 'pedidos.csv'
if not os.path.exists(ORDERS_FILE):
    pd.DataFrame(columns=['Fecha', 'Cliente', 'Cedula', 'Mesa', 'Pedido', 'Total', 'Status']).to_csv(ORDERS_FILE, index=False)

# Estructura de la App
tab_menu, tab_admin = st.tabs(['📋 VER MENÚ', '🔒 ADMINISTRACIÓN'])

with tab_menu:
    # Logo central
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if os.path.exists(logo_path): st.image(logo_path, use_container_width=True)

    st.markdown("<h1 style='text-align: center;'>Menú Digital</h1>", unsafe_allow_html=True)
    mesa = st.text_input('Tu número de mesa', value='1')

    # Ejemplo de productos
    st.markdown("<h3 class='category-header'>☕ Cafetería</h3>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("<div class='menu-card'><h4>Café Americano</h4><p>RD$120</p></div>", unsafe_allow_html=True)
        c_am = st.number_input('Cantidad', 0, 10, key='am')

    with col_b:
        st.markdown("<div class='menu-card'><h4>Cappuccino</h4><p>RD$180</p></div>", unsafe_allow_html=True)
        c_cap = st.number_input('Cantidad', 0, 10, key='cap')

    # Sección de Pedido
    st.markdown("<div class='order-section'>", unsafe_allow_html=True)
    st.subheader("Confirmar Pedido")
    nombre = st.text_input("Nombre completo")
    cedula = st.text_input("Cédula (ID)")
    
    if st.button("ENVIAR PEDIDO"):
        if nombre and cedula:
            st.success(f"¡Gracias {nombre}! Pedido enviado.")
            st.balloons()
        else:
            st.warning("Por favor completa tus datos.")
    st.markdown("</div>", unsafe_allow_html=True)

with tab_admin:
    st.info("Ingresa tus credenciales para ver los pedidos en curso.")
