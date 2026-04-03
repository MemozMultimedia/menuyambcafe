import streamlit as st
import pandas as pd
from datetime import datetime
import os
import hashlib

st.set_page_config(page_title="Yamb Café - Premium Menu", layout="wide", initial_sidebar_state="expanded")

# --- ESTILOS PERSONALIZADOS (UI/UX) ---
st.markdown("""<style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF4B4B; color: white; border: none; font-weight: bold; }
    .stButton>button:hover { background-color: #ff3333; border: none; }
    .menu-card { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; border-left: 5px solid #FF4B4B; }
    .price-tag { color: #FF4B4B; font-weight: bold; font-size: 1.2em; }
    h1, h2, h3 { color: #2d3436; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2d3436,#2d3436); color: white; }
</style>""", unsafe_allow_html=True)

# --- GESTIÓN DE DATOS ---
USERS_FILE = "usuarios.csv"
ORDERS_FILE = "pedidos.csv"

def init_db():
    if not os.path.exists(USERS_FILE):
        pd.DataFrame(columns=["user", "password", "nombre"]).to_csv(USERS_FILE, index=False)
    if not os.path.exists(ORDERS_FILE):
        pd.DataFrame(columns=["Fecha", "Usuario", "Mesa", "Pedido", "Total", "Pago"]).to_csv(ORDERS_FILE, index=False)

init_db()

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# --- LÓGICA DE SESIÓN ---
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user' not in st.session_state: st.session_state['user'] = ""

# --- MENÚ DE PRODUCTOS ---
menu = {
    "☕ Bebidas Especiales": {"Café Latte": 150, "Capuccino": 160, "Jugo Natural": 120},
    "🍔 Platos Premium": {"Burger Gourmet": 450, "Pizza Artesanal": 600, "Club Sandwich": 350}
}

# --- SIDEBAR: NAVEGACIÓN ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3170/3170733.png", width=100)
    if not st.session_state['logged_in']:
        choice = st.radio("Acceso", ["Login", "Registro"])
    else:
        st.success(f"Bienvenido, {st.session_state['user']}")
        choice = st.selectbox("Panel", ["Hacer Pedido", "Mis Pedidos", "Admin"])
        if st.button("Cerrar Sesión"):
            st.session_state['logged_in'] = False
            st.rerun()

# --- FLUJO DE USUARIOS ---
if not st.session_state['logged_in']:
    if choice == "Registro":
        st.title("📝 Crea tu cuenta")
        new_user = st.text_input("Usuario")
        new_name = st.text_input("Nombre Completo")
        new_password = st.text_input("Contraseña", type='password')
        if st.button("Registrarme"):
            df = pd.read_csv(USERS_FILE)
            if new_user in df['user'].values:
                st.error("El usuario ya existe")
            else:
                new_row = pd.DataFrame([[new_user, make_hashes(new_password), new_name]], columns=["user", "password", "nombre"])
                new_row.to_csv(USERS_FILE, mode='a', header=False, index=False)
                st.success("!Cuenta creada! Por favor inicia sesión.")

    elif choice == "Login":
        st.title("🔐 Iniciar Sesión")
        user = st.text_input("Usuario")
        password = st.text_input("Contraseña", type='password')
        if st.button("Entrar"):
            df = pd.read_csv(USERS_FILE)
            user_data = df[df['user'] == user]
            if not user_data.empty and check_hashes(password, user_data.iloc[0]['password']):
                st.session_state['logged_in'] = True
                st.session_state['user'] = user
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

else:
    # --- CLIENTE: PEDIDOS ---
    if choice == "Hacer Pedido":
        st.title("🍽️ Nuestro Menú")
        mesa = st.text_input("Número de Mesa", value="1")
        
        carrito = []
        for cat, items in menu.items():
            st.markdown(f"### {cat}")
            cols = st.columns(3)
            for i, (nombre, precio) in enumerate(items.items()):
                with cols[i % 3]:
                    st.markdown(f"""<div class='menu-card'>
                        <h4>{nombre}</h4>
                        <p class='price-tag'>RD${precio}</p>
                    </div>""", unsafe_allow_html=True)
                    cant = st.number_input(f"Cantidad de {nombre}", 0, 10, 0, key=f"q_{nombre}")
                    if cant > 0: carrito.append((nombre, cant, precio))

        total = sum(c*p for n,c,p in carrito)
        st.markdown(f"## 💰 Total a Pagar: RD${total}")
        pago = st.selectbox("Método de Pago", ["Efectivo", "Tarjeta", "Transferencia"])
        
        if st.button("Confirmar Pedido"):
            if total > 0:
                pedido_txt = ", ".join([f"{n} x{c}" for n,c,p in carrito])
                nuevo = pd.DataFrame([[datetime.now().strftime('%Y-%m-%d %H:%M'), st.session_state['user'], mesa, pedido_txt, total, pago]], 
                                     columns=["Fecha", "Usuario", "Mesa", "Pedido", "Total", "Pago"])
                nuevo.to_csv(ORDERS_FILE, mode='a', header=False, index=False)
                st.balloons()
                st.success("✅ !Pedido enviado con éxito!")
            else:
                st.warning("El carrito está vacío")

    elif choice == "Mis Pedidos":
        st.title("📋 Mi Historial")
        df = pd.read_csv(ORDERS_FILE)
        mis_pedidos = df[df['Usuario'] == st.session_state['user']]
        st.dataframe(mis_pedidos, use_container_width=True)

    elif choice == "Admin":
        st.title("📊 Dashboard Administrativo")
        df = pd.read_csv(ORDERS_FILE)
        col1, col2 = st.columns(2)
        col1.metric("Ventas Totales", f"RD${df['Total'].sum()}")
        col2.metric("Pedidos Totales", len(df))
        st.write("### Detalle de Ventas")
        st.dataframe(df, use_container_width=True)
