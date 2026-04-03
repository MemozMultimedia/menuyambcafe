import streamlit as st
import pandas as pd
import os
from datetime import datetime
import base64

st.set_page_config(page_title="YAMB CAFE", layout="wide")

# ================== FONDO CON TU IMAGEN ==================
def set_bg(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """, unsafe_allow_html=True)

set_bg("menu.png")

# ================== CSS PRO ==================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

html, body, [class*=\"st-\"]  {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, p, span, label {
    color: white !important;
    text-align: center;
}

.stNumberInput label {
    display: none;
}

.card {
    background: rgba(0,0,0,0.75);
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 5px;
    border: 1px solid rgba(255,255,255,0.1);
    font-weight: bold;
    font-size: 1.1rem;
}

.price-tag {
    color: #ff2b2b !important;
    font-weight: 800;
    font-size: 1.2rem;
}

/* Estilo para los inputs */
input {
    background-color: rgba(255,255,255,0.1) !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ================== BASE DE DATOS ==================
file = "pedidos.csv"
if not os.path.exists(file):
    df = pd.DataFrame(columns=["Fecha", "Mesa", "Pedido", "Total", "Pago"])
    df.to_csv(file, index=False)

# ================== MENU ==================
menu = {
    "CUBA LIBRE": 150,
    "VODKA NARANJA": 150,
    "PRESIDENTE": 150,
    "ONE": 100,
    "HEINEKEN": 230,
    "REFRESCO": 60,
    "AGUA": 25,
    "HAMBURGER + PAPAS": 350,
    "HOT DOG": 200,
    "HOT DOG + PAPAS": 250
}

tab_menu, tab_admin = st.tabs(["🔥 MENU", "🔒 ADMIN"])

with tab_menu:
    st.title("🔥 YAMB CAFE MENU")
    mesa = st.text_input("Número de mesa", "1")

    carrito = []

    for item, precio in menu.items():
        col1, col2, col3 = st.columns([3,1,1])
        with col1:
            st.markdown(f"<div class='card'>{item}</div>", unsafe_allow_html=True)
        with col2:
            cantidad = st.number_input("", 0, 10, 0, key=item)
        with col3:
            st.markdown(f"<p class='price-tag'>RD${precio}</p>", unsafe_allow_html=True)

        if cantidad > 0:
            carrito.append((item, cantidad, precio))

    total = sum(c * p for _, c, p in carrito)
    st.markdown(f"## 💰 Total: RD${total}")

    if total > 0:
        pago = st.selectbox("Forma de pago", ["Efectivo", "Transferencia", "Tarjeta"])
        if st.button("CONFIRMAR PEDIDO", use_container_width=True, type="primary"):
            pedido_texto = ", ".join([f"{n} x{c}" for n,c,p in carrito])
            nuevo = pd.DataFrame([{
                "Fecha": datetime.now().strftime('%Y-%m-%d %H:%M'),
                "Mesa": mesa,
                "Pedido": pedido_texto,
                "Total": total,
                "Pago": pago
            }])
            nuevo.to_csv(file, mode='a', header=False, index=False)
            st.balloons()
            st.success("Pedido enviado 🔥")

with tab_admin:
    st.header("Panel de Control")
    clave = st.text_input("Clave de acceso", type="password")
    if clave == "yamb123":
        if os.path.exists(file):
            df_p = pd.read_csv(file)
            st.dataframe(df_p)
        else:
            st.info("No hay pedidos aún.")
