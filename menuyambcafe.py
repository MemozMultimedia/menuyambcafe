import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title='Yamb Café | Menú Digital', layout='wide', initial_sidebar_state='collapsed')

# --- ESTILOS CSS CON IMÁGENES DE FONDO ---
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    /* Imagen de fondo para toda la app */
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1600');
        background-attachment: fixed;
        background-size: cover;
    }

    html, body, [class*='css'] { font-family: 'Poppins', sans-serif; }
    [data-testid='stSidebar'] { display: none; }
    
    /* Contenedor principal con transparencia */
    .main-container {
        background: rgba(255, 255, 255, 0.85);
        padding: 30px;
        border-radius: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }

    .menu-card {
        background-color: white;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        transition: transform 0.3s ease;
        overflow: hidden;
        border: none;
    }
    .menu-card:hover { transform: scale(1.03); }
    
    .menu-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
    }

    .menu-info { padding: 15px; text-align: center; }
    .menu-info h4 { margin: 0; color: #1a1a1a; font-weight: 600; }
    .price-tag { color: #e63946; font-weight: bold; font-size: 1.3rem; }
    
    .category-title {
        color: white;
        background: #e63946;
        padding: 10px 30px;
        border-radius: 50px;
        display: inline-block;
        margin: 30px 0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .login-box {
        background: white;
        padding: 40px;
        border-radius: 20px;
        max-width: 400px;
        margin: auto;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }

    .stButton>button {
        background-color: #e63946 !important;
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        font-weight: 600 !important;
    }

    .whatsapp-float { position: fixed; width: 60px; height: 60px; bottom: 40px; right: 40px; background-color: #25d366; color: #FFF; border-radius: 50px; text-align: center; font-size: 30px; box-shadow: 2px 2px 10px rgba(0,0,0,0.3); z-index: 100; }
    .whatsapp-icon { margin-top: 15px; }
</style>""", unsafe_allow_html=True)

st.markdown("""<a href='https://wa.me/1234567890' class='whatsapp-float' target='_blank'>
    <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css'>
    <i class='fa fa-whatsapp whatsapp-icon'></i>
</a>""", unsafe_allow_html=True)

ORDERS_FILE = 'pedidos.csv'
if not os.path.exists(ORDERS_FILE):
    pd.DataFrame(columns=['Fecha', 'Cliente', 'Cedula', 'Mesa', 'Pedido', 'Total', 'Status']).to_csv(ORDERS_FILE, index=False)

menu_data = {
    '☕ Especialidades de Café': [
        {'name': 'Espresso Intenso', 'price': 150, 'img': 'https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=600'},
        {'name': 'Capuccino Art', 'price': 180, 'img': 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=600'}
    ],
    '🍔 Comida Gourmet': [
        {'name': 'Yamb Burger Special', 'price': 450, 'img': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600'},
        {'name': 'Pizza Artesana', 'price': 600, 'img': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600'}
    ]
}

tab_menu, tab_admin = st.tabs(['✨ CARTA DIGITAL', '🔒 ADMIN'])

with tab_menu:
    st.markdown("<center><div style='background:rgba(255,255,255,0.8); padding:20px; border-radius:20px; display:inline-block;'><h1 style='color:#1a1a1a; margin:0;'>YAMB CAFÉ</h1><p style='color:#e63946; font-weight:bold; margin:0;'>EXPERIENCIA GOURMET</p></div></center>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    mesa = col2.text_input('Número de Mesa', '1')

    carrito = []
    for cat, items in menu_data.items():
        st.markdown(f"<center><h2 class='category-title'>{cat}</h2></center>", unsafe_allow_html=True)
        cols = st.columns(2)
        for idx, item in enumerate(items):
            with cols[idx % 2]:
                st.markdown(f"""<div class='menu-card'><img src='{item['img']}' class='menu-img'><div class='menu-info'><h4>{item['name']}</h4><p class='price-tag'>RD${item['price']}</p></div></div>""", unsafe_allow_html=True)
                cant = st.number_input(f"Agregar", 0, 10, 0, key=f"q_{item['name']}")
                if cant > 0: carrito.append({'name': item['name'], 'q': cant, 'sub': cant*item['price']})
    
    total = sum(i['sub'] for i in carrito)
    if total > 0:
        st.markdown(f"<div style='background:white; padding:20px; border-radius:15px; text-align:center; box-shadow:0 4px 15px rgba(0,0,0,0.1);'><h3>Total Pedido: RD${total}</h3></div>", unsafe_allow_html=True)
        if st.button('🚀 CONFIRMAR PEDIDO'): st.session_state['confirmando'] = True

    if st.session_state.get('confirmando'):
        with st.expander("Finalizar mi Pedido", expanded=True):
            nombre = st.text_input("Tu Nombre")
            cedula = st.text_input("Cédula")
            if st.button("ENVIAR A COCINA"):
                if nombre and cedula:
                    p_str = ', '.join([f"{i['name']} x{i['q']}" for i in carrito])
                    nuevo = pd.DataFrame([[datetime.now().strftime('%H:%M'), nombre, cedula, mesa, p_str, total, 'Pendiente']], columns=['Fecha', 'Cliente', 'Cedula', 'Mesa', 'Pedido', 'Total', 'Status'])
                    nuevo.to_csv(ORDERS_FILE, mode='a', header=False, index=False)
                    st.balloons(); st.success("¡Pedido enviado!"); st.session_state['confirmando'] = False

with tab_admin:
    if not st.session_state.get('admin_logged'):
        st.markdown("<br><div class='login-box'><h3>Acceso Restringido</h3>", unsafe_allow_html=True)
        u, p = st.text_input("Usuario"), st.text_input("Clave", type="password")
        if st.button("ENTRAR"): 
            if u=="admin" and p=="yamb2024": st.session_state['admin_logged']=True; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        if st.button("Salir"): st.session_state['admin_logged']=False; st.rerun()
        if os.path.exists(ORDERS_FILE): st.dataframe(pd.read_csv(ORDERS_FILE))
