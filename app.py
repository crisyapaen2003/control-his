import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Control de Errores HIS", layout="wide", page_icon="🏥")

# --- INICIO DE SESIÓN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- BASE DE DATOS DE USUARIOS---
USUARIOS_PERMITIDOS = {
    "admin": {"password": "12345", "nombre": "Cristopher Palacios"},
    "auditor1": {"password": "salud2026", "nombre": "Dra. Ana Martínez"},
    "supervisor": {"password": "his_control", "nombre": "Ing. Luis Benites"},
    "carlos.medina": {"password": "medico99", "nombre": "Dr. Carlos Medina"}
}

# --- PANTALLA DE LOGIN ---
def login_screen():
    # foto de fondo de GitHub
    fondo_url = "https://raw.githubusercontent.com/crisyapaen2003/control-his/main/fondo.jpeg"
    
    # URL de una imagen médica
    imagen_medica_url = "https://cdn-icons-png.flaticon.com/512/3063/3063176.png"

    # CSS 
    st.markdown(
        f"""
        <style>
        /* Fondo de pantalla con overlay oscuro */
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)), url("{fondo_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        
        /* Ocultar elementos nativos de Streamlit */
        header, footer, [data-testid="stHeader"] {{
            visibility: hidden;
        }}
        
        /* Contenedor principal del Login */
        div[data-testid="stForm"] {{
            background-color: #1a2332 !important; /* Lado derecho oscuro */
            border: none !important;
            border-radius: 20px !important;
            box-shadow: 0px 20px 40px rgba(0, 0, 0, 0.65) !important;
            max-width: 850px !important;
            margin: 80px auto 0px auto !important;
            padding: 0 !important;
            overflow: hidden !important;
            display: flex !important;
            flex-direction: row !important;
        }}
        
        /* Panel Izquierdo Turquesa Organizado (Título arriba, imagen abajo) */
        div[data-testid="stForm"]::before {{
            content: "HIS\\A\\A Sistema de Control\\A de Calidad";
            white-space: pre-line;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start; /* Alinea el texto en la parte superior */
            text-align: center;
            width: 42%;
            background-color: #2ebfa5 !important;
            color: white !important;
            font-family: 'Inter', sans-serif;
            font-weight: 800;
            font-size: 26px;
            padding: 40px 20px;
            box-sizing: border-box;
            line-height: 1.3;
            
            /* Aquí inyectamos la imagen médica en la parte inferior del panel verde */
            background-image: url("{imagen_medica_url}");
            background-repeat: no-repeat;
            background-position: center 80%; /* Centrado horizontalmente y al 80% del alto */
            background-size: 110px !important; /* Tamaño óptimo para que no tape el texto */
        }}
        
        /* Ajustar el contenedor de inputs para que ocupe el lado derecho */
        div[data-testid="stForm"] > div[data-testid="stVerticalBlock"] {{
            width: 58% !important;
            padding: 40px !important;
            box-sizing: border-box;
        }}
        
        /* Estilizar títulos del panel derecho */
        .login-title-custom {{
            color: white !important;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
            margin-top: 0px;
            margin-bottom: 5px;
            font-size: 28px;
        }}
        .login-subtitle-custom {{
            color: #8b9bb4 !important;
            font-size: 13px;
            margin-bottom: 25px;
        }}
        
        /* Estilo de los Inputs */
        div[data-testid="stForm"] label p {{
            color: #8b9bb4 !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            font-size: 11px !important;
            letter-spacing: 0.8px;
        }}
        
        div[data-testid="stForm"] input {{
            background-color: #121824 !important;
            color: white !important;
            border: 1px solid #2c374e !important;
            border-radius: 8px !important;
        }}
        
        /* Estilo del Botón de Ingreso (Turquesa a juego) */
        div[data-testid="stForm"] button {{
            background-color: #2ebfa5 !important;
            color: white !important;
            border: none !important;
            font-weight: bold !important;
            padding: 10px 0 !important;
            border-radius: 8px !important;
            transition: all 0.3s ease;
        }}
        
        div[data-testid="stForm"] button:hover {{
            background-color: #25a38c !important;
            box-shadow: 0px 4px 15px rgba(46, 191, 165, 0.4) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # formulario -bloque derecho
    with st.form("login_form"):
        st.markdown("<h2 class='login-title-custom'>Iniciar Sesión</h2>", unsafe_allow_html=True)
        st.markdown("<p class='login-subtitle-custom'>Ingresa tus credenciales para acceder al panel</p>", unsafe_allow_html=True)
        
        username = st.text_input("Usuario", placeholder="ejemplo@correo.com")
        password = st.text_input("Contraseña", type="password", placeholder="••••••••")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        submit_button = st.form_submit_button("INICIAR SESIÓN", use_container_width=True)
        
        if submit_button:
            # Validamos si el usuario existe en nuestra nueva estructura
            if username in USUARIOS_PERMITIDOS and USUARIOS_PERMITIDOS[username]["password"] == password:
                st.session_state.logged_in = True
                # 👇 AQUÍ GUARDAMOS EL NOMBRE REAL EN LUGAR DEL USUARIO
                st.session_state.nombre_usuario = USUARIOS_PERMITIDOS[username]["nombre"]
                st.success("¡Acceso concedido!")
                st.rerun()
            else:
                st.error("Credenciales inválidas")

# --CONTROL DE ACCESO ---
if not st.session_state.logged_in:
    login_screen()
else:
    # --- MENÚ LATERAL DE NAVEGACIÓN Y BOTÓN DE SALIDA ---
    st.sidebar.title("Navegación")
    
    # nombre real en la barra lateral
    st.sidebar.markdown(f"👤 **Usuario:** {st.session_state.nombre_usuario}") 
    
    if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
        
    st.sidebar.markdown("---")

    # ---SISTEMA HIS ---
    st.title("🏥 Sistema de Control de Calidad y Errores HIS")
    
    # Saludo
    st.markdown(f"👋 ¡Bienvenido(a), **{st.session_state.nombre_usuario}**! Qué bueno tenerte de vuelta.")
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
                    
                    columnas_interes = ['Lote', 'Pag', 'Reg', 'F_Atención', 'Descripcion_Ups', 'Tipo de Error Detectado', 'Paciente']
                    columnas_a_mostrar = [c for c in columnas_interes if c in df_prof.columns]
                    
                    st.markdown("📋 **Ubicación del Registro para Corrección:**")
                    st.dataframe(df_prof[columnas_a_mostrar], use_container_width=True, hide_index=True)

            else:
                st.warning("No se encontró la columna 'Atiende' para habilitar el buscador.")

            st.markdown("---")

            # ---SECCIÓN DE GRÁFICOS CON FILTRO POR ESTABLECIMIENTO ---
            st.subheader("📊 Análisis de Gráficos por Establecimiento")
            
            if 'Establecimiento' in df_filtrado.columns:
                lista_estabs_graficos = ["Ver Todos"] + sorted(list(df_filtrado['Establecimiento'].dropna().unique()))
                est_seleccionado = st.selectbox(
                    "🏥 Selecciona un Establecimiento para filtrar los gráficos de abajo:",
                    options=lista_estabs_graficos
                )
                
                if est_seleccionado != "Ver Todos":
                    df_graficos = df_filtrado[df_filtrado['Establecimiento'] == est_seleccionado]
                    total_errores_est = len(df_graficos)
                    st.error(f"🏥 **{est_seleccionado}** registra un total de **{total_errores_est:,}** errores.")
                else:
                    df_graficos = df_filtrado.copy()
                    total_errores_est = len(df_graficos)
                    st.info(f"Mostrando datos consolidados de **Todos** los establecimientos. Total: **{total_errores_est:,}** errores.")
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
            
            # --- GRÁFICO: ERRORES POR ESPECIALIDAD ---
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
