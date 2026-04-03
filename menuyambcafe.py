import streamlit as st
import os
import pandas as pd
from datetime import datetime

logo_path = 'Vector Smart Object.png'
st.set_page_config(page_title='Yamb Café | Menú Digital', layout='wide')

# --- CSS para Máximo Contraste ---
st.markdown("""<style>
    .stApp { background-color: #ffffff; color: #1e1e1e; }
    .category-header { color: #e63946; border-bottom: 3px solid #e63946; padding-bottom: 5px; margin-top: 30px; font-weight: 800; text-transform: uppercase; font-size: 1.8rem; }
    .menu-card { background: #ffffff; border: 2px solid #f0f0f0; border-radius: 15px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center; }
    h3 { color: #1e1e1e !important; font-weight: 700 !important; }
    .price-tag { color: #e63946; font-weight: 800; font-size: 1.3rem; margin-top: 10px; }
    .stMarkdown p { color: #1e1e1e; font-weight: 500; }
    /* Ajuste para inputs y botones */
    .stNumberInput label { color: #1e1e1e !important; font-weight: bold; }
</style>""", unsafe_allow_html=True)

tab_menu, tab_admin = st.tabs(['📋 CARTA INTERACTIVA', '🔒 ADMINISTRACIÓN'])

with tab_menu:
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if os.path.exists(logo_path): st.image(logo_path, use_container_width=True)
    
    st.markdown("<h1 style='text-align: center; color: #1e1e1e;'>Menú Yamb Café</h1>", unsafe_allow_html=True)
    mesa = st.text_input("Número de Mesa", "1")
    
    carrito = {}

    # --- SECCIÓN COMIDAS ---
    st.markdown("<h2 class='category-header'>🍔 COMIDAS</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='menu-card'><h3>Burguer + Papas</h3><p class='price-tag'>RD$350</p></div>", unsafe_allow_html=True)
        qty_f1 = st.number_input("Cantidad", 0, 10, key="f1")
        if qty_f1 > 0: carrito['Burguer + Papas'] = [qty_f1, 350]
    with col2:
        st.markdown("<div class='menu-card'><h3>Hot Dog Especial</h3><p class='price-tag'>RD$250</p></div>", unsafe_allow_html=True)
        qty_f2 = st.number_input("Cantidad", 0, 10, key="f2")
        if qty_f2 > 0: carrito['Hot Dog Especial'] = [qty_f2, 250]
    with col3:
        st.markdown("<div class='menu-card'><h3>Pizza Personal</h3><p class='price-tag'>RD$300</p></div>", unsafe_allow_html=True)
        qty_f3 = st.number_input("Cantidad", 0, 10, key="f3")
        if qty_f3 > 0: carrito['Pizza Personal'] = [qty_f3, 300]

    # --- SECCIÓN BEBIDAS ---
    st.markdown("<h2 class='category-header'>☕ BEBIDAS</h2>", unsafe_allow_html=True)
    b_col1, b_col2, b_col3 = st.columns(3)
    with b_col1:
        st.markdown("<div class='menu-card'><h3>Cappuccino</h3><p class='price-tag'>RD$180</p></div>", unsafe_allow_html=True)
        qty_b1 = st.number_input("Cantidad", 0, 10, key="b1")
        if qty_b1 > 0: carrito['Cappuccino'] = [qty_b1, 180]
    with b_col2:
        st.markdown("<div class='menu-card'><h3>Cerveza</h3><p class='price-tag'>RD$150</p></div>", unsafe_allow_html=True)
        qty_b2 = st.number_input("Cantidad", 0, 10, key="b2")
        if qty_b2 > 0: carrito['Cerveza'] = [qty_b2, 150]
    with b_col3:
        st.markdown("<div class='menu-card'><h3>Jugo Natural</h3><p class='price-tag'>RD$120</p></div>", unsafe_allow_html=True)
        qty_b3 = st.number_input("Cantidad", 0, 10, key="b3")
        if qty_b3 > 0: carrito['Jugo Natural'] = [qty_b3, 120]

    st.divider()
    if carrito:
        st.subheader("📝 Resumen de tu Pedido")
        resumen_data = []
        total_general = 0
        for item, info in carrito.items():
            subtotal = info[0] * info[1]
            resumen_data.append({"Producto": item, "Cantidad": info[0], "Precio Unit.": f"RD${info[1]}", "Subtotal": f"RD${subtotal}"})
            total_general += subtotal
        
        st.table(pd.DataFrame(resumen_data))
        st.markdown(f"<h3 style='color: #e63946;'>Total a Pagar: RD${total_general}</h3>", unsafe_allow_html=True)

        st.subheader("Confirmar Datos")
        nombre = st.text_input("Nombre Completo")
        cedula = st.text_input("Cédula / ID")
        
        if st.button("ENVIAR PEDIDO", use_container_width=True):
            if nombre and cedula:
                st.success(f"✅ {nombre}, su pedido por RD${total_general} ha sido recibido.")
                st.balloons()
            else:
                st.warning("Por favor ingrese su nombre y cédula para finalizar.")

with tab_admin:
    st.markdown("<h2 style='color: #1e1e1e;'>🔐 Panel de Control</h2>", unsafe_allow_html=True)
    col_cocina, col_bar = st.columns(2)
    with col_cocina:
        st.info("👨‍🍳 Cocina")
        u_c = st.text_input("Usuario", key="admin_c")
        p_c = st.text_input("Clave", type="password", key="pass_c")
        if st.button("Acceder Cocina"):
            if p_c == "yamb123": st.success("Acceso concedido")
    with col_bar:
        st.info("🍸 Bar")
        u_b = st.text_input("Usuario", key="admin_b")
        p_b = st.text_input("Clave", type="password", key="pass_b")
        if st.button("Acceder Bar"):
            if p_b == "yamb456": st.success("Acceso concedido")
