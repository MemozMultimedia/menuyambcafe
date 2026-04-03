import streamlit as st
import pandas as pd
import os

logo_path = 'Vector Smart Object.png'
st.set_page_config(page_title='Yamb Café | Menú', layout='wide')

# --- CSS ---
st.markdown("""<style>
    .stApp { background-color: #ffffff; }
    .category-title { background-color: #e63946; color: white !important; padding: 10px; border-radius: 10px; text-align: center; margin-top: 20px; }
    .menu-card { background: white; border: 1px solid #eee; border-radius: 15px; padding: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); text-align: center; }
    .price-tag { color: #e63946; font-weight: bold; }
</style>""", unsafe_allow_html=True)

tab_menu, tab_admin = st.tabs(['📋 CARTA INTERACTIVA', '🔒 ADMINISTRACIÓN'])

with tab_menu:
    st.title("🍽️ Nuestro Menú")
    mesa = st.text_input("Mesa", "1")
    carrito = {}

    # --- COMIDAS PRIMERO ---
    st.markdown("<h2 class='category-title'>🍔 COMIDAS</h2>", unsafe_allow_html=True)
    cf1, cf2, cf3 = st.columns(3)
    with cf1:
        st.markdown("<div class='menu-card'><h3>Burguer + Papas</h3><p class='price-tag'>RD$350</p></div>", unsafe_allow_html=True)
        carrito['Burguer'] = [st.number_input("Cant.", 0, 20, key='f1'), 350]
    with cf2:
        st.markdown("<div class='menu-card'><h3>Hot Dog Solo</h3><p class='price-tag'>RD$150</p></div>", unsafe_allow_html=True)
        carrito['HD_S'] = [st.number_input("Cant.", 0, 20, key='f2'), 150]
    with cf3:
        st.markdown("<div class='menu-card'><h3>Hot Dog + Papas</h3><p class='price-tag'>RD$250</p></div>", unsafe_allow_html=True)
        carrito['HD_P'] = [st.number_input("Cant.", 0, 20, key='f3'), 250]

    # --- BEBIDAS DESPUÉS ---
    st.markdown("<h2 class='category-title'>☕ BEBIDAS</h2>", unsafe_allow_html=True)
    cb1, cb2, cb3 = st.columns(3)
    with cb1:
        st.markdown("<div class='menu-card'><h3>Cuba Libre</h3><p class='price-tag'>RD$150</p></div>", unsafe_allow_html=True)
        carrito['CubaLibre'] = [st.number_input("Cant.", 0, 20, key='b1'), 150]
    with cb2:
        st.markdown("<div class='menu-card'><h3>Vodka Naranja</h3><p class='price-tag'>RD$150</p></div>", unsafe_allow_html=True)
        carrito['Vodka'] = [st.number_input("Cant.", 0, 20, key='b2'), 150]
    with cb3:
        st.markdown("<div class='menu-card'><h3>Cerveza One</h3><p class='price-tag'>RD$100</p></div>", unsafe_allow_html=True)
        carrito['Cerveza'] = [st.number_input("Cant.", 0, 20, key='b3'), 100]

    if st.button("CONFIRMAR PEDIDO"):
        st.success("Pedido enviado")

with tab_admin:
    st.header("Accesos Administrativos")
    col_admin1, col_admin2 = st.columns(2)
    
    with col_admin1:
        st.subheader("🍔 Admin Comida")
        user_f = st.text_input("Usuario Comida")
        pass_f = st.text_input("Clave Comida", type="password")
        if st.button("Entrar Comida"):
            if user_f == "admin_comida" and pass_f == "yamb123":
                st.success("Acceso a Comidas concedido")
            else: st.error("Error")
            
    with col_admin2:
        st.subheader("☕ Admin Bebidas")
        user_b = st.text_input("Usuario Bebidas")
        pass_b = st.text_input("Clave Bebidas", type="password")
        if st.button("Entrar Bebidas"):
            if user_b == "admin_bebida" and pass_b == "yamb456":
                st.success("Acceso a Bebidas concedido")
            else: st.error("Error")
