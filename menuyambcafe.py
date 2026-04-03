import streamlit as st
import os
import pandas as pd
from datetime import datetime

logo_path = 'Vector Smart Object.png'
st.set_page_config(page_title='Yamb Café | Menú Digital', layout='wide')

# --- CSS para diseño de tarjetas e imágenes ---
st.markdown("""<style>
    .stApp { background-color: #ffffff; }
    .category-header { color: #e63946; border-bottom: 3px solid #e63946; padding-bottom: 5px; margin-top: 30px; font-weight: bold; text-transform: uppercase; }
    .menu-card { background: white; border: 1px solid #eee; border-radius: 15px; padding: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); text-align: center; }
    .price-tag { color: #e63946; font-weight: bold; font-size: 1.2rem; }
</style>""", unsafe_allow_html=True)

tab_menu, tab_admin = st.tabs(['📋 CARTA INTERACTIVA', '🔒 ADMINISTRACIÓN'])

with tab_menu:
    if os.path.exists(logo_path): st.image(logo_path, width=150)
    st.title("Menú Yamb Café")
    mesa = st.text_input("Número de Mesa", "1")
    
    carrito = {}

    # --- SECCIÓN COMIDAS ---
    st.markdown("<h2 class='category-header'>🍔 COMIDAS</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='menu-card'><h3>Burguer + Papas</h3><p class='price-tag'>RD$350</p></div>", unsafe_allow_html=True)
        qty_f1 = st.number_input("Cant.", 0, 10, key="f1")
        if qty_f1 > 0: carrito['Burguer + Papas'] = [qty_f1, 350]
    with c2:
        st.markdown("<div class='menu-card'><h3>Hot Dog Especial</h3><p class='price-tag'>RD$250</p></div>", unsafe_allow_html=True)
        qty_f2 = st.number_input("Cant.", 0, 10, key="f2")
        if qty_f2 > 0: carrito['Hot Dog Especial'] = [qty_f2, 250]
    with c3:
        st.markdown("<div class='menu-card'><h3>Pizza Personal</h3><p class='price-tag'>RD$300</p></div>", unsafe_allow_html=True)
        qty_f3 = st.number_input("Cant.", 0, 10, key="f3")
        if qty_f3 > 0: carrito['Pizza Personal'] = [qty_f3, 300]

    # --- SECCIÓN BEBIDAS ---
    st.markdown("<h2 class='category-header'>☕ BEBIDAS</h2>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown("<div class='menu-card'><h3>Cappuccino</h3><p class='price-tag'>RD$180</p></div>", unsafe_allow_html=True)
        qty_b1 = st.number_input("Cant.", 0, 10, key="b1")
        if qty_b1 > 0: carrito['Cappuccino'] = [qty_b1, 180]
    with b2:
        st.markdown("<div class='menu-card'><h3>Cerveza</h3><p class='price-tag'>RD$150</p></div>", unsafe_allow_html=True)
        qty_b2 = st.number_input("Cant.", 0, 10, key="b2")
        if qty_b2 > 0: carrito['Cerveza'] = [qty_b2, 150]
    with b3:
        st.markdown("<div class='menu-card'><h3>Jugo Natural</h3><p class='price-tag'>RD$120</p></div>", unsafe_allow_html=True)
        qty_b3 = st.number_input("Cant.", 0, 10, key="b3")
        if qty_b3 > 0: carrito['Jugo Natural'] = [qty_b3, 120]

    st.divider()
    if carrito:
        st.subheader("📝 Resumen de tu Pedido")
        # Crear tabla de resumen
        resumen_data = []
        total_general = 0
        for item, info in carrito.items():
            subtotal = info[0] * info[1]
            resumen_data.append({"Producto": item, "Cantidad": info[0], "Precio Unit.": f"RD${info[1]}", "Subtotal": f"RD${subtotal}"})
            total_general += subtotal
        
        st.table(pd.DataFrame(resumen_data))
        st.markdown(f"### **Total a Pagar: RD${total_general}**")

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
    st.markdown("## 🔐 Panel de Control")
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
