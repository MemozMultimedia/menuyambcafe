import streamlit as st
import pandas as pd
import os
from datetime import datetime

logo_path = 'Vector Smart Object.png'
file_db = 'pedidos.csv'

# Inicializar base de datos si no existe
if not os.path.exists(file_db):
    df_init = pd.DataFrame(columns=['Fecha', 'Mesa', 'Cliente', 'Cedula', 'Pedido', 'Total'])
    df_init.to_csv(file_db, index=False)

st.set_page_config(
    page_title='Yamb Café | Menú Digital',
    page_icon=logo_path,
    layout='wide',
    initial_sidebar_state='collapsed'
)

# CSS Mejorado
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    .stApp { background-color: #ffffff; color: #1e1e1e; font-family: 'Inter', sans-serif; }
    .category-header { color: #e63946; border-bottom: 3px solid #e63946; padding-bottom: 5px; margin-top: 30px; font-weight: 700; text-transform: uppercase; }
    .menu-card { background: white; border: 1px solid #f0f0f0; border-radius: 12px; padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center; }
    .price-tag { color: #e63946; font-weight: 700; font-size: 1.1rem; }
    .admin-box { background-color: #fdfdfd; border: 1px solid #eee; border-radius: 20px; padding: 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
</style>""", unsafe_allow_html=True)

tab_menu, tab_admin = st.tabs(['📋 CARTA INTERACTIVA', '🔒 ÁREA ADMINISTRATIVA'])

with tab_menu:
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if os.path.exists(logo_path): st.image(logo_path, use_container_width=True)

    st.markdown("<h1 style='text-align: center;'>Menú Yamb Café</h1>", unsafe_allow_html=True)
    mesa = st.text_input('Número de mesa', value='1')

    carrito = []

    # --- SECCIÓN COMIDAS ---
    st.markdown("<h3 class='category-header'>🍔 Comidas</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='menu-card'><h4>Burguer + Papas</h4><p class='price-tag'>RD$350</p></div>", unsafe_allow_html=True)
        f1 = st.number_input('Cant.', 0, 10, key='f1')
        if f1 > 0: carrito.append({'item': 'Burguer + Papas', 'cant': f1, 'precio': 350})
    with col2:
        st.markdown("<div class='menu-card'><h4>Hot Dog Especial</h4><p class='price-tag'>RD$250</p></div>", unsafe_allow_html=True)
        f2 = st.number_input('Cant.', 0, 10, key='f2')
        if f2 > 0: carrito.append({'item': 'Hot Dog Especial', 'cant': f2, 'precio': 250})
    with col3:
        st.markdown("<div class='menu-card'><h4>Hot Dog Solo</h4><p class='price-tag'>RD$150</p></div>", unsafe_allow_html=True)
        f3 = st.number_input('Cant.', 0, 10, key='f3')
        if f3 > 0: carrito.append({'item': 'Hot Dog Solo', 'cant': f3, 'precio': 150})

    # --- SECCIÓN BEBIDAS ---
    st.markdown("<h3 class='category-header'>☕ Bebidas y Cafés</h3>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown("<div class='menu-card'><h4>Cappuccino</h4><p class='price-tag'>RD$180</p></div>", unsafe_allow_html=True)
        b1 = st.number_input('Cant.', 0, 10, key='b1')
        if b1 > 0: carrito.append({'item': 'Cappuccino', 'cant': b1, 'precio': 180})
    with col5:
        st.markdown("<div class='menu-card'><h4>Cerveza Nacional</h4><p class='price-tag'>RD$150</p></div>", unsafe_allow_html=True)
        b2 = st.number_input('Cant.', 0, 10, key='b2')
        if b2 > 0: carrito.append({'item': 'Cerveza Nacional', 'cant': b2, 'precio': 150})
    with col6:
        st.markdown("<div class='menu-card'><h4>Jugo Natural</h4><p class='price-tag'>RD$120</p></div>", unsafe_allow_html=True)
        b3 = st.number_input('Cant.', 0, 10, key='b3')
        if b3 > 0: carrito.append({'item': 'Jugo Natural', 'cant': b3, 'precio': 120})

    if carrito:
        total = sum(c['cant'] * c['precio'] for c in carrito)
        st.divider()
        st.subheader("📝 Finalizar Pedido")
        st.write(f"**Total a pagar: RD${total}**")
        
        nombre_cliente = st.text_input("Tu Nombre Completo")
        cedula_cliente = st.text_input("Tu Cédula")

        if st.button("CONFIRMAR Y ENVIAR ORDEN", use_container_width=True):
            if nombre_cliente and cedula_cliente:
                # CORRECCIÓN DE SINTAXIS AQUÍ: Evitar escapes dentro de f-strings
                detalle_pedido = ', '.join([f'{c["item"]} (x{c["cant"]})' for c in carrito])
                nueva_orden = pd.DataFrame([{
                    'Fecha': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'Mesa': mesa,
                    'Cliente': nombre_cliente,
                    'Cedula': cedula_cliente,
                    'Pedido': detalle_pedido,
                    'Total': total
                }])
                nueva_orden.to_csv(file_db, mode='a', header=False, index=False)
                st.balloons()
                st.success("¡Pedido enviado con éxito! Lo estamos preparando.")
            else:
                st.error("Por favor completa tu nombre y cédula.")

with tab_admin:
    st.markdown("<h2 style='text-align: center;'>🔐 Acceso Administrativo</h2>", unsafe_allow_html=True)
    col_f, col_b = st.columns(2)
    
    with col_f:
        st.markdown("<div class='admin-box'>### 👨‍🍳 Cocina</div>", unsafe_allow_html=True)
        pass_f = st.text_input("Clave Cocina", type="password", key="p_f")
        if pass_f == "yamb123":
            st.success("Órdenes de Cocina")
            if os.path.exists(file_db):
                df_pedidos = pd.read_csv(file_db)
                st.dataframe(df_pedidos)
            else:
                st.info("No hay pedidos registrados.")
            
    with col_b:
        st.markdown("<div class='admin-box'>### 🍸 Bar</div>", unsafe_allow_html=True)
        pass_b = st.text_input("Clave Bar", type="password", key="p_b")
        if pass_b == "yamb456":
            st.success("Órdenes de Bar")
            if os.path.exists(file_db):
                df_pedidos = pd.read_csv(file_db)
                st.dataframe(df_pedidos)
            else:
                st.info("No hay pedidos registrados.")
