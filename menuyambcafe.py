import streamlit as st
import pandas as pd
import os

logo_path = 'Vector Smart Object.png'

st.set_page_config(
    page_title='Yamb Café | Menú Digital',
    page_icon=logo_path,
    layout='wide',
    initial_sidebar_state='collapsed'
)

# CSS mejorado para Legibilidad y Login Atractivo
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    .stApp { background-color: #ffffff; color: #1e1e1e; font-family: 'Inter', sans-serif; }
    
    .category-header { color: #e63946; border-bottom: 3px solid #e63946; padding-bottom: 5px; margin-top: 30px; font-weight: 700; text-transform: uppercase; }
    
    .menu-card { background: white; border: 1px solid #f0f0f0; border-radius: 12px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center; }
    
    .price-tag { color: #e63946; font-weight: 700; font-size: 1.1rem; }

    /* Estilo para el Login Admin */
    .admin-box { background-color: #fdfdfd; border: 1px solid #eee; border-radius: 20px; padding: 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
    .admin-title { color: #1e1e1e; text-align: center; font-weight: 700; margin-bottom: 20px; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; font-weight: 600; }
</style>""", unsafe_allow_html=True)

tab_menu, tab_admin = st.tabs(['📋 CARTA INTERACTIVA', '🔒 ÁREA ADMINISTRATIVA'])

with tab_menu:
    c1, c2, c3 = st.columns([1,1,1])
    with c2: 
        if os.path.exists(logo_path): st.image(logo_path, use_container_width=True)
    
    st.markdown("<h1 style='text-align: center;'>Menú Yamb Café</h1>", unsafe_allow_html=True)
    mesa = st.text_input('Número de mesa', value='1')

    st.markdown("<h3 class='category-header'>🍔 Comidas</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='menu-card'><h4>Burguer + Papas</h4><p class='price-tag'>RD$350</p></div>", unsafe_allow_html=True)
        st.number_input('Cant.', 0, 10, key='f1')
    with col2:
        st.markdown("<div class='menu-card'><h4>Hot Dog Especial</h4><p class='price-tag'>RD$250</p></div>", unsafe_allow_html=True)
        st.number_input('Cant.', 0, 10, key='f2')

    st.markdown("<h3 class='category-header'>☕ Bebidas</h3>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("<div class='menu-card'><h4>Cappuccino</h4><p class='price-tag'>RD$180</p></div>", unsafe_allow_html=True)
        st.number_input('Cant.', 0, 10, key='b1')
    with col4:
        st.markdown("<div class='menu-card'><h4>Cerveza Nacional</h4><p class='price-tag'>RD$150</p></div>", unsafe_allow_html=True)
        st.number_input('Cant.', 0, 10, key='b2')

    if st.button("CONFIRMAR PEDIDO", use_container_width=True):
        st.balloons()
        st.success("¡Pedido enviado con éxito!")

with tab_admin:
    st.markdown("<h2 class='admin-title'>🔐 Acceso Restringido</h2>", unsafe_allow_html=True)
    
    col_f, col_spacer, col_b = st.columns([1, 0.1, 1])
    
    with col_f:
        st.markdown("<div class='admin-box'>", unsafe_allow_html=True)
        st.markdown("### 👨‍🍳 Cocina")
        user_f = st.text_input("Usuario", key="u_f", placeholder="Admin Comida")
        pass_f = st.text_input("Contraseña", type="password", key="p_f")
        if st.button("Entrar a Cocina", use_container_width=True):
            if user_f == "admin" and pass_f == "123": st.success("Acceso concedido")
            else: st.error("Credenciales incorrectas")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='admin-box'>", unsafe_allow_html=True)
        st.markdown("### 🍸 Bar")
        user_b = st.text_input("Usuario", key="u_b", placeholder="Admin Bebida")
        pass_b = st.text_input("Contraseña", type="password", key="p_b")
        if st.button("Entrar a Bar", use_container_width=True):
            if user_b == "bar" and pass_b == "456": st.success("Acceso concedido")
            else: st.error("Credenciales incorrectas")
        st.markdown("</div>", unsafe_allow_html=True)
