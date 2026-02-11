import streamlit as st
import pandas as pd
from datetime import date

st.title("Examen I parcial")

st.set_page_config(
    page_title="Tienda de Electrodomésticos",
    layout="centered"
)

# catalogo de productos
catalogo = [
    {"nombre": "Refrigeradora Samsung",  "precio": 4500.00, "categoria": "Refrigeración"},
    {"nombre": "Lavadora LG",            "precio": 3200.00, "categoria": "Lavandería"},
    {"nombre": "Microondas",             "precio":  850.00, "categoria": "Cocina"},
    {"nombre": "Licuadora",              "precio":  350.00, "categoria": "Cocina"},
    {"nombre": "Aire Acondicionado",     "precio": 5800.00, "categoria": "Climatización"},
    {"nombre": "Plancha",                "precio":  280.00, "categoria": "Cuidado del Hogar"},
    {"nombre": "Televisor 4K",           "precio": 7200.00, "categoria": "Entretenimiento"},
    {"nombre": "Cafetera",               "precio":  950.00, "categoria": "Cocina"},
]

nombres_productos = [p["nombre"] for p in catalogo]

st.sidebar.markdown("**Desarrollado por:**\nDavid Requeno")
st.sidebar.markdown("---")
st.sidebar.markdown("Categorías disponibles")
categorias = sorted(set(p["categoria"] for p in catalogo))
for cat in categorias:
    st.sidebar.markdown(f"- {cat}")

st.header("Selección de Producto")

producto_seleccionado = st.selectbox(
    "Selecciona un producto del catalogo:",
    options=nombres_productos
)

# buscar datos del producto seleccionado
producto = next(p for p in catalogo if p["nombre"] == producto_seleccionado)

# mostrar detalles del producto
col1, col2, col3 = st.columns(3)
col1.metric("Nombre",     producto["nombre"])
col2.metric("Precio",     f"L {producto['precio']:,.2f}")
col3.metric("Categoría",  producto["categoria"])

st.markdown("---")
cantidad = st.number_input(
    "Cantidad deseada:",
    min_value=1, max_value=50, step=1, value=1
)

subtotal = producto["precio"] * cantidad
st.info(f"**Subtotal:** L {subtotal:,.2f}  ({cantidad} x L {producto['precio']:,.2f})")

if "carrito" not in st.session_state:
    st.session_state.carrito = []

if st.button("Agregar al carrito"):
    # si el producto ya esta, sumar cantidad
    existe = False
    for item in st.session_state.carrito:
        if item["nombre"] == producto["nombre"]:
            item["cantidad"] += cantidad
            item["subtotal"] = item["precio"] * item["cantidad"]
            existe = True
            break
    if not existe:
        st.session_state.carrito.append({
            "nombre":    producto["nombre"],
            "categoria": producto["categoria"],
            "precio":    producto["precio"],
            "cantidad":  cantidad,
            "subtotal":  subtotal,
        })
    st.success(f"**{producto['nombre']}** agregado al carrito.")

# resumen de compra
st.markdown("---")
st.header("Resumen de Productos")

# detalle del producto actualmente seleccionado 
st.subheader("Producto seleccionado")

r1, r2, r3, r4 = st.columns(4)
r1.markdown("**Producto**")
r2.markdown("**Precio unitario**")
r3.markdown("**Cantidad**")
r4.markdown("**Subtotal**")

r1b, r2b, r3b, r4b = st.columns(4)
r1b.write(producto["nombre"])
r2b.write(f"L {producto['precio']:,.2f}")
r3b.write(cantidad)
r4b.write(f"L {subtotal:,.2f}")

st.subheader("Catálogo completo")

df_catalogo = pd.DataFrame(catalogo)
df_catalogo.columns = ["Nombre", "Precio (L)", "Categoría"]
df_catalogo["Precio (L)"] = df_catalogo["Precio (L)"].map(lambda x: f"L {x:,.2f}")

st.dataframe(df_catalogo, use_container_width=True, hide_index=True)

st.markdown("---")
st.subheader("Carrito de Compras")

if not st.session_state.carrito:
    st.warning("El carrito está vacío. ¡Agrega productos arriba!")
else:
    h1, h2, h3, h4, h5 = st.columns([4, 2, 1, 2, 1])
    h1.markdown("**Producto**")
    h2.markdown("**Categoría**")
    h3.markdown("**Cant.**")
    h4.markdown("**Subtotal**")
    h5.markdown("**Quitar**")

    indices_a_eliminar = []

    for i, item in enumerate(st.session_state.carrito):
        c1, c2, c3, c4, c5 = st.columns([4, 2, 1, 2, 1])
        c1.write(item["nombre"])
        c2.write(item["categoria"])
        c3.write(item["cantidad"])
        c4.write(f"L {item['subtotal']:,.2f}")
        if c5.button("Quitar", key=f"del_{i}"):
            indices_a_eliminar.append(i)

    for idx in sorted(indices_a_eliminar, reverse=True):
        st.session_state.carrito.pop(idx)
    if indices_a_eliminar:
        st.rerun()

    st.markdown("---")
    total_bruto = sum(i["subtotal"] for i in st.session_state.carrito)
    iva         = total_bruto * 0.12
    total_final = total_bruto + iva

    tc1, tc2 = st.columns(2)
    tc1.markdown("**Subtotal:**")
    tc2.markdown(f"L {total_bruto:,.2f}")

    tc3, tc4 = st.columns(2)
    tc3.markdown("**IVA (12%):**")
    tc4.markdown(f"L {iva:,.2f}")
    tc5, tc6 = st.columns(2)
    tc5.markdown("### TOTAL:")
    tc6.markdown(f"### L {total_final:,.2f}")

    st.markdown("---")
    if st.button("Vaciar carrito"):
        st.session_state.carrito = []
        st.rerun()

# reseumen de compra
st.markdown("---")
st.header("Resumen de Facturacion")

if not st.session_state.carrito:
    st.warning("Agrega productos al carrito para generar la factura.")
else:
    st.subheader("Datos del Cliente")

    nombre_cliente = st.text_input("Nombre del cliente:")
    rtn_cliente    = st.text_input("RTN / Número de Identidad:")
    fecha_compra   = st.date_input("Fecha de compra:", value=date.today())

    st.markdown("---")

    st.subheader("Detalle de Compra")

    df_carrito = pd.DataFrame([
        {
            "Producto":          item["nombre"],
            "Cantidad":          item["cantidad"],
            "Precio Unit. (L)":  f"L {item['precio']:,.2f}",
            "Subtotal (L)":      f"L {item['subtotal']:,.2f}",
        }
        for item in st.session_state.carrito
    ])
    st.table(df_carrito)

    st.subheader("Cálculos Finales")

    subtotal_general = sum(i["subtotal"] for i in st.session_state.carrito)
    isv              = subtotal_general * 0.15          # ISV 15%
    total_a_pagar    = subtotal_general + isv

    st.markdown(
        f"**Subtotal general:** suma de todos los subtotales del carrito  \n"
        f"→ L {subtotal_general:,.2f}"
    )
    st.markdown(
        f"**ISV (15%):** L {subtotal_general:,.2f} × 0.15  \n"
        f"→ L {isv:,.2f}"
    )
    st.markdown(
        f"**Total a pagar:** subtotal general + ISV  \n"
        f"→ L {subtotal_general:,.2f} + L {isv:,.2f}"
    )

    st.markdown("---")
    fa1, fa2 = st.columns(2)
    fa1.markdown("**Subtotal general:**")
    fa2.markdown(f"L {subtotal_general:,.2f}")

    fa3, fa4 = st.columns(2)
    fa3.markdown("**ISV (15%):**")
    fa4.markdown(f"L {isv:,.2f}")

    fa5, fa6 = st.columns(2)
    fa5.markdown("##Total a pagar:")
    fa6.markdown(f"## L {total_a_pagar:,.2f}")

    st.markdown("---")
    if st.button("Generar Factura"):
        if not nombre_cliente.strip():
            st.error("Por favor ingresa el nombre del cliente.")
        elif not rtn_cliente.strip():
            st.error("Por favor ingresa el RTN o número de identidad.")
        else:
            st.success("Factura generada exitosamente.")
            st.markdown("###FACTURA")
            st.markdown(f"**Cliente:** {nombre_cliente}")
            st.markdown(f"**RTN / Identidad:** {rtn_cliente}")
            st.markdown(f"**Fecha:** {fecha_compra.strftime('%d/%m/%Y')}")
            st.markdown("---")
            st.table(df_carrito)
            st.markdown(f"**Subtotal general:** L {subtotal_general:,.2f}")
            st.markdown(f"**ISV (15%):** L {isv:,.2f}")
            st.markdown(f"### Total a pagar: L {total_a_pagar:,.2f}")