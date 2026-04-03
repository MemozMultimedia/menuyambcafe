import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# --- Configuración Inicial ---
logo_path = "Vector Smart Object.png"
file_pedidos = "pedidos.csv"
file_menu = "menu.csv"
columns_p = ["Fecha", "Mesa", "Cliente", "Pedido", "Total", "Categoria"]
ROLES_CONFIG = {"Comida": "1111", "Bebida": "2222", "Administrador General": "3333"}

if not os.path.exists(file_pedidos):
    pd.DataFrame(columns=columns_p).to_csv(file_pedidos, index=False)

st.set_page_config(page_title="Yamb Café | Menú Digital", layout="wide", page_icon="☕")

# --- CSS Adaptativo ---
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

    html, body, [class*='st-'] { font-family: 'Inter', sans-serif !important; }

    /* ELIMINAR ESPACIOS DE SOBRA */
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    header { visibility: hidden; height: 0; }
    footer { visibility: hidden; }

    /* LOGO REDUCIDO Y CENTRADO */
    .logo-container { display: flex; justify-content: center; align-items: center; width: 100%; padding: 10px 0; }
    .logo-img { max-width: 140px; width: 40%; height: auto; }

    @media (prefers-color-scheme: light) {
        .stApp { background-color: #ffffff !important; }
        p, label, span, div, .stMarkdown { color: #1e1e1e !important; }
        .product-card { background: white; border: 1px solid #f0f0f0; }
        .footer-premium { background: #f9f9f9; border-top: 1px solid #eee; }
    }

    @media (prefers-color-scheme: dark) {
        .stApp { background-color: #0e1117 !important; }
        p, label, span, div, .stMarkdown { color: #ffffff !important; }
        .product-card { background: #1e1e1e; border: 1px solid #333; }
        .footer-premium { background: #111111; border-top: 1px solid #333; }
    }

    .category-title { background: linear-gradient(135deg, #e63946 0%, #b91d1d 100%); color: white !important; padding: 12px; border-radius: 15px; text-align: center; margin: 25px 0; font-weight: 800; font-size: 1.5rem; text-transform: uppercase; }
    .product-card { border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; margin-bottom: 30px; overflow: hidden; }
    .product-img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-bottom: 1px solid #eee; }
    .product-price { color: #e63946 !important; font-weight: 800; font-size: 1.4rem; }

    /* PIE DE PAGINA */
    .footer-premium { padding: 40px 20px; border-radius: 30px 30px 0 0; margin-top: 20px; text-align: center; }
    .footer-brand { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 800; margin-bottom: 10px; }

    .whatsapp-float { position: fixed; width: 60px; height: 60px; bottom: 30px; right: 30px; background: #25d366; color: white !important; border-radius: 50px; display: flex; justify-content: center; align-items: center; font-size: 30px; z-index: 9999; box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
</style>""", unsafe_allow_html=True)

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

if 'auth_role' not in st.session_state: st.session_state.auth_role = None

@st.dialog("📝 Finalizar Orden")
def checkout_modal(carrito, mesa):
    with st.form("form_final"):
        nombre = st.text_input("Nombre Completo")
        cedula = st.text_input("Cédula / ID")
        if st.form_submit_button("ENVIAR PEDIDO AHORA", use_container_width=True):
            if nombre and cedula:
                for cat in ["Comida", "Bebida"]:
                    items = [f"{n} x{v[0]}" for n,v in carrito.items() if v[2] == cat]
                    if items:
                        subtotal = sum(v[0]*v[1] for n,v in carrito.items() if v[2] == cat)
                        pd.DataFrame([{ "Fecha": datetime.now().strftime("%H:%M"), "Mesa": mesa, "Cliente": nombre, "Pedido": ", ".join(items), "Total": subtotal, "Categoria": cat}]).to_csv(file_pedidos, mode="a", header=False, index=False)
                st.success("¡Pedido enviado!"); st.balloons(); st.rerun()

# --- NAVEGACIÓN ---
c_t1, c_t2 = st.columns([10, 1])
with c_t2:
    icon = "🔐" if st.session_state.auth_role is None else "📋"
    if st.button(icon):
        st.session_state.auth_role = "login" if st.session_state.auth_role is None else None
        st.rerun()

if st.session_state.auth_role is None:
    b64_logo = get_image_base64(logo_path)
    if b64_logo:
        st.markdown(f"<div class='logo-container'><img src='data:image/png;base64,{b64_logo}' class='logo-img'></div>", unsafe_allow_html=True)

    mesa = st.text_input("📍 Mesa", "1")
    carrito = {}
    df_menu = pd.read_csv(file_menu)

    for cat in ["Comida", "Bebida"]:
        st.markdown(f"<div class='category-title'>{'🍔' if cat=='Comida' else '🍹'} {cat.upper()}</div>", unsafe_allow_html=True)
        items = df_menu[df_menu['Categoria'] == cat]
        cols = st.columns(2)
        for i, row in enumerate(items.itertuples()):
            with cols[i % 2]:
                st.markdown(f"""<div class='product-card'><img src='{row.Imagen}' class='product-img'><div style='padding:15px;'><div style='font-weight:700;'>{row.Nombre}</div><div class='product-price'>RD${row.Precio}</div></div></div>""", unsafe_allow_html=True)
                if row.Disponible:
                    qty = st.number_input("Cantidad", 0, 20, key=f"q{row.Index}", label_visibility="collapsed")
                    if qty > 0: carrito[row.Nombre] = [qty, row.Precio, cat]
                else:
                    st.markdown("<div style='color:red;'>⚠️ No disponible</div>", unsafe_allow_html=True)

    if carrito:
        total = sum(v[0]*v[1] for v in carrito.values())
        if st.button(f"🛒 FINALIZAR PEDIDO - RD${total}", use_container_width=True): checkout_modal(carrito, mesa)

    st.markdown("""<div class='footer-premium'><div class='footer-brand'>☕ Yamb Café</div><div>Cada producto de <b>YAMB</b> apoya a jóvenes talentos en la música y el arte.</div><p style='margin-top:10px; font-size:0.8rem; font-weight:700; color:#e63946;'>Compra con propósito • Apoya el talento</p></div>""", unsafe_allow_html=True)

elif st.session_state.auth_role == "login":
    st.subheader("🔒 Acceso Administrativo")
    rol_sel = st.selectbox("Rol", ["Comida", "Bebida", "Administrador General"])
    pin = st.text_input("PIN", type="password")
    if st.button("Entrar"):
        if pin == ROLES_CONFIG.get(rol_sel): st.session_state.auth_role = rol_sel; st.rerun()
        else: st.error("PIN Incorrecto")

else:
    st.title(f"📊 Gestión: {st.session_state.auth_role}")
    df_m = pd.read_csv(file_menu)
    if st.session_state.auth_role == "Administrador General":
        st.subheader("Configuración del Menú")
        edited_df = st.data_editor(df_m, use_container_width=True)
        if st.button("💾 Guardar Cambios en Menú"):
            edited_df.to_csv(file_menu, index=False)
            st.success("Menú actualizado.")
        st.subheader("Historial de Ventas")
        st.dataframe(pd.read_csv(file_pedidos), use_container_width=True)
    else:
        st.subheader(f"Pedidos Pendientes: {st.session_state.auth_role}")
        peds = pd.read_csv(file_pedidos)
        st.dataframe(peds[peds['Categoria'] == st.session_state.auth_role], use_container_width=True)