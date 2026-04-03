import streamlit as st
import pandas as pd
from datetime import datetime
import os
import hashlib

st.set_page_config(page_title='Yamb Café - Menu Digital Pro', layout='wide')

# --- ESTILOS ---
st.markdown("""<style>
    .main { background-color: #f5f7f9; }
    .menu-card { background-color: white; border-radius: 15px; padding: 0px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; border: 1px solid #eee; overflow: hidden; }
    .menu-img { width: 100%; height: 200px; object-fit: cover; }
    .menu-info { padding: 15px; }
    .price-tag { color: #e63946; font-weight: bold; font-size: 1.2rem; }
    .category-title { color: #1d3557; border-left: 5px solid #e63946; padding-left: 10px; margin-top: 30px; }
</style>""", unsafe_allow_html=True)

# --- DB ---
USERS_FILE = 'usuarios.csv'
ORDERS_FILE = 'pedidos.csv'

def init_db():
    if not os.path.exists(USERS_FILE):
        pd.DataFrame(columns=['user', 'password', 'nombre']).to_csv(USERS_FILE, index=False)
    if not os.path.exists(ORDERS_FILE):
        pd.DataFrame(columns=['Fecha', 'Usuario', 'Mesa', 'Pedido', 'Total', 'Status']).to_csv(ORDERS_FILE, index=False)

init_db()

def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user' not in st.session_state: st.session_state['user'] = ''

menu_data = {
    '☕ Bebidas': [
        {'name': 'Café Espresso', 'price': 150, 'img': 'https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=400'},
        {'name': 'Capuccino Art', 'price': 180, 'img': 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=400'}
    ],
    '🍔 Comida': [
        {'name': 'Yamb Burger', 'price': 450, 'img': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400'},
        {'name': 'Pizza Artesanal', 'price': 600, 'img': 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400'}
    ]
}

st.sidebar.title('🦁 Yamb Café')
modo = st.sidebar.radio('Navegar', ['Menú y Pedidos', 'Panel Admin'])

if st.session_state['logged_in']:
    st.sidebar.success(f"Usuario: {st.session_state['user']}")
    if st.sidebar.button('Cerrar Sesión'):
        st.session_state['logged_in'] = False; st.rerun()

if modo == 'Menú y Pedidos':
    st.title('🍽️ Carta Digital')
    mesa = st.text_input('Tu Mesa', '1')

    carrito = []
    for cat, items in menu_data.items():
        st.markdown(f"<h2 class='category-title'>{cat}</h2>", unsafe_allow_html=True)
        cols = st.columns(2)
        for idx, item in enumerate(items):
            with cols[idx % 2]:
                st.markdown(f"""<div class='menu-card'>
                    <img src='{item['img']}' class='menu-img'>
                    <div class='menu-info'>
                        <h4>{item['name']}</h4>
                        <p class='price-tag'>RD${item['price']}</p>
                    </div>
                </div>""", unsafe_allow_html=True)
                cant = st.number_input(f"Cantidad", 0, 10, 0, key=item['name'])
                if cant > 0: carrito.append({'name': item['name'], 'q': cant, 'sub': cant*item['price']})

    total = sum(i['sub'] for i in carrito)
    st.sidebar.markdown(f"## Total: RD${total}")

    if st.sidebar.button('🚀 Confirmar Pedido'):
        if total == 0:
            st.sidebar.error('Carrito vacío')
        elif not st.session_state['logged_in']:
            st.session_state['show_login'] = True
        else:
            p_str = ', '.join([f"{i['name']} x{i['q']}" for i in carrito])
            pd.DataFrame([[datetime.now().strftime('%H:%M'), st.session_state['user'], mesa, p_str, total, 'Pendiente']],
                         columns=['Fecha', 'Usuario', 'Mesa', 'Pedido', 'Total', 'Status']).to_csv(ORDERS_FILE, mode='a', header=False, index=False)
            st.balloons(); st.success('¡Pedido enviado!')

    if 'show_login' in st.session_state and st.session_state['show_login'] and not st.session_state['logged_in']:
        st.divider()
        st.subheader("🔐 Identifícate para completar el pedido")
        t1, t2 = st.tabs(['Login', 'Registro'])
        with t1:
            u = st.text_input('Usuario')
            p = st.text_input('Clave', type='password')
            if st.button('Entrar'):
                df = pd.read_csv(USERS_FILE)
                if not df[df['user']==u].empty and check_hashes(p, df[df['user']==u].iloc[0]['password']):
                    st.session_state['logged_in'] = True; st.session_state['user'] = u; st.session_state['show_login'] = False; st.rerun()
                else: st.error('Datos incorrectos')
        with t2:
            nu = st.text_input('Nuevo Usuario')
            np = st.text_input('Nueva Clave', type='password')
            if st.button('Registrar y Pedir'):
                pd.DataFrame([[nu, make_hashes(np), nu]], columns=['user', 'password', 'nombre']).to_csv(USERS_FILE, mode='a', header=False, index=False)
                st.session_state['logged_in'] = True; st.session_state['user'] = nu; st.session_state['show_login'] = False; st.rerun()

elif modo == 'Panel Admin':
    st.header('📊 Recibidor de Pedidos')
    if os.path.exists(ORDERS_FILE):
        df = pd.read_csv(ORDERS_FILE)
        st.dataframe(df.sort_values(by='Fecha', ascending=False), use_container_width=True)
