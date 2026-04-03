import streamlit as st
import pandas as pd
from datetime import datetime
import os
import hashlib

st.set_page_config(page_title='Yamb Café - Control de Pedidos', layout='wide')

# --- ARCHIVOS DE BASE DE DATOS ---
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

# --- MENÚ ---
menu = {
    '☕ Bebidas': {'Café': 150, 'Capuccino': 180, 'Jugo Natural': 120},
    '🍔 Comida': {'Burger': 450, 'Pizza': 600, 'Club Sandwich': 350}
}

# --- NAVEGACIÓN ---
st.sidebar.title('Yamb Café')
modo = st.sidebar.radio('Navegar', ['Menú y Pedidos', 'Panel Admin (Recibidor)', 'Mi Cuenta'])

# ================= MI CUENTA / LOGIN =================
if modo == 'Mi Cuenta':
    st.header('👤 Gestión de Usuario')
    if not st.session_state['logged_in']:
        tab_l, tab_r = st.tabs(['Entrar', 'Registrarse'])
        with tab_l:
            u = st.text_input('Usuario')
            p = st.text_input('Contraseña', type='password')
            if st.button('Iniciar Sesión'):
                df = pd.read_csv(USERS_FILE)
                user_data = df[df['user'] == u]
                if not user_data.empty and check_hashes(p, user_data.iloc[0]['password']):
                    st.session_state['logged_in'] = True
                    st.session_state['user'] = u
                    st.rerun()
                else: st.error('Usuario o clave incorrecta')
        with tab_r:
            nu = st.text_input('Nuevo Usuario')
            np = st.text_input('Nueva Contraseña', type='password')
            if st.button('Crear Cuenta'):
                df = pd.read_csv(USERS_FILE)
                if nu in df['user'].values: st.error('El usuario ya existe')
                else:
                    pd.DataFrame([[nu, make_hashes(np), nu]], columns=['user', 'password', 'nombre']).to_csv(USERS_FILE, mode='a', header=False, index=False)
                    st.success('¡Cuenta creada! Ya puedes iniciar sesión.')
    else:
        st.write(f'Sesión activa: **{st.session_state["user"]}**')
        if st.button('Cerrar Sesión'):
            st.session_state['logged_in'] = False
            st.rerun()

# ================= MENÚ Y PEDIDOS =================
elif modo == 'Menú y Pedidos':
    st.header('🍽️ Realizar Pedido')
    mesa = st.text_input('Número de Mesa', '1')
    carrito = []
    for cat, items in menu.items():
        st.subheader(cat)
        for prod, precio in items.items():
            cant = st.number_input(f'{prod} (RD${precio})', 0, 10, 0, key=prod)
            if cant > 0: carrito.append({'prod': prod, 'cant': cant, 'sub': cant*precio})
    
    total = sum(item['sub'] for item in carrito)
    st.markdown(f'### Total: RD${total}')

    if st.button('Enviar Pedido'):
        if not st.session_state['logged_in']:
            st.warning('Debes iniciar sesión para pedir.')
        elif total == 0:
            st.error('El carrito está vacío.')
        else:
            pedido_str = ', '.join([f"{i['prod']} x{i['cant']}" for i in carrito])
            nuevo_pedido = pd.DataFrame([[
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                st.session_state['user'],
                mesa,
                pedido_str,
                total,
                'Pendiente'
            ]], columns=['Fecha', 'Usuario', 'Mesa', 'Pedido', 'Total', 'Status'])
            nuevo_pedido.to_csv(ORDERS_FILE, mode='a', header=False, index=False)
            st.success('¡Pedido enviado al recibidor!')

# ================= PANEL ADMIN =================
elif modo == 'Panel Admin (Recibidor)':
    st.header('📊 Recibidor de Pedidos (Control de Clientes)')
    if os.path.exists(ORDERS_FILE):
        df_pedidos = pd.read_csv(ORDERS_FILE)
        st.write('### Pedidos Recientes')
        st.dataframe(df_pedidos.sort_values(by='Fecha', ascending=False))
        
        st.write('### Resumen por Cliente')
        resumen = df_pedidos.groupby('Usuario')['Total'].sum().reset_index()
        st.table(resumen)
    else:
        st.info('No hay pedidos registrados.')
