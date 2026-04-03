import streamlit as st
import pandas as pd
from datetime import datetime
import os

logo_path = 'Vector Smart Object.png'
# Imagen de ejemplo para productos si no hay una específica
default_item_img = 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?q=80&w=500&auto=format&fit=crop'

st.set_page_config(
    page_title='Yamb Café | Menú Digital',
    page_icon=logo_path if os.path.exists(logo_path) else None,
    layout='wide',
    initial_sidebar_state='collapsed'
)

# Estilos CSS Mejorados para legibilidad y atractivo visual
st.markdown("""<style>
    .stApp { background-color: #ffffff; }
    
    /* Títulos y textos generales con alto contraste */
    h1, h2, h3, p, span, label { 
        color: #1a1a1a !important; 
        font-weight: 500 !important;
    }

    .menu-card {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 0px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
        overflow: hidden;
        border: 1px solid #f0f0f0;
    }
    
    .menu-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
    }

    .card-content {
        padding: 15px;
    }

    .price-tag {
        color: #e63946 !important;
        font-size: 1.2rem;
        font-weight: bold !important;
    }

    .stButton>button {
        background-color: #e63946 !important;
        color: white !important;
        border-radius: 12px !important;
        width: 100%;
        height: 50px;
        font-size: 18px !important;
        font-weight: bold !important;
        border: none !important;
    }

    /* Ajuste para inputs de número */
    .stNumberInput div div input {
        color: #1a1a1a !important;
        font-size: 1.1rem !important;
    }
</style>""", unsafe_allow_html=True)

# Persistencia de Datos
if not os.path.exists('pedidos.csv'):
    pd.DataFrame(columns=['Fecha', 'Cliente', 'Cedula', 'Mesa', 'Pedido', 'Total']).to_csv('pedidos.csv', index=False)

tab_menu, tab_admin = st.tabs(['📋 CARTA INTERACTIVA', '🔒 ACCESO ADMIN'])

with tab_menu:
    st.title("🍽️ Nuestro Menú")
    mesa = st.text_input("Número de Mesa", "1")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""<div class='menu-card'>
            <img src='{default_item_img}' class='menu-img'>
            <div class='card-content'>
                <h3>Café Especial</h3>
                <p class='price-tag'>RD$150</p>
            </div>
        </div>""", unsafe_allow_html=True)
        q1 = st.number_input("Cantidad", 0, 10, key='item1')

    with col2:
        st.markdown(f"""<div class='menu-card'>
            <img src='https://images.unsplash.com/photo-1551024601-bec78aea704b?q=80&w=500&auto=format&fit=crop' class='menu-img'>
            <div class='card-content'>
                <h3>Postre Premium</h3>
                <p class='price-tag'>RD$250</p>
            </div>
        </div>""", unsafe_allow_html=True)
        q2 = st.number_input("Cantidad", 0, 10, key='item2')

    if (q1 + q2) > 0:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("📝 Completa tu pedido")
        nombre = st.text_input("Tu Nombre Completo")
        cedula = st.text_input("Tu Cédula")
        
        if st.button("CONFIRMAR Y ENVIAR"):
            if nombre and cedula:
                st.success(f"¡Gracias {nombre}! Tu pedido ha sido enviado.")
                st.balloons()
            else:
                st.error("Por favor, introduce tu nombre y cédula para continuar.")

with tab_admin:
    st.subheader("Panel de Control Administrativo")
    st.info("Aquí se visualizarán los pedidos entrantes en tiempo real.")
    if os.path.exists('pedidos.csv'):
        df_view = pd.read_csv('pedidos.csv')
        st.dataframe(df_view)
