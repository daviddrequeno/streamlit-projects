import streamlit as st
import pandas as pd

def calcular_subtotal(nombre_producto, cantidad, precio_unitario):
    subtotal = float(precio_unitario) * float(cantidad)
    nueva_fila = {
        'Producto': nombre_producto,
        'Cantidad': cantidad,
        'Precio Unitario': precio_unitario,
        'Subtotal': subtotal
    }
    st.session_state.table_data = pd.concat(
        [st.session_state.table_data, pd.DataFrame([nueva_fila])],
        ignore_index=True
    )

if "table_data" not in st.session_state:
    st.session_state.table_data = pd.DataFrame(
        columns=['Producto', 'Cantidad', 'Precio Unitario', 'Subtotal']
    )

st.title("Supermercado en Línea")

with st.form("producto_form"):
    producto_nombre = st.text_input("Nombre del Producto")
    producto_cantidad = st.number_input("Cantidad", min_value=1, step=1)
    producto_precio = st.number_input("Precio Unitario")

    subtotal_button = st.form_submit_button("Comprar Producto")
    if subtotal_button:
        calcular_subtotal(producto_nombre, producto_cantidad, producto_precio)

st.dataframe(st.session_state.table_data)

st.sidebar.markdown(f"**Desarrollado por:** \nDavid Requeno")

if st.button("Calcular total a pagar"):
    total = st.session_state.table_data['Subtotal'].sum()
    st.subheader(f"Total a Pagar: ${total:.2f}")
    st.write("Gracias por su compra. ¡Vuelva pronto!")

