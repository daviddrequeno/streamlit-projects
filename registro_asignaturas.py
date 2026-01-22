import streamlit as st
import pandas as pd
from datetime import date

CAMPUS = ["Central", "Norte", "Sur", "Virtual"]

PROFESORES = {
    "Central": ["Ana Pérez", "Luis Gómez", "María Torres"],
    "Norte": ["Carlos Ruiz", "Elena Soto"],
    "Sur": ["Jorge Ramírez", "Paula Díaz"],
    "Virtual": ["Equipo Virtual"]
}

AULAS = {
    "Central": ["A-101", "A-102", "Lab-1"],
    "Norte": ["B-201", "B-202"],
    "Sur": ["C-301", "C-302"],
    "Virtual": ["Online"]
}

def registrar_asignatura(nombre, campus, fecha, hora_inicio, hora_final, aula, maestro):
    nueva_fila = {
        'Asignatura': nombre,
        'Campus': campus,
        'Fecha de Registro': fecha,
        'Hora Inicio': hora_inicio,
        'Hora Final': hora_final,
        'Aula': aula,
        'Maestro': maestro
    }

    st.session_state.table_data = pd.concat(
        [st.session_state.table_data, pd.DataFrame([nueva_fila])],
        ignore_index=True
    )

if "table_data" not in st.session_state:
    st.session_state.table_data = pd.DataFrame(
        columns=[
            'Asignatura', 'Campus', 'Fecha de Registro',
            'Hora Inicio', 'Hora Final', 'Aula', 'Maestro'
        ]
    )

st.title("Registro de Asignaturas Matriculadas")

with st.form("asignatura_form"):
    nombre = st.text_input("Nombre de la Asignatura")

    campus = st.selectbox("Campus", CAMPUS)
    maestro = st.selectbox("Profesor", PROFESORES[campus])
    aula = st.selectbox("Aula", AULAS[campus])

    fecha = st.date_input("Fecha de Registro")
    hora_inicio = st.time_input("Hora de Inicio")
    hora_final = st.time_input("Hora Final")

    registrar = st.form_submit_button("Registrar Asignatura")

    if registrar:
        hoy = date.today()

        if fecha < hoy:
            st.error("No se puede registrar una asignatura con fecha anterior a hoy.")
        elif hora_inicio >= hora_final:
            st.error("La hora de inicio debe ser menor que la hora final.")
        else:
            registrar_asignatura(
                nombre, campus,
                fecha, hora_inicio, hora_final,
                aula, maestro
            )
            st.success("Asignatura registrada correctamente.")


st.subheader("Reporte de Asignaturas")
st.dataframe(st.session_state.table_data, use_container_width=True)
