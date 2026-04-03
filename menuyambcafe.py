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

# --- CSS UI AVANZADA ---
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    html, body, [class*='st-'] { font-family: 'Inter', sans-serif !important; }
    .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; }
    header, footer { visibility: hidden; }

    .stApp { background-color: #f8f9fa; color: #1e1e1e; }

    .category-title {
        background: linear-gradient(135deg, #e63946 0%, #b91d1d 100%);
        color: white !important; padding: 14px; border-radius: 12px; text-align: center; margin: 25px 0;
        font-weight: 800; font-size: 1.4rem; text-transform: uppercase;
    }

    .product-card {
        background: white; border-radius: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.06);
        overflow: hidden; border: 1px solid #f0f0f0; margin-bottom: 20px;
    }

    .product-img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
    .product-info { padding: 12px; text-align: center; }
    .product-title { font-weight: 700; font-size: 1.1rem; margin-bottom: 4px; }
    .product-price { color: #e63946 !important; font-weight: 800; font-size: 1.2rem; }

    /* CENTERED HORIZONTAL PILL SELECTOR */
    .qty-pill-container {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 15px !important;
        background: #f1f3f5;
        border-radius: 40px;
        padding: 5px 15px;
        width: 140px;
        margin: 10px auto !important;
        border: 1px solid #e9ecef;
    }

    .qty-display-text {
        font-weight: 800;
        font-size: 1.4rem;
        color: #495057;
        min-width: 25px;
        text-align: center;
    }

    div.stButton > button {
        background-color: transparent !important;
        border: none !important;
        color: #e63946 !important;
        padding: 0 !important;
        font-size: 1.8rem !important;
        width: 35px !important;
        height: 35px !important;
    }

    .footer-premium { padding: 40px 20px; border-radius: 30px 30px 0 0; margin-top: 50px; text-align: center; background: #fff; border-top: 1px solid #eee; }
    .whatsapp-float { position: fixed; width: 60px; height: 60px; bottom: 25px; right: 25px; background: #25d366; color: white !important; border-radius: 50px; display: flex; justify-content: center; align-items: center; font-size: 30px; z-index: 9999; box-shadow: 0 8px 15px rgba(37, 211, 102, 0.3); }
    
    /* Grid Responsive: 2 col desktop, 1 col mobile */
    [data-testid="stHorizontalBlock"] { gap: 1rem; }
</style>""", unsafe_allow_html=True)

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
    if os.path.exists(logo_path): st.image(logo_path, width=160)
    mesa = st.text_input("📍 Mesa", "1")
    if os.path.exists(file_menu):
        df_menu = pd.read_csv(file_menu)
        for cat in ["Comida", "Bebida"]:
            st.markdown(f"<div class='category-title'>{'🍔' if cat=='Comida' else '🍹'} {cat.upper()}</div>", unsafe_allow_html=True)
            items = df_menu[df_menu['Categoria'] == cat]
            
            # Logic for Responsive Grid (2 columns on Desktop, handled by Streamlit naturally in wide mode)
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

                    # CENTERED PILL SELECTOR
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

    st.markdown("""<div class='footer-premium'>☕ Yamb Café<br><small>Apoya a jóvenes talentos</small></div>""", unsafe_allow_html=True)

elif st.session_state.auth_role == "login":
    rol_sel = st.selectbox("Rol", ["Comida", "Bebida", "Administrador General"])
    pin = st.text_input("PIN", type="password")
    if st.button("Entrar", use_container_width=True):
        if pin == ROLES_CONFIG.get(rol_sel): st.session_state.auth_role = rol_sel; st.rerun()
        else: st.error("PIN Incorrecto")
else:
    st.title(f"📊 Panel {st.session_state.auth_role}")
    if os.path.exists(file_pedidos): st.data_editor(pd.read_csv(file_pedidos), use_container_width=True)
