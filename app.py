import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Control de Errores HIS", layout="wide", page_icon="🏥")

# --- SISTEMA DE LOGIN SIMPLE ---
def check_password():
    """Retorna True si el usuario ingresó la contraseña correcta."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # Mostrar formulario de ingreso
    st.markdown("### 🔐 Acceso Restringido - Control de Calidad HIS")
    password = st.text_input("Ingresa la contraseña institucional para usar la herramienta:", type="password")
    
    # Define aquí la contraseña que usarán los profesionales
    CONTRASENA_CORRECTA = "HIS2026" 

    if st.button("Ingresar"):
        if password == CONTRASENA_CORRECTA:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("🔑 Contraseña incorrecta. Inténtalo de nuevo.")
    return False

# Si la contraseña no es correcta, detenemos la ejecución aquí
if not check_password():
    st.stop()

# --- INICIO DE LA APLICACIÓN (Tu código original optimizado) ---

st.title("🏥 Sistema de Control de Calidad y Errores HIS")
st.markdown("Sube tu archivo Excel para identificar rápidamente las inconsistencias de digitación por profesional.")

# Subida del archivo
archivo_subido = st.file_uploader("Sube la hoja 'Datos de Errores' aquí", type=["xlsx"])

if archivo_subido is not None:
    try:
        # Cargamos el Excel buscando la pestaña específica
        df = pd.read_excel(archivo_subido, sheet_name="Datos de Errores")
        
        # Limpieza estándar de nombres de columnas (quita espacios invisibles al inicio/final)
        df.columns = df.columns.str.strip()
        
        st.success("¡Base de datos cargada con éxito!")
        
        # --- FILTROS DINÁMICOS EN LA BARRA LATERAL ---
        st.sidebar.header("Filtros de Reporte")
        
        # Filtro de Establecimiento General
        if 'Establecimiento' in df.columns:
            estab_seleccionados = st.sidebar.multiselect(
                "Filtrar Base de Datos por Establecimiento", 
                options=df['Establecimiento'].unique(), 
                default=df['Establecimiento'].unique()
            )
            df_filtrado = df[df['Establecimiento'].isin(estab_seleccionados)]
        else:
            df_filtrado = df.copy()

        # --- TARJETAS DE INDICADORES ---
        st.subheader("📌 Resumen de Inconsistencias")
        total_errores = len(df_filtrado)
        
        profesionales_con_error = df_filtrado['Atiende'].nunique() if 'Atiende' in df_filtrado.columns else 0
        
        # Evitamos errores si el filtro queda vacío
        moda_serie = df_filtrado['Tipo de Error Detectado'].dropna().mode() if 'Tipo de Error Detectado' in df_filtrado.columns else []
        error_mas_comun = moda_serie[0] if len(moda_serie) > 0 else "N/A"
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Errores Detectados", f"{total_errores:,}")
        col2.metric("Profesionales con Errores", f"{profesionales_con_error}")
        col3.metric("Error Más Frecuente", str(error_mas_comun)[:35] + "...")

        st.markdown("---")

        # --- SECCIÓN: BUSCADOR POR PROFESIONAL ---
        st.subheader("🔍 Buscador de Errores por Profesional")
        st.markdown("Selecciona tu nombre de la lista para ver tu ficha de inconsistencias personalizada.")
        
        if 'Atiende' in df_filtrado.columns:
            lista_profesionales = sorted(df_filtrado['Atiende'].dropna().unique())
            
            profesional_seleccionado = st.selectbox(
                "Elige tu nombre de la lista:",
                options=lista_profesionales,
                index=0 if lista_profesionales else None
            )
            
            if profesional_seleccionado:
                df_prof = df_filtrado[df_filtrado['Atiende'] == profesional_seleccionado]
                
                if 'Establecimiento' in df_prof.columns:
                    estabs = df_prof['Establecimiento'].dropna().unique()
                    estabs_texto = ", ".join(estabs)
                else:
                    estabs_texto = "No especificado"
                
                col_p1, col_p2, col_p3 = st.columns(3)
                with col_p1:
                    st.info(f"🏢 **Establecimiento:** {estabs_texto}")
                with col_p2:
                    st.error(f"⚠️ **Inconsistencias Totales:** {len(df_prof)}")
                with col_p3:
                    err_comun_prof_serie = df_prof['Tipo de Error Detectado'].dropna().mode() if 'Tipo de Error Detectado' in df_prof.columns else []
                    err_comun_prof = err_comun_prof_serie[0] if len(err_comun_prof_serie) > 0 else "N/A"
                    st.warning(f"💡 **Error más repetido:** {err_comun_prof}")
                
                columnas_interes = ['F_Atención', 'Establecimiento', 'Descripcion_Ups', 'Tipo de Error Detectado', 'Paciente']
                columnas_a_mostrar = [c for c in columnas_interes if c in df_prof.columns]
                
                st.dataframe(df_prof[columnas_a_mostrar], use_container_width=True, hide_index=True)
        else:
            st.warning("No se encontró la columna 'Atiende' para habilitar el buscador.")

        st.markdown("---")

        # --- NUEVA SECCIÓN DE GRÁFICOS CON FILTRO POR ESTABLECIMIENTO ---
        st.subheader("📊 Análisis de Gráficos por Establecimiento")
        
        # Botón selector de establecimiento exclusivo para los gráficos
        if 'Establecimiento' in df_filtrado.columns:
            lista_estabs_graficos = ["Ver Todos"] + sorted(list(df_filtrado['Establecimiento'].dropna().unique()))
            est_seleccionado = st.selectbox(
                "🏥 Selecciona un Establecimiento para filtrar los gráficos de abajo:",
                options=lista_estabs_graficos
            )
            
            # Aplicamos el filtro para los gráficos
            if est_seleccionado != "Ver Todos":
                df_graficos = df_filtrado[df_filtrado['Establecimiento'] == est_seleccionado]
                st.info(f"Mostrando datos únicamente de: **{est_seleccionado}**")
            else:
                df_graficos = df_filtrado.copy()
                st.info("Mostrando datos consolidados de **Todos** los establecimientos.")
        else:
            df_graficos = df_filtrado.copy()

        # Renderizado de los dos gráficos
        col_g1, col_g2 = st.columns(2)

        # Gráfico 1: Profesionales con más errores
        with col_g1:
            st.markdown("### 👨‍⚕️ Top 10 Profesionales con más Errores")
            if 'Atiende' in df_graficos.columns and len(df_graficos) > 0:
                df_prof_graf = df_graficos['Atiende'].value_counts().reset_index().head(10)
                df_prof_graf.columns = ['Profesional', 'Cantidad de Errores']
                
                fig_prof = px.bar(
                    df_prof_graf, 
                    x='Cantidad de Errores', 
                    y='Profesional', 
                    orientation='h',
                    color='Cantidad de Errores',
                    color_continuous_scale='Reds'
                )
                fig_prof.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_prof, use_container_width=True)
            else:
                st.warning("No hay datos disponibles para mostrar en este establecimiento.")

        # Gráfico 2: Errores más comunes
        with col_g2:
            st.markdown("### ⚠️ Errores más Comunes en el HIS")
            if 'Tipo de Error Detectado' in df_graficos.columns and len(df_graficos) > 0:
                df_err = df_graficos['Tipo de Error Detectado'].value_counts().reset_index().head(10)
                df_err.columns = ['Tipo de Error', 'Cantidad']
                
                fig_err = px.pie(
                    df_err, 
                    values='Cantidad', 
                    names='Tipo de Error', 
                    hole=0.4
                )
                st.plotly_chart(fig_err, use_container_width=True)
            else:
                st.warning("No hay datos disponibles para mostrar en este establecimiento.")

        st.markdown("---")
        
        # --- GRÁFICO EXTRA: ERRORES POR ESPECIALIDAD ---
        st.subheader("🏢 Distribución de Errores por Área / Especialidad")
        if 'Descripcion_Ups' in df_graficos.columns and len(df_graficos) > 0:
            df_up = df_graficos['Descripcion_Ups'].value_counts().reset_index()
            df_up.columns = ['Especialidad', 'Cantidad de Errores']
            
            fig_up = px.bar(
                df_up,
                x='Especialidad',
                y='Cantidad de Errores',
                color='Cantidad de Errores',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_up, use_container_width=True)
        else:
            st.warning("No hay datos disponibles de especialidades para este establecimiento.")
        
        # --- TABLA DE DETALLE GLOBAL ---
        st.subheader("📋 Tabla General de Inconsistencias (Primeros 500 registros)")
        columnas_visibles = []
        for col in ['Atiende', 'Establecimiento', 'Descripcion_Ups', 'Tipo de Error Detectado']:
            if col in df_filtrado.columns:
                columnas_visibles.append(col)
                
        if columnas_visibles:
            st.dataframe(df_filtrado[columnas_visibles].head(500), hide_index=True)
        else:
            st.dataframe(df_filtrado.head(500), hide_index=True)

    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
        st.info("Asegúrate de que la hoja de tu archivo de Excel se llame exactamente 'Datos de Errores'.")
else:
    st.info("A la espera del archivo Excel. Por favor arrástralo en el recuadro superior.")
