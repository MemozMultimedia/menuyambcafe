import streamlit as st
import pandas as pd
from datetime import datetime
import os

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
ORDERS_FILE = 'pedidos.csv'

def init_db():
    if not os.path.exists(ORDERS_FILE):
        pd.DataFrame(columns=['Fecha', 'Cliente', 'Cedula', 'Mesa', 'Pedido', 'Total', 'Status']).to_csv(ORDERS_FILE, index=False)

init_db()

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

if modo == 'Menú y Pedidos':
    st.title('🍽️ Carta Digital')
    mesa = st.sidebar.text_input('Tu Mesa', '1')

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
        else:
            st.session_state['confirmando'] = True

    if st.session_state.get('confirmando'):
        st.divider()
        st.subheader("📝 Datos para el Pedido")
        nombre_cliente = st.text_input("Nombre Completo")
        cedula_cliente = st.text_input("Número de Cédula")
        
        if st.button("Finalizar y Enviar"):
            if nombre_cliente and cedula_cliente:
                p_str = ', '.join([f"{i['name']} x{i['q']}" for i in carrito])
                nuevo_pedido = pd.DataFrame([[datetime.now().strftime('%H:%M'), nombre_cliente, cedula_cliente, mesa, p_str, total, 'Pendiente']],
                                         columns=['Fecha', 'Cliente', 'Cedula', 'Mesa', 'Pedido', 'Total', 'Status'])
                nuevo_pedido.to_csv(ORDERS_FILE, mode='a', header=False, index=False)
                st.balloons()
                st.success(f'✅ ¡Gracias {nombre_cliente}! Su pedido se ha tomado y se le notificará cuando esté listo.')
                st.session_state['confirmando'] = False
            else:
                st.warning("Por favor completa tu nombre y cédula.")

elif modo == 'Panel Admin':
    st.header('📊 Recibidor de Pedidos')
    if os.path.exists(ORDERS_FILE):
        df = pd.read_csv(ORDERS_FILE)
        st.dataframe(df.sort_values(by='Fecha', ascending=False), use_container_width=True)
