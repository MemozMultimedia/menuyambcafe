import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title='Yamb Café | Menú Digital', layout='wide', initial_sidebar_state='collapsed')

st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    html, body, [class*='css'] { font-family: 'Poppins', sans-serif; background-color: #ffffff; }
    [data-testid='stSidebar'] { display: none; }
    .main { background-color: #ffffff; }
    .menu-card { background-color: #fff; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); margin-bottom: 25px; border: 1px solid #f0f0f0; transition: transform 0.3s ease; overflow: hidden; }
    .menu-card:hover { transform: translateY(-5px); }
    .menu-img { width: 100%; height: 180px; object-fit: cover; border-bottom: 3px solid #e63946; }
    .menu-info { padding: 20px; text-align: center; }
    .menu-info h4 { margin: 0; color: #1a1a1a; font-weight: 600; }
    .price-tag { color: #e63946; font-weight: bold; font-size: 1.3rem; margin-top: 5px; }
    .category-title { color: #1a1a1a; font-weight: 600; text-align: center; margin: 40px 0 20px 0; text-transform: uppercase; letter-spacing: 2px; border-bottom: 2px solid #e63946; display: inline-block; }
    .login-box { max-width: 400px; margin: auto; padding: 40px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); background: white; text-align: center; }
    .stButton>button { background-color: #e63946 !important; color: white !important; border-radius: 50px !important; padding: 10px 25px !important; border: none !important; width: 100%; font-weight: 600 !important; }
</style>""", unsafe_allow_html=True)

ORDERS_FILE = 'pedidos.csv'
if not os.path.exists(ORDERS_FILE):
    pd.DataFrame(columns=['Fecha', 'Cliente', 'Cedula', 'Mesa', 'Pedido', 'Total', 'Status']).to_csv(ORDERS_FILE, index=False)

menu_data = {
    '☕ Especialidades de Café': [
        {'name': 'Espresso Intenso', 'price': 150, 'img': 'https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=600'},
        {'name': 'Capuccino Art', 'price': 180, 'img': 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=600'}
    ],
    '🍔 Para Picar': [
        {'name': 'Yamb Burger Special', 'price': 450, 'img': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600'},
        {'name': 'Pizza Artesana', 'price': 600, 'img': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600'}
    ]
}

tab_menu, tab_admin = st.tabs(['✨ CARTA DIGITAL', '🔒 ACCESO ADMIN'])

with tab_menu:
    st.markdown("<center><h1 style='color:#1a1a1a;'>YAMB CAFÉ</h1><p>Experiencia Gourmet</p></center>", unsafe_allow_html=True)
    mesa = st.text_input('Número de Mesa', '1')
    carrito = []
    for cat, items in menu_data.items():
        st.markdown(f"<center><h2 class='category-title'>{cat}</h2></center>", unsafe_allow_html=True)
        cols = st.columns(2)
        for idx, item in enumerate(items):
            with cols[idx % 2]:
                st.markdown(f"""<div class='menu-card'><img src='{item['img']}' class='menu-img'><div class='menu-info'><h4>{item['name']}</h4><p class='price-tag'>RD${item['price']}</p></div></div>""", unsafe_allow_html=True)
                cant = st.number_input(f"Cantidad", 0, 10, 0, key=f"q_{item['name']}")
                if cant > 0: carrito.append({'name': item['name'], 'q': cant, 'sub': cant*item['price']})
    total = sum(i['sub'] for i in carrito)
    if total > 0:
        st.markdown(f"### Total: RD${total}")
        if st.button('🚀 CONFIRMAR MI PEDIDO'): st.session_state['confirmando'] = True
    if st.session_state.get('confirmando'):
        with st.expander("Finalizar Pedido", expanded=True):
            nombre = st.text_input("Nombre")
            cedula = st.text_input("Cédula")
            if st.button("ENVIAR A COCINA"):
                if nombre and cedula:
                    p_str = ', '.join([f"{i['name']} x{i['q']}" for i in carrito])
                    nuevo = pd.DataFrame([[datetime.now().strftime('%H:%M'), nombre, cedula, mesa, p_str, total, 'Pendiente']], columns=['Fecha', 'Cliente', 'Cedula', 'Mesa', 'Pedido', 'Total', 'Status'])
                    nuevo.to_csv(ORDERS_FILE, mode='a', header=False, index=False)
                    st.success("Pedido Enviado!"); st.balloons(); st.session_state['confirmando'] = False

with tab_admin:
    if not st.session_state.get('admin_logged'):
        st.markdown("<div class='login-box'><h3>🔐 Acceso</h3>", unsafe_allow_html=True)
        u, p = st.text_input("Usuario"), st.text_input("Clave", type="password")
        if st.button("ENTRAR"): 
            if u=="admin" and p=="yamb2024": st.session_state['admin_logged']=True; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        if st.button("Salir"): st.session_state['admin_logged']=False; st.rerun()
        if os.path.exists(ORDERS_FILE): st.dataframe(pd.read_csv(ORDERS_FILE))
