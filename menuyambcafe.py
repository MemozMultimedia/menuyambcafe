import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Menu Digital Pro", layout="wide")

# Base de datos
file = "pedidos.csv"

if not os.path.exists(file):
    df = pd.DataFrame(columns=["Fecha", "Mesa", "Pedido", "Total", "Pago"])
    df.to_csv(file, index=False)

# MENÚ
menu = {
    "Bebidas": {
        "Café": 100,
        "Cerveza": 150,
        "Jugo": 120
    },
    "Comida": {
        "Pizza": 300,
        "Hamburguesa": 250,
        "Hot Dog": 150
    }
}

# SIDEBAR
modo = st.sidebar.selectbox("Modo", ["Cliente", "Admin"])

# ================= CLIENTE =================
if modo == "Cliente":
    st.title("🍽️ Menú Digital")

    mesa = st.text_input("Número de mesa")

    carrito = []

    for categoria, items in menu.items():
        st.subheader(categoria)
        for nombre, precio in items.items():
            col1, col2, col3 = st.columns([3,1,1])

            with col1:
                st.write(f"{nombre} - RD${precio}")
            with col2:
                cantidad = st.number_input(f"{nombre}", 0, 10, 0, key=nombre)
            with col3:
                if cantidad > 0:
                    carrito.append((nombre, cantidad, precio))

    # Calcular total
    total = sum(cant * precio for nombre, cant, precio in carrito)

    st.markdown(f"## 💰 Total: RD${total}")

    pago = st.selectbox("Forma de pago", ["Efectivo", "Transferencia", "Tarjeta"])

    if st.button("Confirmar pedido"):
        if mesa == "":
            st.warning("Introduce número de mesa")
        elif len(carrito) == 0:
            st.warning("Selecciona al menos un producto")
        else:
            pedido_texto = ", ".join([f"{n} x{c}" for n,c,p in carrito])

            nuevo = pd.DataFrame([{
                "Fecha": datetime.now(),
                "Mesa": mesa,
                "Pedido": pedido_texto,
                "Total": total,
                "Pago": pago
            }])

            nuevo.to_csv(file, mode='a', header=False, index=False)
            st.success("✅ Pedido enviado!")

# ================= ADMIN =================
elif modo == "Admin":
    st.title("📊 Panel Administrativo")

    if os.path.exists(file):
        df = pd.read_csv(file)
        st.subheader("Pedidos en tiempo real")
        st.dataframe(df)

        # Métricas
        total_dia = df["Total"].sum()
        pedidos = len(df)

        col1, col2 = st.columns(2)
        col1.metric("💰 Total vendido", f"RD${total_dia}")
        col2.metric("🧾 Pedidos", pedidos)

        # Filtro por mesa
        mesa_filtro = st.text_input("Filtrar por mesa")

        if mesa_filtro:
            df_filtrado = df[df["Mesa"] == mesa_filtro]
            st.dataframe(df_filtrado)
    else:
        st.info("No hay pedidos registrados aún.")
