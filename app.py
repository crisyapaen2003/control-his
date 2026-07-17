import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Control HIS - Login", page_icon="🔒", layout="wide")

# --- CONTROL DE ESTADO DE INICIO DE SESIÓN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- FUNCIÓN PARA LA PANTALLA DE LOGIN CON DISEÑO CORREGIDO ---
def login_screen():
    # Tu imagen de GitHub para el fondo
    fondo_url = "https://raw.githubusercontent.com/crisyapaen2003/control-his/main/fondo.jpg"

    # CSS para el fondo de pantalla y para estilizar la caja de login
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
        
        /* Ocultar elementos predeterminados de Streamlit que no necesitamos */
        header, footer, [data-testid="stHeader"] {{
            visibility: hidden;
        }}
        
        /* Estilo para la tarjeta de login blanca y sólida */
        div[data-testid="stVerticalBlock"] > div > div > div[data-testid="stVerticalBlock"] {{
            background-color: white !important; /* Fondo blanco sólido */
            padding: 40px !important;
            border-radius: 15px !important;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.4) !important; /* Sombra para dar profundidad */
            width: 450px !important; /* Ancho de la caja */
            margin-right: 100px !important; /* Margen derecho para separarlo un poco del borde */
            display: block !important;
        }}
        
        /* Asegurar que el título sea visible y de color oscuro */
        .login-title {{
            color: #0F52BA !important;
            text-align: center;
            margin-bottom: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Lógica de columnas para mover la caja a la derecha
    # Ajustamos la proporción para que el login tenga un buen tamaño
    col_vacia, col_login = st.columns([1.5, 1])
    
    with col_login:
        # Añadimos espacios en blanco arriba para bajar la caja un poco
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
        # Todo este bloque se renderizará dentro de la tarjeta blanca estilizada por el CSS de arriba
        with st.container():
            # Título principal con icono
            st.markdown("<h2 class='login-title'>🔑 Control HIS</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #333; font-size: 16px;'>Ingresa al panel administrativo</p>", unsafe_allow_html=True)
            st.write("---")
            
            # Campos de entrada de texto
            # Usamos claves únicas para asegurar que Streamlit los rastree correctamente
            username = st.text_input("Usuario", placeholder="ejemplo@correo.com", key="login_user")
            password = st.text_input("Contraseña", type="password", placeholder="••••••••", key="login_pass")
            
            st.write("") # Un poco de espacio antes del botón
            
            # Botón de ingreso que ocupa todo el ancho de la tarjeta
            if st.button("Ingresar", use_container_width=True, type="primary"):
                # Credenciales de prueba
                if username == "admin" and password == "12345":
                    st.session_state.logged_in = True
                    st.success("¡Bienvenido!")
                    st.rerun() # Recarga la página para mostrar el contenido principal
                else:
                    st.error("Credenciales inválidas. Por favor, inténtalo de nuevo.")

# --- LÓGICA DE ACCESO ---
if not st.session_state.logged_in:
    login_screen()
else:
    # --- AQUÍ EMPIEZA EL CONTENIDO DE TU APLICACIÓN ---
    st.title("📊 Panel de Control HIS")
    st.write("¡Has iniciado sesión con éxito! Bienvenido al sistema.")
    st.write("Aquí irán tus tablas, gráficos y formularios.")
    
    # Botón para cerrar sesión en la barra lateral
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
