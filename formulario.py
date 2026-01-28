import streamlit as st

st.sidebar.markdown(f"**Desarrollado por:** \nDavid Requeno")

st.title("Formulario de Registro Estudiantil")

nombre = st.text_input("Nombre Completo")
edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
carrera = st.selectbox("Carrera", ["Ingeniería", "Medicina", "Derecho", "Arquitectura", "Administración"])
comentario = st.text_area("Comentario Adicional")

if st.button("Enviar"):
    st.write(f"Nombre: {nombre}")
    st.write(f"Edad: {edad}")
    st.write(f"Carrera: {carrera}")
    st.write(f"Comentario: {comentario}")
    st.success("Formulario enviado con éxito.")