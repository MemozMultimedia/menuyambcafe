import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# --- Configuración Inicial ---
logo_path = "Vector Smart Object.png"
file_pedidos = "pedidos.csv"
file_menu = "menu.csv"
columns_p = ["Fecha", "Mesa", "Cliente", "Pedido", "Total", "Categoria", "Estado"]
ROLES_CONFIG = {"Comida": "1111", "Bebida": "2222", "Administrador General": "3333"}

if not os.path.exists(file_pedidos):
    pd.DataFrame(columns=columns_p).to_csv(file_pedidos, index=False)

st.set_page_config(page_title="Yamb Café | Menú Digital", layout="wide", page_icon="☕")

# --- CSS Mejorado para Alineación de Selector ---
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

    html, body, [class*='st-'] { font-family: 'Inter', sans-serif !important; }
    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
    header { visibility: hidden; height: 0; }
    footer { visibility: hidden; }

    .stApp { background-color: white; color: #1e1e1e; }

    .logo-container { display: flex; justify-content: center; align-items: center; width: 100%; padding: 15px 0; }
    .logo-img { max-width: 140px; width: 45%; height: auto; }

    .category-title {
        background: linear-gradient(135deg, #e63946 0%, #b91d1d 100%);
        color: white !important; padding: 12px; border-radius: 15px; text-align: center; margin: 30px 0 20px 0;
        font-weight: 800; font-size: 1.5rem; text-transform: uppercase;
    }

    .product-card {
        background: white; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); 
        margin-bottom: 25px; overflow: hidden; border: 1px solid #eee;
        display: flex; flex-direction: column;
    }
    .product-img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
    .product-info { padding: 15px; text-align: center; flex-grow: 1; }
    .product-title { font-weight: 800; font-size: 1.2rem; min-height: 3em; margin-bottom: 5px; }
    .product-price { color: #e63946 !important; font-weight: 800; font-size: 1.3rem; margin-bottom: 10px; }

    /* --- ÁREA DEL SELECTOR ORGANIZADA --- */
    .selector-container {
        background: #fcfcfc; border-top: 1px solid #eee; padding: 10px;
    }
    
    [data-testid="column"] {
        width: calc(33% - 5px) !important; flex: 1 1 calc(33% - 5px) !important; min-width: calc(33% - 5px) !important;
    }

    div[data-testid="stHorizontalBlock"] {
        flex-direction: row !important; display: flex !important; flex-wrap: nowrap !important; align-items: center !important;
    }

    .stButton > button { 
        width: 100% !important; border-radius: 8px !important; height: 40px !important; 
        border: 1px solid #ddd !important; background: white !important; color: black !important;
    }

    .qty-text { text-align: center; font-weight: 800; font-size: 1.2rem; margin: 0; pointer-events: none; }

    .footer-premium { padding: 40px 20px; border-radius: 40px 40px 0 0; margin-top: 30px; text-align: center; background: #f9f9f9; border-top: 1px solid #eee; }
    .whatsapp-float { position: fixed; width: 60px; height: 60px; bottom: 20px; right: 20px; background: #25d366; color: white !important; border-radius: 50px; display: flex; justify-content: center; align-items: center; font-size: 30px; z-index: 9999; box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
</style>""", unsafe_allow_html=True)

def get_image_base64(path):
    if os.path.exists(path): 
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

if 'carrito' not in st.session_state: st.session_state.carrito = {}
if 'auth_role' not in st.session_state: st.session_state.auth_role = None

@st.dialog("📝 Finalizar Orden")
def checkout_modal(mesa):
    with st.form("form_final"):
        st.subheader("Datos del Cliente")
        nombre = st.text_input("Nombre Completo")
        cedula = st.text_input("Cédula / ID")
        if st.form_submit_button("ENVIAR PEDIDO AHORA", use_container_width=True):
            if nombre and cedula:
                for cat in ["Comida", "Bebida"]:
                    items = [f"{n} x{v['qty']}" for n,v in st.session_state.carrito.items() if v['cat'] == cat and v['qty'] > 0]
                    if items:
                        subtotal = sum(v['qty']*v['price'] for n,v in st.session_state.carrito.items() if v['cat'] == cat)
                        pd.DataFrame([{"Fecha": datetime.now().strftime("%H:%M"), "Mesa": mesa, "Cliente": nombre, "Pedido": ", ".join(items), "Total": subtotal, "Categoria": cat, "Estado": "Pendiente"}]).to_csv(file_pedidos, mode="a", header=False, index=False)
                st.session_state.carrito = {}
                st.success("¡Gracias por elegirnos!"); st.balloons(); st.rerun()

c_t1, c_t2 = st.columns([10, 1])
with c_t2:
    icon = "🔐" if st.session_state.auth_role is None else "📋"
    if st.button(icon):
        st.session_state.auth_role = "login" if st.session_state.auth_role is None else None
        st.rerun()

if st.session_state.auth_role is None:
    b64_logo = get_image_base64(logo_path)
    if b64_logo: st.markdown(f"<div class='logo-container'><img src='data:image/png;base64,{b64_logo}' class='logo-img'></div>", unsafe_allow_html=True)

    mesa = st.text_input("📍 Número de Mesa", "1")

    if os.path.exists(file_menu):
        df_menu = pd.read_csv(file_menu)
        df_menu = df_menu.sort_values(by=['Categoria', 'Nombre'], ascending=[False, True])
        
        for cat in ["Comida", "Bebida"]:
            st.markdown(f"<div class='category-title'>{'🍔' if cat=='Comida' else '🍹'} {cat.upper()}</div>", unsafe_allow_html=True)
            items = df_menu[df_menu['Categoria'] == cat]
            cols = st.columns(2)
            for i, row in enumerate(items.itertuples()):
                with cols[i % 2]:
                    # Estructura de tarjeta con área de selector separada
                    st.markdown(f"""<div class='product-card'>
                        <img src='{row.Imagen}' class='product-img'>
                        <div class='product-info'>
                            <div class='product-title'>{row.Nombre}</div>
                            <div class='product-price'>RD${row.Precio}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                    
                    if row.Disponible:
                        item_key = f"item_{row.Index}"
                        if item_key not in st.session_state.carrito: st.session_state.carrito[item_key] = {'qty': 0, 'price': row.Precio, 'cat': cat, 'name': row.Nombre}
                        
                        with st.container():
                            st.markdown("<div class='selector-container'>", unsafe_allow_html=True)
                            q1, q2, q3 = st.columns([1,1,1])
                            with q1: 
                                if st.button("➖", key=f"min_{row.Index}"): 
                                    st.session_state.carrito[item_key]['qty'] = max(0, st.session_state.carrito[item_key]['qty'] - 1)
                                    st.rerun()
                            with q2: st.markdown(f"<p class='qty-text'>{st.session_state.carrito[item_key]['qty']}</p>", unsafe_allow_html=True)
                            with q3: 
                                if st.button("➕", key=f"plus_{row.Index}"): 
                                    st.session_state.carrito[item_key]['qty'] += 1
                                    st.rerun()
                            st.markdown("</div>", unsafe_allow_html=True)
                    else: st.error("Agotado")

    total_final = sum(v['qty']*v['price'] for v in st.session_state.carrito.values())
    if total_final > 0:
        if st.button(f"🛒 FINALIZAR PEDIDO - RD${total_final}", use_container_width=True, type="primary"):
            checkout_modal(mesa)

    st.markdown("""<div class='footer-premium'><div class='footer-brand'>☕ Yamb Café</div><div>Cada producto de <b>YAMB</b> apoya a jóvenes talentos en la música y el arte.</div><div class='footer-tagline'>Compra con propósito • Apoya el talento</div></div>""", unsafe_allow_html=True)

elif st.session_state.auth_role == "login":
    st.subheader("🔒 Acceso Administrativo")
    rol_sel = st.selectbox("Rol", ["Comida", "Bebida", "Administrador General"])
    pin = st.text_input("PIN", type="password")
    if st.button("Entrar", use_container_width=True):
        if pin == ROLES_CONFIG.get(rol_sel): st.session_state.auth_role = rol_sel; st.rerun()
        else: st.error("PIN Incorrecto")
else:
    st.title(f"📊 Gestión: {st.session_state.auth_role}")
    df_p = pd.read_csv(file_pedidos)
    if st.session_state.auth_role == "Administrador General":
        st.data_editor(df_p, use_container_width=True, hide_index=True)
    else:
        mask = (df_p['Categoria'] == st.session_state.auth_role)
        filtered = df_p[mask]
        edited = st.data_editor(filtered, use_container_width=True, disabled=["Fecha", "Mesa", "Cliente", "Pedido", "Total", "Categoria"], hide_index=True)
        if st.button("✅ Sincronizar Entregas", use_container_width=True):
            df_p.update(edited)
            df_p.to_csv(file_pedidos, index=False)
            st.success("Sincronizado"); st.rerun()
