import streamlit as st

def convertir_lempiras_a_dolares(lempiras):
    tasa_cambio = 26.0  # 1 dólar = 26 lempiras
    dolares = lempiras / tasa_cambio
    return dolares

st.title("Conversor de Monedas")

lempiras = st.number_input("Ingrese la cantidad de dinero a convertir:", min_value=0.0, format="%.2f")

if st.button("Convertir"):
    dolares = convertir_lempiras_a_dolares(lempiras)
    st.write(f"La cantidad en dólares es: ${dolares:.2f}")  
    st.success("Conversión realizada con éxito.")
