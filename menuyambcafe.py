import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# --- Configuración Inicial ---
logo_path = "Vector Smart Object.png"
file_pedidos = "pedidos.csv"
file_menu = "menu.csv"
columns_p = ["Fecha", "Mesa", "Cliente", "Pedido", "Notas", "Total", "Categoria", "Estado"]
ROLES_CONFIG = {
    "Comida": "1111",
    "Bebida": "2222",
    "Administrador General": "3333"
}

if not os.path.exists(file_pedidos):
    pd.DataFrame(columns=columns_p).to_csv(file_pedidos, index=False)

st.set_page_config(page_title="Yamb Café | Menú Digital", layout="wide", page_icon="☕")

# --- CSS UI COMPACTA ---
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

    html, body, [class*='st-'], .stMarkdown, p, label, span, div { font-family: 'Inter', sans-serif !important; color: #1e1e1e !important; }
    .stApp { background-color: #f8f9fa; }
    .block-container { padding-top: 0.2rem !important; }
    header, footer { visibility: hidden; }

    /* LOGO MUCHO MÁS PEQUEÑO */
    .logo-container { display: flex; justify-content: center; align-items: center; width: 100%; padding: 2px 0; }
    .logo-img { max-width: 80px; width: 25%; height: auto; }

    /* BARRA DE SELECCION DE MESA */
    .mesa-ui-bar { 
        background: #ffffff; 
        padding: 10px 15px; 
        border-radius: 15px; 
        border: 2px solid #e63946; 
        margin-bottom: 20px; 
        box-shadow: 0 4px 10px rgba(230, 57, 70, 0.1);
    }

    .category-title { background: linear-gradient(135deg, #e63946 0%, #b91d1d 100%); color: white !important; padding: 10px; border-radius: 12px; text-align: center; margin: 15px 0; font-weight: 800; font-size: 1.2rem; text-transform: uppercase; }

    .product-card { background: white; border-radius: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.06); overflow: hidden; border: 1px solid #f0f0f0; margin-bottom: 12px; }
    .product-img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
    .product-info { padding: 8px; text-align: center; }
    .product-title { font-weight: 700; font-size: 1rem; margin-bottom: 2px; }
    .product-price { color: #e63946 !important; font-weight: 800; font-size: 1.1rem; }

    .qty-pill-container {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 5px !important;
        background: #f1f3f5;
        border-radius: 40px;
        padding: 2px 8px;
        width: 110px;
        margin: 5px auto !important;
        border: 1px solid #e9ecef;
    }

    .qty-display-text { font-weight: 800; font-size: 1.2rem; color: #495057; min-width: 20px; text-align: center; }

    div.stButton > button { background-color: transparent !important; border: none !important; color: #e63946 !important; padding: 0 !important; font-size: 1.5rem !important; width: 28px !important; height: 28px !important; }

    .footer-premium { background: #f9f9f9; padding: 40px 20px; border-radius: 40px 40px 0 0; margin-top: 40px; text-align: center; border-top: 1px solid #eee; }
    .footer-brand { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 800; margin-bottom: 10px; }
    .footer-text { color: #444; font-size: 1rem; }
    .footer-tagline { font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: #e63946; letter-spacing: 2px; padding-top: 10px; border-top: 1px solid #eee; display: inline-block; }

    .whatsapp-float { position: fixed; width: 65px; height: 65px; bottom: 20px; right: 20px; background: #25d366; color: white !important; border-radius: 50px; display: flex; justify-content: center; align-items: center; font-size: 28px; z-index: 9999; box-shadow: 0 8px 15px rgba(37, 211, 102, 0.3); }
</style>""", unsafe_allow_html=True)

def get_image_base64(path):
    if os.path.exists(path): return base64.b64encode(open(path, "rb").read()).decode()
    return ""

if 'carrito' not in st.session_state: st.session_state.carrito = {}
if 'auth_role' not in st.session_state: st.session_state.auth_role = None

@st.dialog("🛒 Resumen de tu Orden")
def checkout_modal(mesa):
    with st.form("form_final"):
        st.markdown("### Datos del Cliente")
        nombre = st.text_input("Nombre Completo")
        notas = st.text_area("Notas (Ej: Sin cebolla, etc.)")
        if st.form_submit_button("CONFIRMAR Y ENVIAR", use_container_width=True):
            if nombre:
                for cat in ["Comida", "Bebida"]:
                    items = [f"{v['name']} x{v['qty']}" for k,v in st.session_state.carrito.items() if v['cat'] == cat and v['qty'] > 0]
                    if items:
                        subtotal = sum(v['qty']*v['price'] for k,v in st.session_state.carrito.items() if v['cat'] == cat)
                        pd.DataFrame([{"Fecha": datetime.now().strftime("%H:%M"), "Mesa": mesa, "Cliente": nombre, "Pedido": ", ".join(items), "Notas": notas, "Total": subtotal, "Categoria": cat, "Estado": "Pendiente"}]).to_csv(file_pedidos, mode="a", header=False, index=False)
                st.session_state.carrito = {}
                st.success("¡Pedido enviado!"); st.balloons(); st.rerun()

c_t1, c_t2 = st.columns([10, 1])
with c_t2:
    icon = "🔐" if st.session_state.auth_role is None else "📋"
    if st.button(icon): st.session_state.auth_role = "login" if st.session_state.auth_role is None else None; st.rerun()

if st.session_state.auth_role is None:
    b64_logo = get_image_base64(logo_path)
    if b64_logo: st.markdown(f"<div class='logo-container'><img src='data:image/png;base64,{b64_logo}' class='logo-img'></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='mesa-ui-bar'>", unsafe_allow_html=True)
    mesa = st.selectbox("📍 Selecciona tu Mesa aquí", [str(i) for i in range(1, 21)], help="Elige el número de mesa donde te encuentras")
    st.markdown("</div>", unsafe_allow_html=True)

    if os.path.exists(file_menu):
        df_menu = pd.read_csv(file_menu)
        for cat in ["Comida", "Bebida"]:
            st.markdown(f"<div class='category-title'>{'🍔' if cat=='Comida' else '🍹'} {cat.upper()}</div>", unsafe_allow_html=True)
            items = df_menu[df_menu['Categoria'] == cat]
            cols = st.columns(2)
            for i, row in enumerate(items.itertuples()):
                with cols[i % 2]:
                    st.markdown(f"""<div class='product-card'>
                        <img src='{row.Imagen}' class='product-img'>
                        <div class='product-info'>
                            <div class='product-title'>{row.Nombre}</div>
                            <div class='product-price'>RD${row.Precio}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    item_key = f"item_{row.Index}"
                    if item_key not in st.session_state.carrito: st.session_state.carrito[item_key] = {'qty': 0, 'price': row.Precio, 'cat': cat, 'name': row.Nombre}
                    st.markdown("<div class='qty-pill-container'>", unsafe_allow_html=True)
                    q1, q2, q3 = st.columns([1, 1, 1])
                    with q1: 
                        if st.button("−", key=f"m_{row.Index}"):
                            st.session_state.carrito[item_key]['qty'] = max(0, st.session_state.carrito[item_key]['qty'] - 1); st.rerun()
                    with q2: st.markdown(f"<div class='qty-display-text'>{st.session_state.carrito[item_key]['qty']}</div>", unsafe_allow_html=True)
                    with q3:
                        if st.button("+", key=f"p_{row.Index}"): 
                            st.session_state.carrito[item_key]['qty'] += 1; st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
    total_final = sum(v['qty']*v['price'] for v in st.session_state.carrito.values())
    if total_final > 0:
        if st.button(f"🛒 FINALIZAR PEDIDO - RD${total_final}", use_container_width=True, type="primary"): checkout_modal(mesa)
    
    st.markdown("""<div class='footer-premium'>
        <div class='footer-brand'>☕ Yamb Café</div>
        <div class='footer-text'>Cada producto apoya a jóvenes talentos en la música y el arte.</div>
        <div class='footer-tagline'>Compra con propósito • Apoya el talento</div>
    </div>""", unsafe_allow_html=True)
else:
    st.title(f"📊 Panel {st.session_state.auth_role}")
    if os.path.exists(file_pedidos): st.data_editor(pd.read_csv(file_pedidos), use_container_width=True)
