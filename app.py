import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Control HIS - Login", page_icon="🔒", layout="wide")

# --- CONTROL DE ESTADO DE INICIO DE SESIÓN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- FUNCIÓN PARA LA PANTALLA DE LOGIN ---
def login_screen():
    # Tu imagen de GitHub
    fondo_url = "https://raw.githubusercontent.com/crisyapaen2003/control-his/main/fondo.jpeg"

    # Inyectamos el CSS para el fondo y para ocultar las cabeceras de Streamlit
    st.markdown(
        f"""
        <style>
        /* Fondo de pantalla completo */
        .stApp {{
            background-image: url("{fondo_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        
        /* Quitamos las decoraciones por defecto de Streamlit arriba */
        header, footer, [data-testid="stHeader"] {{
            visibility: hidden;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Creamos columnas: una muy ancha a la izquierda y una más pequeña a la derecha
    # Esto empuja TODO el login hacia la derecha de manera limpia y responsiva
    col_vacia, col_login = st.columns([1.8, 1])
    
    with col_login:
        # Añadimos un par de espacios para que el login no quede tan pegado arriba
        st.write("#")
        st.write("#")
        
        # Usamos el contenedor nativo con borde para crear la "tarjeta"
        with st.container(border=True):
            # Título bonito dentro de la tarjeta
            st.markdown("<h2 style='text-align: center; color: #0F52BA; margin-bottom: 0px;'>🔑 Control HIS</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #555; font-size: 14px;'>Ingresa al panel administrativo</p>", unsafe_allow_html=True)
            st.write("---")
            
            # Los campos quedan perfectamente contenidos aquí dentro
            username = st.text_input("Usuario", placeholder="ejemplo@correo.com")
            password = st.text_input("Contraseña", type="password", placeholder="••••••••")
            
            st.write("")
            
            # Botón de ingreso que ocupa el ancho de la tarjeta
            if st.button("Ingresar", use_container_width=True, type="primary"):
                if username == "admin" and password == "12345":
                    st.session_state.logged_in = True
                    st.success("¡Bienvenido!")
                    st.rerun()
                else:
                    st.error("Credenciales inválidas")

# --- LÓGICA DE ACCESO ---
if not st.session_state.logged_in:
    login_screen()
else:
    # --- AQUÍ EMPIEZA EL CONTENIDO DE TU APP ACTUAL ---
    st.title("📊 Panel de Control HIS")
    st.write("¡Has iniciado sesión con éxito!")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
