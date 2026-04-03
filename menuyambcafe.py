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

# Inyectamos el CSS de forma segura
st.markdown("""<style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1600');
        background-attachment: fixed;
        background-size: cover;
    }
    .main-container {
        background: rgba(255, 255, 255, 0.85);
        padding: 30px;
        border-radius: 30px;
    }
    .menu-card {
        background-color: white;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        text-align: center;
        overflow: hidden;
    }
    .menu-img { width: 100%; height: 180px; object-fit: cover; }
    .category-title { color: white; background: #e63946; padding: 10px 30px; border-radius: 50px; display: inline-block; margin: 20px 0; }
</style>""", unsafe_allow_html=True)

# Contenido de la Carta
col_l1, col_l2, col_l3 = st.columns([1,1,1])
with col_l2:
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)

st.markdown("<h1 style='text-align: center; color: white;'>Yamb Café</h1>", unsafe_allow_html=True)
st.info("El menú está cargando con el nuevo diseño...")
