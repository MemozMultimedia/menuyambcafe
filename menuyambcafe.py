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
else:
    df_temp = pd.read_csv(file_pedidos)
    if "Estado" not in df_temp.columns:
        df_temp["Estado"] = "Pendiente"
        df_temp.to_csv(file_pedidos, index=False)

st.set_page_config(page_title="Yamb Café | Menú Digital", layout="wide", page_icon="☕")

# --- CSS Mejorado para Estética y UX ---
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    html, body, [class*='st-'] { font-family: 'Inter', sans-serif !important; color: #1e1e1e; }
    .stApp { background-color: #ffffff; }
    .block-container { padding-top: 1rem !important; }
    header { visibility: hidden; height: 0; }

    .logo-container { display: flex; justify-content: center; align-items: center; width: 100%; padding: 15px 0; }
    .logo-img { max-width: 140px; width: 45%; height: auto; }

    .category-title { 
        background: linear-gradient(135deg, #e63946 0%, #b91d1d 100%); 
        color: white !important; 
        padding: 12px; 
        border-radius: 15px; 
        text-align: center; 
        margin: 25px 0 15px 0; 
        font-weight: 800; 
        font-size: 1.4rem; 
        text-transform: uppercase; 
        letter-spacing: 1px;
    }

    .product-card {
        border-radius: 20px; 
        box-shadow: 0 8px 20px rgba(0,0,0,0.08); 
        text-align: center; 
        margin-bottom: 25px; 
        overflow: hidden; 
        background: white; 
        border: 1px solid #f0f0f0;
        transition: transform 0.2s;
    }
    .product-card:hover { transform: translateY(-2px); }

    .product-img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-bottom: 1px solid #f0f0f0; }
    
    .product-info { padding: 15px; }
    .product-title { font-weight: 800; font-size: 1.15rem; margin-bottom: 5px; color: #1e1e1e; }
    .product-price { color: #e63946 !important; font-weight: 800; font-size: 1.3rem; margin-bottom: 10px; }

    .qty-container { padding: 0 15px 15px 15px; }
    
    .footer-premium { padding: 50px 20px; border-radius: 35px 35px 0 0; margin-top: 40px; text-align: center; background: #f9f9f9; border-top: 1px solid #eee; }
    .footer-brand { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 800; margin-bottom: 10px; }

    /* Mejora visibilidad de inputs */
    .stNumberInput label { font-weight: 700 !important; font-size: 0.9rem !important; color: #555 !important; }
</style>""", unsafe_allow_html=True)

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

if 'auth_role' not in st.session_state: st.session_state.auth_role = None

@st.dialog("📝 Finalizar Orden")
def checkout_modal(carrito, mesa):
    with st.form("form_final"):
        st.subheader("Datos del Cliente")
        nombre = st.text_input("Nombre Completo")
        cedula = st.text_input("Cédula / ID")
        if st.form_submit_button("ENVIAR PEDIDO AHORA", use_container_width=True):
            if nombre and cedula:
                for cat in ["Comida", "Bebida"]:
                    items = [f"{n} x{v[0]}" for n,v in carrito.items() if v[2] == cat]
                    if items:
                        subtotal = sum(v[0]*v[1] for n,v in carrito.items() if v[2] == cat)
                        pd.DataFrame([{"Fecha": datetime.now().strftime("%H:%M"), "Mesa": mesa, "Cliente": nombre, "Pedido": ", ".join(items), "Total": subtotal, "Categoria": cat, "Estado": "Pendiente"}]).to_csv(file_pedidos, mode="a", header=False, index=False)
                st.success("¡Pedido enviado con éxito!"); st.balloons(); st.rerun()

# --- NAVEGACIÓN ---
c_t1, c_t2 = st.columns([10, 1])
with c_t2:
    icon = "🔐" if st.session_state.auth_role is None else "📋"
    if st.button(icon):
        st.session_state.auth_role = "login" if st.session_state.auth_role is None else None
        st.rerun()

if st.session_state.auth_role is None:
    b64_logo = get_image_base64(logo_path)
    if b64_logo: st.markdown(f"<div class='logo-container'><img src='data:image/png;base64,{b64_logo}' class='logo-img'></div>", unsafe_allow_html=True)
    
    c_mesa1, c_mesa2 = st.columns([1, 1])
    with c_mesa1: mesa = st.text_input("📍 Número de Mesa", "1")
    
    carrito = {}
    if os.path.exists(file_menu):
        df_menu = pd.read_csv(file_menu)
        for cat in ["Comida", "Bebida"]:
            st.markdown(f"<div class='category-title'>{'🍔' if cat=='Comida' else '🍹'} {cat.upper()}</div>", unsafe_allow_html=True)
            items = df_menu[df_menu['Categoria'] == cat]
            cols = st.columns(2)
            for i, row in enumerate(items.itertuples()):
                with cols[i % 2]:
                    st.markdown(f"""
                        <div class='product-card'>
                            <img src='{row.Imagen}' class='product-img'>
                            <div class='product-info'>
                                <div class='product-title'>{row.Nombre}</div>
                                <div class='product-price'>RD${row.Precio}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    if row.Disponible:
                        qty = st.number_input("Cantidad", 0, 20, key=f"q{row.Index}", label_visibility="visible")
                        if qty > 0: carrito[row.Nombre] = [qty, row.Precio, cat]
                    else:
                        st.error("Agotado")

    if carrito:
        total = sum(v[0]*v[1] for v in carrito.values())
        st.markdown("--- ")
        if st.button(f"🛒 VER RESUMEN Y PAGAR - RD${total}", use_container_width=True, type="primary"): 
            checkout_modal(carrito, mesa)
    
    st.markdown("""<div class='footer-premium'><div class='footer-brand'>☕ Yamb Café</div><div style='font-size: 0.95rem; color: #666;'>Cada producto apoya el talento local.</div></div>""", unsafe_allow_html=True)

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
        st.subheader("Historial de Pedidos")
        edited_p = st.data_editor(df_p, use_container_width=True, hide_index=True)
        if st.button("💾 Guardar Cambios"):
            edited_p.to_csv(file_pedidos, index=False)
            st.success("Sincronizado")
    else:
        st.subheader(f"Pedidos Pendientes")
        mask = (df_p['Categoria'] == st.session_state.auth_role)
        filtered_df = df_p[mask]
        edited_filtered = st.data_editor(filtered_df, use_container_width=True, disabled=["Fecha", "Mesa", "Cliente", "Pedido", "Total", "Categoria"], hide_index=True)
        if st.button("✅ Confirmar Entregas", use_container_width=True):
            df_p.update(edited_filtered)
            df_p.to_csv(file_pedidos, index=False)
            st.success("Estados actualizados"); st.rerun()
