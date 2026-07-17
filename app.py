import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE LA PÁGINA (Debe ser la primera instrucción) ---
st.set_page_config(page_title="Control de Errores HIS", layout="wide", page_icon="🏥")

# --- CONTROL DE ESTADO DE INICIO DE SESIÓN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- PANTALLA DE LOGIN ---
def login_screen():
    # Tu imagen de GitHub (y un degradado azul por si la imagen no carga)
    fondo_url = "https://raw.githubusercontent.com/crisyapaen2003/control-his/main/fondo.jpeg"

    # CSS de alta fidelidad para un diseño moderno tipo "Glassmorphism"
    st.markdown(
        f"""
        <style>
        /* Fondo de pantalla con degradado premium y tu imagen encima */
        .stApp {{
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            background-image: linear-gradient(rgba(15, 32, 39, 0.55), rgba(44, 83, 100, 0.55)), url("{fondo_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        
        /* Ocultar decoraciones innecesarias de Streamlit */
        header, footer, [data-testid="stHeader"] {{
            visibility: hidden;
        }}
        
        /* Estilo premium para la tarjeta de login */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: rgba(255, 255, 255, 0.92) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-radius: 20px !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.45) !important;
            padding: 35px 40px !important;
            margin-top: 20px !important;
        }}
        
        /* Estilos para textos dentro del Login */
        .login-header {{
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            color: #1e3c72;
            margin-bottom: 5px;
        }}
        .login-subtitle {{
            text-align: center;
            color: #555555;
            font-size: 14px;
            font-family: 'Inter', sans-serif;
            margin-bottom: 25px;
        }}
        
        /* Estilo para los textos de etiquetas "Usuario" y "Contraseña" */
        label {{
            color: #1e3c72 !important;
            font-weight: 600 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Diseño de columnas: desplazamos la tarjeta hacia la derecha de forma limpia
    col_vacia, col_login = st.columns([1.6, 1])
    
    with col_login:
        # Espacio para centrarlo verticalmente
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
        # Usamos el contenedor con borde nativo que ahora tiene nuestro estilo CSS Premium
        with st.container(border=True):
            st.markdown("<h2 class='login-header'>🏥 Control HIS</h2>", unsafe_allow_html=True)
            st.markdown("<p class='login-subtitle'>Panel de Control de Calidad y Errores</p>", unsafe_allow_html=True)
            
            username = st.text_input("Usuario", placeholder="ejemplo@correo.com", key="login_user")
            password = st.text_input("Contraseña", type="password", placeholder="••••••••", key="login_pass")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("Ingresar al Sistema", use_container_width=True, type="primary"):
                if username == "admin" and password == "12345":
                    st.session_state.logged_in = True
                    st.success("¡Acceso concedido!")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")

# --- LÓGICA DE CONTROL DE ACCESO ---
if not st.session_state.logged_in:
    login_screen()
else:
    # --- MENÚ LATERAL DE NAVEGACIÓN Y BOTÓN DE SALIDA ---
    st.sidebar.title("Navegación")
    if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
        
    st.sidebar.markdown("---")

    # --- TODO TU SISTEMA HIS ORIGINAL EMPIEZA AQUÍ ---
    st.title("🏥 Sistema de Control de Calidad y Errores HIS")
    st.markdown("Sube tu archivo Excel para identificar rápidamente las inconsistencias de digitación por profesional.")

    # Subida del archivo
    archivo_subido = st.file_uploader("Sube la hoja 'Datos de Errores' aquí", type=["xlsx"])

    if archivo_subido is not None:
        try:
            # Cargamos el Excel buscando la pestaña específica
            df = pd.read_excel(archivo_subido, sheet_name="Datos de Errores")
            
            # Limpieza estándar de nombres de columnas
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
            
            if 'Tipo de Error Detectado' in df_filtrado.columns and not df_filtrado['Tipo de Error Detectado'].dropna().empty:
                error_mas_comun = df_filtrado['Tipo de Error Detectado'].mode()[0]
            else:
                error_mas_comun = "N/A"
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Errores Detectados", f"{total_errores:,}")
            col2.metric("Profesionales con Errores", f"{profesionales_con_error}")
            col3.metric("Error Más Frecuente", str(error_mas_comun)[:35] + "...")

            st.markdown("---")

            # --- SECCIÓN: BUSCADOR POR PROFESIONAL ---
            st.subheader("🔍 Buscador de Errores por Profesional")
            st.markdown("Selecciona un profesional de la lista para ver su ficha de inconsistencias personalizada.")
            
            if 'Atiende' in df_filtrado.columns:
                lista_profesionales = sorted(df_filtrado['Atiende'].dropna().unique())
                
                profesional_seleccionado = st.selectbox(
                    "Elige un profesional:",
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
                        st.info(f"🏢 *Establecimiento:* {estabs_texto}")
                    with col_p2:
                        st.error(f"⚠️ *Inconsistencias Totales:* {len(df_prof)}")
                    with col_p3:
                        if 'Tipo de Error Detectado' in df_prof.columns and not df_prof['Tipo de Error Detectado'].dropna().empty:
                            err_comun_prof = df_prof['Tipo de Error Detectado'].mode()[0]
                        else:
                            err_comun_prof = "N/A"
                        st.warning(f"💡 *Error más repetido:* {err_comun_prof}")
                    
                    columnas_interes = ['F_Atención', 'Establecimiento', 'Descripcion_Ups', 'Tipo de Error Detectado', 'Paciente']
                    columnas_a_mostrar = [c for c in columnas_interes if c in df_prof.columns]
                    
                    st.dataframe(df_prof[columnas_a_mostrar], use_container_width=True, hide_index=True)
            else:
                st.warning("No se encontró la columna 'Atiende' para habilitar el buscador.")

            st.markdown("---")

            # --- NUEVA SECCIÓN DE GRÁFICOS CON FILTRO POR ESTABLECIMIENTO ---
            st.subheader("📊 Análisis de Gráficos por Establecimiento")
            
            if 'Establecimiento' in df_filtrado.columns:
                lista_estabs_graficos = ["Ver Todos"] + sorted(list(df_filtrado['Establecimiento'].dropna().unique()))
                est_seleccionado = st.selectbox(
                    "🏥 Selecciona un Establecimiento para filtrar los gráficos de abajo:",
                    options=lista_estabs_graficos
                )
                
                if est_seleccionado != "Ver Todos":
                    df_graficos = df_filtrado[df_filtrado['Establecimiento'] == est_seleccionado]
                    st.info(f"Mostrando datos únicamente de: *{est_seleccionado}*")
                else:
                    df_graficos = df_filtrado.copy()
                    st.info("Mostrando datos consolidados de *Todos* los establecimientos.")
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
