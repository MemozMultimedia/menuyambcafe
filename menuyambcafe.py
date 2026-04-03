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

# --- Estilos CSS Ultra-Visibilidad (Texto Blanco sobre Fondo Negro) ---
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

    /* FUERZA COLOR BLANCO EN TODO EL APP POR SOLICITUD DEL USUARIO */
    html, body, [class*='st-'], .stMarkdown, p, label, span, div, li, input, button, select {
        font-family: 'Inter', sans-serif !important;
        color: #ffffff !important;
    }

    .stApp { background-color: #000000 !important; }
    [data-testid="stSidebar"] { display: none; }
    
    /* REDUCCIÓN DE ESPACIO SUPERIOR */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem; }

    /* SELECTOR DE ADMINISTRADORES */
    div[data-baseweb="select"] * {
        color: #ffffff !important;
        background-color: #333333 !important;
    }

    div[data-baseweb="select"] {
        border: 2px solid #ffffff !important;
        border-radius: 10px !important;
    }

    .category-title {
        background: linear-gradient(135deg, #e63946 0%, #b91d1d 100%);
        color: white !important;
        padding: 15px; border-radius: 15px; text-align: center; margin: 30px 0 20px 0;
        font-weight: 800; font-size: 1.6rem; text-transform: uppercase;
    }

    .product-card {
        background: #1e1e1e; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        text-align: center; margin-bottom: 30px; border: 1px solid #333; overflow: hidden;
    }

    .product-img { width: 100%; height: 220px; object-fit: cover; }
    .product-info { padding: 15px; }
    .product-name { color: #ffffff !important; font-weight: 700; font-size: 1.2rem; min-height: 2.5em; display: flex; align-items: center; justify-content: center; }
    .product-price { color: #e63946 !important; font-weight: 800; font-size: 1.4rem; }

    .footer-premium {
        background: #111111; padding: 60px 20px; border-radius: 40px 40px 0 0;
        margin-top: 80px; text-align: center; border-top: 1px solid #333;
    }

    .whatsapp-float {
        position: fixed; width: 65px; height: 65px; bottom: 30px; right: 30px;
        background: #25d366; color: white !important; border-radius: 50px;
        display: flex; justify-content: center; align-items: center; font-size: 32px; z-index: 9999;
    }

    .admin-box { 
        max-width: 500px; 
        margin: 0 auto; 
        padding: 40px; 
        background: #1e1e1e; 
        border-radius: 20px; 
        border: 1px solid #444444; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.5); 
    }
</style>""", unsafe_allow_html=True)

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

if 'auth_role' not in st.session_state: st.session_state.auth_role = None

whatsapp_link = f"https://wa.me/{whatsapp_number}?text=Hola!%20Vengo%20desde%20el%20menu%20digital."
st.markdown(f"""<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'><a href='{whatsapp_link}' class='whatsapp-float' target='_blank'><i class='fab fa-whatsapp'></i></a>""", unsafe_allow_html=True)

c_t1, c_t2 = st.columns([10, 1])
with c_t2:
    if st.session_state.auth_role is None:
        if st.button("🔐", help="Panel Admin"): st.session_state.auth_role = "login"; st.rerun()
    else:
        if st.button("📋", help="Volver al Menú"): st.session_state.auth_role = None; st.rerun()

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
    if b64_logo: st.markdown(f"<center><img src='data:image/png;base64,{b64_logo}' width='220'></center>", unsafe_allow_html=True)

    mesa = st.text_input("📍 Número de Mesa", "1")
    carrito = {}

    st.markdown("<div class='category-title'>🍔 COMIDA</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    items_c = [("Hamburguer + papas", 350, "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600", "c1"), ("Hot Dog Especial", 250, "https://images.unsplash.com/photo-1541214113241-21578d2d9b62?w=600", "c2")]
    for col, (name, price, img, k) in zip([col1, col2], items_c):
        with col:
            st.markdown(f"<div class='product-card'><img src='{img}' class='product-img'><div class='product-info'><p class='product-name'>{name}</p><p class='product-price'>RD${price}</p></div></div>", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 10, key=k)
            if qty > 0: carrito[name] = [qty, price, "Comida"]

    st.markdown("<div class='category-title'>🍹 BEBIDAS</div>", unsafe_allow_html=True)
    bcol1, bcol2 = st.columns(2)
    items_b = [("Cuba Libre", 150, "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=600", "b1"), ("Cerveza Fria", 150, "https://images.unsplash.com/photo-1618885472179-5e474019f2a9?w=600", "b2")]
    for col, (name, price, img, k) in zip([bcol1, bcol2], items_b):
        with col:
            st.markdown(f"<div class='product-card'><img src='{img}' class='product-img'><div class='product-info'><p class='product-name'>{name}</p><p class='product-price'>RD${price}</p></div></div>", unsafe_allow_html=True)
            qty = st.number_input("Cantidad", 0, 10, key=k)
            if qty > 0: carrito[name] = [qty, price, "Bebida"]

    if carrito:
        total = sum(v[0]*v[1] for v in carrito.values())
        if st.button(f"🛒 VER RESUMEN - RD${total}", use_container_width=True): checkout_modal(carrito, mesa)

    st.markdown("""<div class='footer-premium'><div class='footer-brand'>☕ Yamb Café</div><div class='footer-text'>Cada producto de <b>YAMB</b> apoya a jóvenes talentos en la música y el arte.</div></div>""", unsafe_allow_html=True)

elif st.session_state.auth_role == "login":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='admin-box'>", unsafe_allow_html=True)
    st.subheader("🔒 Acceso Administrativo")
    rol_sel = st.selectbox("Seleccione su Rol", ["Comida", "Bebida", "Administrador General"])
    pin = st.text_input("PIN de seguridad", type="password")
    if st.button("Ingresar Ahora", use_container_width=True):
        if pin == ROLES_CONFIG.get(rol_sel):
            st.session_state.auth_role = rol_sel; st.rerun()
        else: st.error("Clave incorrecta")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.title(f"📊 Panel: {st.session_state.auth_role}")
    df_adm = pd.read_csv(file) if os.path.exists(file) else pd.DataFrame(columns=columns)
    if st.session_state.auth_role == "Administrador General":
        t1, t2 = st.tabs(["💰 Contabilidad", "📋 Historial"])
        with t1:
            st.metric("Ventas Totales", f"RD${df_adm['Total'].sum():,.2f}")
            if not df_adm.empty: st.bar_chart(df_agg_total = df_adm.groupby('Categoria')['Total'].sum())
        with t2: st.dataframe(df_adm, use_container_width=True)
    else:
        st.dataframe(df_adm[df_adm['Categoria'] == st.session_state.auth_role], use_container_width=True)