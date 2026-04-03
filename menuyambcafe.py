import streamlit as st
import pandas as pd
import os
from datetime import datetime

logo_path = 'Vector Smart Object.png'
file = 'pedidos.csv'

if not os.path.exists(file):
    pd.DataFrame(columns=['Fecha', 'Mesa', 'Cliente', 'Pedido', 'Total', 'Categoria']).to_csv(file, index=False)

st.set_page_config(page_title='Yamb Café | Menú Digital', layout='wide')

# --- CSS ---
st.markdown("""<style>
    .stApp { background-color: #ffffff; }
    .category-header { background-color: #e63946; color: white !important; padding: 15px; border-radius: 10px; text-align: center; margin: 30px 0 20px 0; font-size: 1.8rem; font-weight: bold; }
    .product-card { background: white; border: 1px solid #f0f0f0; border-radius: 15px; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px; }
    .footer-text { text-align: center; color: #1e1e1e; margin-top: 50px; padding: 20px; border-top: 1px solid #eee; font-style: italic; }
</style>""", unsafe_allow_html=True)

@st.dialog("📝 Finalizar Pedido")
def confirmar_pedido_modal(carrito, mesa):
    st.write("Datos del cliente:")
    with st.form("form_datos"):
        nombre = st.text_input("Nombre")
        cedula = st.text_input("Cédula")
        if st.form_submit_button("CONFIRMAR", use_container_width=True):
            if nombre and cedula:
                # Separar pedidos por categoría para los admins
                for cat in ['Comida', 'Bebida']:
                    items_cat = [f"{n} x{v[0]}" for n,v in carrito.items() if v[2] == cat]
                    if items_cat:
                        subtotal = sum(v[0]*v[1] for n,v in carrito.items() if v[2] == cat)
                        nuevo = pd.DataFrame([{
                            'Fecha': datetime.now().strftime('%H:%M:%S'),
                            'Mesa': mesa, 'Cliente': nombre, 'Pedido': ", ".join(items_cat),
                            'Total': subtotal, 'Categoria': cat
                        }])
                        nuevo.to_csv(file, mode='a', header=False, index=False)
                st.success("✅ Pedido enviado!")
                st.balloons()
                st.rerun()

tab_menu, tab_admin = st.tabs(['📋 MENÚ', '🔒 ADMINISTRACIÓN'])

with tab_menu:
    st.markdown("<h1 style='text-align: center;'>YAMB CAFÉ</h1>", unsafe_allow_html=True)
    mesa = st.text_input("Mesa", "1")
    carrito = {}

    st.markdown("<div class='category-header'>🍔 COMIDA</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        q1 = st.number_input("Burguer + Papas (RD$350)", 0, 10, key="f1")
        if q1 > 0: carrito["Burguer"] = [q1, 350, "Comida"]
    with c2:
        q2 = st.number_input("Hot Dog (RD$250)", 0, 10, key="f2")
        if q2 > 0: carrito["Hot Dog"] = [q2, 250, "Comida"]

    st.markdown("<div class='category-header'>☕ BEBIDA</div>", unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        q3 = st.number_input("Cappuccino (RD$180)", 0, 10, key="b1")
        if q3 > 0: carrito["Cappuccino"] = [q3, 180, "Bebida"]
    with b2:
        q4 = st.number_input("Cerveza (RD$150)", 0, 10, key="b2")
        if q4 > 0: carrito["Cerveza"] = [q4, 150, "Bebida"]

    if carrito and st.button("ORDENAR AHORA", use_container_width=True, type='primary'):
        confirmar_pedido_modal(carrito, mesa)

with tab_admin:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👨‍🍳 Cocina")
        if st.text_input("Clave Cocina", type="password") == "yamb123":
            df = pd.read_csv(file)
            st.dataframe(df[df['Categoria'] == 'Comida'])
    with col2:
        st.subheader("🍸 Bar")
        if st.text_input("Clave Bar", type="password") == "yamb456":
            df = pd.read_csv(file)
            st.dataframe(df[df['Categoria'] == 'Bebida'])
