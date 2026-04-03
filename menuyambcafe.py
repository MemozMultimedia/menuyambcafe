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
    .menu-card { background-color: white; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px; overflow: hidden; transition: transform 0.3s; }
    .menu-card:hover { transform: scale(1.02); }
    .menu-img { width: 100%; height: 180px; object-fit: cover; }
    .menu-content { padding: 15px; }
    .price-tag { color: #FF4B4B; font-weight: bold; font-size: 1.2em; }
    h1, h2, h3 { color: #2d3436; font-family: 'Segoe UI', sans-serif; }
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
    return make_hashes(password) == hashed_text

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user' not in st.session_state: st.session_state['user'] = ""

# --- MENÚ DE PRODUCTOS CON IMÁGENES ---
menu = {
    "☕ Bebidas Especiales": {
        "Café Latte": {"p": 150, "img": "https://images.unsplash.com/photo-1536939459926-301728717817?q=80&w=400"},
        "Capuccino": {"p": 160, "img": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?q=80&w=400"},
        "Jugo Natural": {"p": 120, "img": "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?q=80&w=400"}
    },
    "🍔 Platos Premium": {
        "Burger Gourmet": {"p": 450, "img": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=400"},
        "Pizza Artesanal": {"p": 600, "img": "https://images.unsplash.com/photo-1513104890138-7c749659a591?q=80&w=400"},
        "Club Sandwich": {"p": 350, "img": "https://images.unsplash.com/photo-1525351484163-7529414344d8?q=80&w=400"}
    }
}

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3170/3170733.png", width=80)
    if not st.session_state['logged_in']:
        choice = st.radio("Acceso", ["Login", "Registro"])
    else:
        st.success(f"Hola, {st.session_state['user']}")
        choice = st.selectbox("Panel", ["Hacer Pedido", "Mis Pedidos", "Admin"])
        if st.button("Cerrar Sesión"): st.session_state['logged_in'] = False; st.rerun()

if not st.session_state['logged_in']:
    if choice == "Registro":
        st.title("📝 Registro")
        nu = st.text_input("Usuario")
        nn = st.text_input("Nombre")
        np = st.text_input("Password", type='password')
        if st.button("Registrarme"):
            df = pd.read_csv(USERS_FILE)
            if nu in df['user'].values: st.error("Existe")
            else:
                pd.DataFrame([[nu, make_hashes(np), nn]], columns=["user", "password", "nombre"]).to_csv(USERS_FILE, mode='a', header=False, index=False)
                st.success("¡Listo! Inicia sesión")
    else:
        st.title("🔐 Login")
        u = st.text_input("Usuario")
        p = st.text_input("Password", type='password')
        if st.button("Entrar"):
            df = pd.read_csv(USERS_FILE)
            ud = df[df['user'] == u]
            if not ud.empty and check_hashes(p, ud.iloc[0]['password']):
                st.session_state['logged_in'] = True; st.session_state['user'] = u; st.rerun()
            else: st.error("Error")
else:
    if choice == "Hacer Pedido":
        st.title("🍽️ Menú con Imágenes")
        mesa = st.text_input("Mesa", value="1")
        carrito = []
        for cat, items in menu.items():
            st.subheader(cat)
            cols = st.columns(3)
            for i, (nombre, data) in enumerate(items.items()):
                with cols[i % 3]:
                    st.markdown(f"""<div class='menu-card'>
                        <img src='{data['img']}' class='menu-img'>
                        <div class='menu-content'>
                            <h4>{nombre}</h4>
                            <p class='price-tag'>RD${data['p']}</p>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    cant = st.number_input(f"Cant: {nombre}", 0, 10, 0, key=f"v_{nombre}")
                    if cant > 0: carrito.append((nombre, cant, data['p']))

        total = sum(c*p for n,c,p in carrito)
        st.markdown(f"### Total: RD${total}")
        if st.button("Confirmar Pedido") and total > 0:
            pd.DataFrame([[datetime.now().strftime('%Y-%m-%d %H:%M'), st.session_state['user'], mesa, ", ".join([f"{n} x{c}" for n,c,p in carrito]), total, "Pendiente"]], columns=["Fecha", "Usuario", "Mesa", "Pedido", "Total", "Pago"]).to_csv(ORDERS_FILE, mode='a', header=False, index=False)
            st.balloons(); st.success("¡Pedido enviado!")

    elif choice == "Mis Pedidos":
        st.title("📋 Mis Pedidos")
        df = pd.read_csv(ORDERS_FILE)
        st.dataframe(df[df['Usuario'] == st.session_state['user']], use_container_width=True)

    elif choice == "Admin":
        st.title("📊 Admin")
        df = pd.read_csv(ORDERS_FILE)
        st.metric("Ventas", f"RD${df['Total'].sum()}")
        st.dataframe(df, use_container_width=True)
