import streamlit as st
import os

logo_path = 'Vector Smart Object.png'

st.set_page_config(page_title='Yamb Café | Menú', layout='wide')

# CSS para diseño limpio y contraste
st.markdown("""<style>
    .stApp { background-color: #ffffff; }
    .category-header { color: #e63946; border-bottom: 2px solid #e63946; padding-top: 20px; font-weight: bold; }
    .menu-card { background: #f9f9f9; border-radius: 10px; padding: 15px; margin-bottom: 10px; border: 1px solid #eee; text-align: center; }
</style>""", unsafe_allow_html=True)

tab_menu, tab_admin = st.tabs(['📋 MENÚ', '🔒 ADMIN'])

with tab_menu:
    if os.path.exists(logo_path): st.image(logo_path, width=150)
    st.title("Menú Yamb Café")
    mesa = st.text_input("Mesa", "1")

    # SECCIÓN 1: COMIDA
    st.markdown("<h2 class='category-header'>🍔 COMIDAS</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='menu-card'><b>Burguer + Papas</b><br>RD$350</div>", unsafe_allow_html=True)
        st.number_input("Cant.", 0, 10, key="f1")
    with c2:
        st.markdown("<div class='menu-card'><b>Hot Dog Especial</b><br>RD$250</div>", unsafe_allow_html=True)
        st.number_input("Cant.", 0, 10, key="f2")
    with c3:
        st.markdown("<div class='menu-card'><b>Pizza Personal</b><br>RD$300</div>", unsafe_allow_html=True)
        st.number_input("Cant.", 0, 10, key="f3")

    # SECCIÓN 2: BEBIDA
    st.markdown("<h2 class='category-header'>☕ BEBIDAS</h2>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown("<div class='menu-card'><b>Café / Cappuccino</b><br>RD$180</div>", unsafe_allow_html=True)
        st.number_input("Cant.", 0, 10, key="b1")
    with b2:
        st.markdown("<div class='menu-card'><b>Cerveza</b><br>RD$150</div>", unsafe_allow_html=True)
        st.number_input("Cant.", 0, 10, key="b2")
    with b3:
        st.markdown("<div class='menu-card'><b>Cócteles</b><br>RD$150</div>", unsafe_allow_html=True)
        st.number_input("Cant.", 0, 10, key="b3")

    if st.button("CONFIRMAR PEDIDO", use_container_width=True):
        st.success("¡Pedido enviado!")

with tab_admin:
    st.subheader("Acceso restringido")
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("Cocina")
        st.text_input("User", key="u1")
        st.text_input("Pass", type="password", key="p1")
    with col_b:
        st.info("Bar")
        st.text_input("User", key="u2")
        st.text_input("Pass", type="password", key="p2")
