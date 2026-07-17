import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Control HIS - Login", page_icon="🔒", layout="wide")

# --- CONTROL DE ESTADO DE INICIO DE SESIÓN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- FUNCIÓN PARA LA PANTALLA DE LOGIN CON DISEÑO ---
def login_screen():
    # Usamos la imagen que subiste a tu propio repositorio de GitHub
    fondo_url = "https://raw.githubusercontent.com/crisyapaen2003/control-his/main/fondo.jpeg"

    # Inyectamos CSS para poner la imagen de fondo y posicionar el login a la derecha
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
        
        /* Contenedor principal para mover el login arriba a la derecha */
        .login-container {{
            position: absolute;
            top: 40px;
            right: 40px;
            width: 380px;
            background-color: rgba(255, 255, 255, 0.95); /* Fondo blanco con un toque de transparencia */
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.3);
            z-index: 999;
        }}
        
        /* Ocultar elementos innecesarios de Streamlit en la pantalla de login */
        header, footer, [data-testid="stHeader"] {{
            visibility: hidden;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Creamos el contenedor del login usando HTML/CSS personalizado
    st.markdown(
        """
        <div class="login-container">
            <h2 style='text-align: center; color: #0F52BA; margin-bottom: 5px;'>🔑 Control HIS</h2>
            <p style='text-align: center; color: #555; font-size: 14px;'>Ingresa al panel administrativo</p>
            <hr style='border: 0.5px solid #eee; margin-bottom: 20px;'>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Colocamos los campos de entrada de Streamlit empujados hacia la derecha
    col_vacia, col_login = st.columns([2.2, 1])
    
    with col_login:
        # Añadimos un espacio invisible arriba para alinear los inputs con nuestro contenedor flotante
        st.write("###")
        
        username = st.text_input("Usuario", placeholder="ejemplo@correo.com", key="user_input")
        password = st.text_input("Contraseña", type="password", placeholder="••••••••", key="pass_input")
        
        st.write("")
        if st.button("Ingresar", use_container_width=True, type="primary"):
            # Credenciales de prueba (puedes cambiarlas por las que gustes)
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
