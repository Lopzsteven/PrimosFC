import streamlit as st
import random
import json
import os

import base64
import random
import streamlit as st

# 1. Configuración de la página
st.set_page_config(
    page_title="Santa Secreto Futbolero 🎅⚽", page_icon="⚽", layout="centered"
)


# Función para cargar la imagen local como fondo en CSS
def set_background_image(image_file_path):
    with open(image_file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    css_style = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(14, 17, 23, 0.88), rgba(14, 17, 23, 0.88)),
                    url("data:image/jpeg;base64,{encoded_string}");
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .main {{
        background: transparent;
    }}
    .stButton>button {{
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }}
    .card-secret {{
        background: linear-gradient(135deg, rgba(30, 60, 114, 0.95) 0%, rgba(42, 82, 152, 0.95) 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        margin-top: 20px;
        border: 1px solid rgba(255, 215, 0, 0.3);
    }}
    .name-display {{
        font-size: 32px;
        font-weight: 800;
        color: #FFD700;
        margin: 15px 0;
        letter-spacing: 1px;
    }}
    </style>
    """
    st.markdown(css_style, unsafe_allow_html=True)


# Si tienes la imagen en la misma carpeta guardada como "logo.jpg":
try:
    set_background_image("logo.jpg")
except FileNotFoundError:
    # Estilo de respaldo si aún no has puesto el archivo de imagen en la carpeta
    st.markdown(
        """
        <style>
        .stApp { background-color: #0e1117; }
        .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
        .card-secret {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 25px; border-radius: 15px; color: white; text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3); margin-top: 20px;
        }
        .name-display { font-size: 32px; font-weight: 800; color: #FFD700; margin: 15px 0; }
        </style>
    """,
        unsafe_allow_html=True,
    )

# 2. Lista de Participantes
PARTICIPANTES = [
    "César",
    "Pedro",
    "Omar",
    "Fon",
    "Diego Novoa",
    "Jason",
    "Yuldor",
    "Harry",
    "Cristian",
    "Martín",
    "Hebert",
    "Steven",
    "Parra",
    "Camilo",
    "Chipi",
    "Daniel",
]


# 3. Lógica del Sorteo Segura
def realizar_sorteo(lista):
    amigos = lista.copy()
    max_intentos = 1000
    for _ in range(max_intentos):
        random.shuffle(amigos)
        if all(lista[i] != amigos[i] for i in range(len(lista))):
            return {lista[i]: amigos[i] for i in range(len(lista))}
    return None


# 4. Inicialización del Estado de la Sesión
if "sorteo" not in st.session_state:
    st.session_state.sorteo = realizar_sorteo(PARTICIPANTES)

if "pins" not in st.session_state:
    pins_disponibles = random.sample(range(1000, 9999), len(PARTICIPANTES))
    st.session_state.pins = {
        nombre: str(pin) for nombre, pin in zip(PARTICIPANTES, pins_disponibles)
    }

if "revelados" not in st.session_state:
    st.session_state.revelados = {nombre: False for nombre in PARTICIPANTES}

# 5. Encabezado de la App
st.title("🎅⚽ Santa Secreto Futbolero 🏆")
st.write("¡Descubre a quién te toca regalarle la camiseta retro!")

# Pestañas de navegación
tab1, tab2 = st.tabs(
    ["👤 Descubrir Mi Amigo Secreto", "⚙️ Panel de Administrador"]
)

# ==========================================
# PESTAÑA 1: JUGADORES
# ==========================================
with tab1:
    st.subheader("Consulta tu asignación")

    nombre_sel = st.selectbox(
        "Selecciona tu nombre:", ["-- Selecciona tu nombre --"] + PARTICIPANTES
    )
    pin_ingresado = st.text_input(
        "Ingresa tu PIN de 4 dígitos:", type="password", max_chars=4
    )

    if st.button("Revelar mi Amigo Secreto 🎁"):
        if nombre_sel == "-- Selecciona tu nombre --":
            st.error("Por favor selecciona tu nombre de la lista.")
        elif not pin_ingresado:
            st.warning("Ingresa tu PIN para continuar.")
        else:
            pin_correcto = st.session_state.pins.get(nombre_sel, "")

            if pin_ingresado == pin_correcto:
                st.session_state.revelados[nombre_sel] = True
                asignado = st.session_state.sorteo.get(
                    nombre_sel, "No asignado"
                )
                st.markdown(
                    f"""
                    <div class="card-secret">
                        <h3>¡Hola, {nombre_sel}! 👋</h3>
                        <p>Tu amigo secreto al que debes regalarle es:</p>
                        <div class="name-display">⚽ {asignado} ⚽</div>
                        <p><i>¡Recuerda revisar sus 3 equipos favoritos y sus 3 prohibidos!</i></p>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
                st.balloons()
            else:
                st.error("❌ PIN incorrecto. Revisa e intenta de nuevo.")

# ==========================================
# PESTAÑA 2: ADMINISTRADOR
# ==========================================
with tab2:
    st.subheader("Acceso Administrador")
    admin_pass = st.text_input(
        "Contraseña de Administrador:", type="password", key="admin_key"
    )

    if admin_pass == "admin123*+":
        st.success("Acceso concedido")

        # -----------------------------------------------------------
        # BOTÓN DE REINICIO DE SORTEO Y PINS
        # -----------------------------------------------------------
        st.warning("⚠️ Zona de Acciones del Administrador")
        if st.button("🔄 Reiniciar Sorteo y Generar Nuevos PINs"):
            st.session_state.clear()
            st.success("¡Sorteo reiniciado con éxito!")
            st.rerun()

        st.divider()

        # -----------------------------------------------------------
        # SEGUIMIENTO Y ESTADO DE CONSULTAS
        # -----------------------------------------------------------
        st.markdown("### 📊 Seguimiento de Consultas")

        total_participantes = len(PARTICIPANTES)
        consultados = sum(
            1 for estado in st.session_state.revelados.values() if estado
        )

        st.progress(consultados / total_participantes)
        st.info(
            f"**{consultados} de {total_participantes}** personas ya descubrieron a su amigo secreto."
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🟢 Ya consultaron:**")
            vistos = [
                n for n, e in st.session_state.revelados.items() if e
            ]
            if vistos:
                for nombre in vistos:
                    st.write(f"✅ {nombre}")
            else:
                st.caption("Nadie ha consultado aún.")

        with col2:
            st.markdown("**⏳ Pendientes por consultar:**")
            pendientes = [
                n for n, e in st.session_state.revelados.items() if not e
            ]
            if pendientes:
                for nombre in pendientes:
                    st.write(f"⏳ {nombre}")
            else:
                st.success("¡Todos han visto a su amigo secreto!")

        st.divider()

        # -----------------------------------------------------------
        # CREDENCIALES PARA ENVIAR POR WHATSAPP
        # -----------------------------------------------------------
        st.markdown("### 🔑 Credenciales para enviar a los participantes")
        st.write("Copia el PIN de cada participante y envíaselo por privado:")

        for nombre in PARTICIPANTES:
            pin = st.session_state.pins.get(nombre, "N/A")
            msg_wa = f"Hola {nombre}! 🎅⚽ Tu PIN para ver quién te tocó en el Santa Secreto Futbolero es: *{pin}*"
            st.code(
                f"{nombre}: PIN [{pin}] | Mensaje: {msg_wa}", language="text"
            )

        st.divider()

        # Ver matriz completa del sorteo de forma privada
        with st.expander("👁️ Ver matriz completa del sorteo (CONFIDENCIAL)"):
            st.json(st.session_state.sorteo)

    elif admin_pass != "":
        st.error("Contraseña de administrador incorrecta.")
