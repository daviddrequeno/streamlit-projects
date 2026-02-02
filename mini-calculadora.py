import streamlit as st
import pandas as pd

def agregar_ingreso(categoria, monto):
    """Agrega un ingreso a la tabla de ingresos"""
    nueva_fila = {
        'Tipo': 'Ingreso',
        'Categoría': categoria,
        'Monto': float(monto)
    }
    st.session_state.datos_financieros = pd.concat(
        [st.session_state.datos_financieros, pd.DataFrame([nueva_fila])],
        ignore_index=True
    )

def agregar_gasto(categoria, monto):
    """Agrega un gasto a la tabla de gastos"""
    nueva_fila = {
        'Tipo': 'Gasto',
        'Categoría': categoria,
        'Monto': float(monto)
    }
    st.session_state.datos_financieros = pd.concat(
        [st.session_state.datos_financieros, pd.DataFrame([nueva_fila])],
        ignore_index=True
    )

if "datos_financieros" not in st.session_state:
    st.session_state.datos_financieros = pd.DataFrame(
        columns=['Tipo', 'Categoría', 'Monto']
    )

st.set_page_config(
    page_title="Calculadora de Presupuesto Universitario",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Calculadora de Presupuesto Universitario")

# dividir en dos columnas
col1, col2 = st.columns(2)

# columna 1 formulario de Ingresos
with col1:
    st.subheader("Registrar Ingresos")
    with st.form("form_ingresos"):
        categoria_ingreso = st.selectbox(
            "Categoría de Ingreso",
            ["Mesada/Ayuda familiar", "Beca", "Trabajo", "Otros ingresos"]
        )
        monto_ingreso = st.number_input(
            "Monto ($)",
            min_value=0.0,
            step=10.0,
            format="%.2f"
        )
        
        submit_ingreso = st.form_submit_button("Agregar ingreso")
        if submit_ingreso:
            if monto_ingreso <= 0:
                st.error("El monto debe ser mayor a 0")
            else:
                agregar_ingreso(categoria_ingreso, monto_ingreso)
                st.success(f"Ingreso de ${monto_ingreso:.2f} agregado")

# Columna 2 formulario de Gastos
with col2:
    st.subheader("Registrar Gastos")
    with st.form("form_gastos"):
        categoria_gasto = st.selectbox(
            "Categoría de Gasto",
            ["Matrícula", "Transporte", "Alimentación", "Materiales", "Vivienda", "Entretenimiento", "Otros gastos"]
        )
        monto_gasto = st.number_input(
            "Monto ($)",
            min_value=0.0,
            step=10.0,
            format="%.2f"
        )
        
        submit_gasto = st.form_submit_button("Agregar Gasto")
        if submit_gasto:
            if monto_gasto <= 0:
                st.error("El monto debe ser mayor a 0")
            else:
                agregar_gasto(categoria_gasto, monto_gasto)
                st.success(f"Gasto de ${monto_gasto:.2f} agregado")

# mostrar tabla de datos
st.markdown("---")
st.subheader("Registro de Transacciones")

if not st.session_state.datos_financieros.empty:
    st.dataframe(st.session_state.datos_financieros, use_container_width=True, hide_index=True)
    
    # botón para calcular balance
    if st.button("Calcular Balance Mensual", type="primary"):
        df = st.session_state.datos_financieros
        
        total_ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].sum()
        total_gastos = df[df['Tipo'] == 'Gasto']['Monto'].sum()
        balance = total_ingresos - total_gastos
        
        st.markdown("---")
        st.subheader("Análisis Financiero")
        
        # metricas
        col_m1, col_m2, col_m3 = st.columns(3)
        
        with col_m1:
            st.metric("Total Ingresos", f"${total_ingresos:,.2f}")
        
        with col_m2:
            st.metric("Total Gastos", f"${total_gastos:,.2f}")
        
        with col_m3:
            st.metric("Balance", f"${balance:,.2f}")
        
        st.markdown("---")
        
        if balance > 0:
            porcentaje_ahorro = (balance / total_ingresos * 100) if total_ingresos > 0 else 0
            
            if porcentaje_ahorro >= 20:
                st.success(f"¡Excelente gestión! Estás ahorrando ${balance:,.2f} ({porcentaje_ahorro:.1f}% de tus ingresos). Mantén estos buenos hábitos financieros.")
            elif porcentaje_ahorro >= 10:
                st.info(f"Bien hecho. Estás ahorrando ${balance:,.2f} ({porcentaje_ahorro:.1f}% de tus ingresos). Intenta aumentar tu ahorro al 20%.")
            else:
                st.warning(f"Estás ahorrando ${balance:,.2f} ({porcentaje_ahorro:.1f}% de tus ingresos). Es un porcentaje bajo. Considera reducir gastos no esenciales.")
        
        elif balance == 0:
            st.warning("Tus ingresos y gastos están equilibrados. No estás ahorrando. Busca maneras de reducir gastos.")
        
        else:
            deficit = abs(balance)
            st.error(f"¡Atención! Estás gastando ${deficit:,.2f} más de lo que ingresas. Necesitas reducir gastos urgentemente.")
            st.markdown("**Recomendaciones:**")
            st.markdown("- Revisa gastos en entretenimiento y categorías no esenciales")
            st.markdown("- Busca opciones más económicas de transporte y alimentación")
            st.markdown("- Considera buscar un trabajo de medio tiempo")
        
        # mostrar detalle por categoría
        st.markdown("---")
        st.subheader("Detalle por Categoría")
        
        col_det1, col_det2 = st.columns(2)
        
        with col_det1:
            st.markdown("**Ingresos por Categoría**")
            df_ingresos = df[df['Tipo'] == 'Ingreso'].groupby('Categoría')['Monto'].sum().reset_index()
            if not df_ingresos.empty:
                st.dataframe(df_ingresos, use_container_width=True, hide_index=True)
            else:
                st.info("No hay ingresos registrados")
        
        with col_det2:
            st.markdown("**Gastos por Categoría**")
            df_gastos = df[df['Tipo'] == 'Gasto'].groupby('Categoría')['Monto'].sum().reset_index()
            if not df_gastos.empty:
                df_gastos['Porcentaje (%)'] = (df_gastos['Monto'] / total_gastos * 100).round(2)
                st.dataframe(df_gastos, use_container_width=True, hide_index=True)
            else:
                st.info("No hay gastos registrados")
    
    if st.button("Limpiar todo"):
        st.session_state.datos_financieros = pd.DataFrame(
            columns=['Tipo', 'Categoría', 'Monto']
        )
        st.rerun()

else:
    st.info("Agrega tus ingresos y gastos usando los formularios de arriba")

# Footer
st.markdown("---")
st.markdown("Desarrollado por David Requeno")