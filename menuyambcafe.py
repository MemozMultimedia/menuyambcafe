import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# --- Configuración Inicial ---
logo_path = "Vector Smart Object.png"
file = "pedidos.csv"
whatsapp_number = "1234567890"
columns = ["Fecha", "Mesa", "Cliente", "Pedido", "Total", "Categoria"]

ROLES_CONFIG = {
    "Comida": "1111",
    "Bebida": "2222",
    "Administrador General": "3333"
}

if not os.path.exists(file):
    pd.DataFrame(columns=columns).to_csv(file, index=False)

st.set_page_config(page_title="Yamb Café | Menú Digital", layout="wide", page_icon="☕")

# --- Estilos CSS ---
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    html, body, [class*='st-'], .stMarkdown, p, label, span, div { font-family: 'Inter', sans-serif !important; color: #1e1e1e !important; }
    .stApp { background-color: #ffffff !important; }
    [data-testid="stSidebar"] { display: none; }
    .block-container { padding-top: 1.5rem; }
    .category-title { background: linear-gradient(135deg, #e63946 0%, #b91d1d 100%); color: white !important; padding: 15px; border-radius: 15px; text-align: center; margin: 30px 0 20px 0; font-weight: 800; font-size: 1.6rem; text-transform: uppercase; }
    .product-card { background: white; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.07); text-align: center; margin-bottom: 30px; border: 1px solid #f0f0f0; overflow: hidden; }
    .product-img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-bottom: 1px solid #eee; }
    .product-info { padding: 15px; }
    .product-name { font-weight: 700; font-size: 1.2rem; min-height: 2.5em; display: flex; align-items: center; justify-content: center; }
    .product-price { color: #e63946 !important; font-weight: 800; font-size: 1.4rem; }
    .footer-premium { background: #f9f9f9; padding: 60px 20px; border-radius: 40px 40px 0 0; margin-top: 80px; text-align: center; border-top: 1px solid #eee; }
    .footer-brand { font-family: 'Playfair Display', serif; font-size: 2.2rem; font-weight: 800; margin-bottom: 15px; }
    .whatsapp-float { position: fixed; width: 65px; height: 65px; bottom: 30px; right: 30px; background: #25d366; color: white !important; border-radius: 50px; display: flex; justify-content: center; align-items: center; font-size: 32px; z-index: 9999; box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
</style>""", unsafe_allow_html=True)

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

if 'auth_role' not in st.session_state: st.session_state.auth_role = None

whatsapp_link = f"https://wa.me/{whatsapp_number}"
st.markdown(f"""<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'><a href='{whatsapp_link}' class='whatsapp-float' target='_blank'><i class='fab fa-whatsapp'></i></a>""", unsafe_allow_html=True)

# Navigation Toggle
c_t1, c_t2 = st.columns([10, 1])
with c_t2:
    if st.session_state.auth_role is None:
        if st.button("🔐"): st.session_state.auth_role = "login"; st.rerun()
    else:
        if st.button("📋"): st.session_state.auth_role = None; st.rerun()

@st.dialog("📝 Finalizar Orden")
def checkout_modal(carrito, mesa):
    st.markdown("### Datos del Cliente")
    with st.form("form_final"):
        nombre = st.text_input("Nombre Completo")
        cedula = st.text_input("Cédula / ID")
        if st.form_submit_button("ENVIAR PEDIDO AHORA", use_container_width=True):
            if nombre and cedula:
                for cat in ["Comida", "Bebida"]:
                    items = [f"{n} x{v[0]}" for n,v in carrito.items() if v[2] == cat]
                    if items:
                        subtotal = sum(v[0]*v[1] for n,v in carrito.items() if v[2] == cat)
                        pd.DataFrame([{"Fecha": datetime.now().strftime("%H:%M"), "Mesa": mesa, "Cliente": nombre, "Pedido": ", ".join(items), "Total": subtotal, "Categoria": cat}]).to_csv(file, mode="a", header=False, index=False)
                st.success("¡Pedido enviado!"); st.balloons(); st.rerun()

if st.session_state.auth_role is None:
    b64_logo = get_image_base64(logo_path)
    if b64_logo: st.markdown(f"<center><img src='data:image/png;base64,{b64_logo}' width=220></center>", unsafe_allow_html=True)

    mesa = st.text_input("📍 Mesa", "1")
    carrito = {}

    st.markdown("<div class='category-title'>🍔 COMIDA</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    items_c = [("Hamburguer + papas fritas", 350, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600", "c1"), ("Hot Dog", 200, "https://images.unsplash.com/photo-1541214113241-21578d2d9b62?w=600", "c2"), ("Hot Dog + papas fritas", 250, "https://images.unsplash.com/photo-1612392062631-94dd858cba88?w=600", "c3")]
    for i, (name, price, img, k) in enumerate(items_c):
        with [col1, col2][i % 2]:
            st.markdown(f"""<div class='product-card'><img src='https://images.unsplash.com/photo-1518173946687-a4c8892bbd9f?w=400' class='product-img'><div class='product-info'><div class='product-name'>Cerveza Fría</div><div class='product-price'>RD$150</div></div></div>""", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 20, key=k, label_visibility="collapsed")
            if qty > 0: carrito[name] = [qty, price, "Comida"]

    st.markdown("<div class='category-title'>🍹 BEBIDAS</div>", unsafe_allow_html=True)
    bcol1, bcol2 = st.columns(2)
    items_b = [("Cuba Libre (ron con Coca Cola)", 150, "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=600", "b1"), ("Vodka con jugo de naranja", 150, "https://images.unsplash.com/photo-1536935338788-846bb9981813?w=600", "b2"), ("Cerveza Presidente pequeña", 150, "https://images.unsplash.com/photo-1618885472179-5e474019f2a9?w=600", "b3"), ("Cerveza One", 100, "https://images.unsplash.com/photo-1584225064785-c62a8b43d148?w=600", "b4"), ("Cerveza Heineken mediana", 230, "https://images.unsplash.com/photo-1613215049641-81495014a582?w=600", "b5"), ("Refresco", 60, "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=600", "b6"), ("Agua", 25, "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=600", "b7")]
    for i, (name, price, img, k) in enumerate(items_b):
        with [bcol1, bcol2][i % 2]:
            st.markdown(f"""<div class='product-card'><img src='https://images.unsplash.com/photo-1518173946687-a4c8892bbd9f?w=400' class='product-img'><div class='product-info'><div class='product-name'>Cerveza Fría</div><div class='product-price'>RD$150</div></div></div>""", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 20, key=k, label_visibility="collapsed")
            if qty > 0: carrito[name] = [qty, price, "Bebida"]

    if carrito:
        total = sum(v[0]*v[1] for v in carrito.values())
        if st.button(f"🛒 FINALIZAR PEDIDO - RD${total}", use_container_width=True): checkout_modal(carrito, mesa)

    st.markdown("""<div class='footer-premium'><div class='footer-brand'>☕ Yamb Café</div><div>Cada producto de <b>YAMB</b> apoya a jóvenes talentos en la música y el arte.</div><p style='margin-top:15px; font-size:0.9rem; font-weight:700; color:#e63946;'>Compra con propósito • Apoya el talento</p></div>""", unsafe_allow_html=True)

elif st.session_state.auth_role == "login":
    st.markdown("<br><div class='admin-container'>", unsafe_allow_html=True)
    st.subheader("🔒 Acceso Personal")
    rol_sel = st.selectbox("Rol", ["Comida", "Bebida", "Administrador General"])
    pin = st.text_input("PIN", type="password")
    if st.button("Entrar", use_container_width=True):
        if pin == ROLES_CONFIG.get(rol_sel): st.session_state.auth_role = rol_sel; st.rerun()
        else: st.error("PIN incorrecto")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.title(f"📊 Panel: {st.session_state.auth_role}")
    df_adm = pd.read_csv(file) if os.path.exists(file) else pd.DataFrame(columns=columns)
    if st.session_state.auth_role == "Administrador General":
        st.metric("Ventas Totales", f"RD${df_adm['Total'].sum():,.2f}")
    st.dataframe(df_adm, use_container_width=True)