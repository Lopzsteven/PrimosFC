import streamlit as st
import random
import json
import os

import base64
import json
import os
import random
import streamlit as st

# 1. Configuración de la página
st.set_page_config(
    page_title="Santa Secreto Futbolero 🎅⚽", page_icon="⚽", layout="centered"
)


# 2. Manejo de la Imagen de Fondo (Soporta .jpeg, .jpg, .png)
def cargar_fondo_local():
    archivos_imagen = [
        "logo.jpeg",
        "logo.jpg",
        "logo.png",
        "1000001288.jpg",
        "1000001288.jpeg",
    ]
    encoded_string = ""
    formato = "jpeg"

    for archivo in archivos_imagen:
        if os.path.exists(archivo):
            with open(archivo, "rb") as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode()
                if archivo.endswith(".png"):
                    formato = "png"
                break

    if encoded_string:
        css = f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-color: #0e1117;
            background-image: linear-gradient(rgba(14, 17, 23, 0.88), rgba(14, 17, 23, 0.88)), 
                              url("data:image/{formato};base64,{encoded_string}"); 
            background-size: 380px;
            background-position: center 20%;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        [data-testid="stHeader"] {{
            background-color: rgba(0,0,0,0) !important;
        }}
        .card-secret {{
            background: linear-gradient(135deg, rgba(30, 60, 114, 0.95) 0%, rgba(42, 82, 152, 0.95) 100%);
            padding: 25px;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.6);
            margin-top: 20px;
            border: 1px solid rgba(255, 215, 0, 0.4);
        }}
        .name-display {{
            font-size: 32px;
            font-weight: 800;
            color: #FFD700;
            margin: 15px 0;
            letter-spacing: 1px;
        }}
        .stButton>button {{
            width: 100%;
            border-radius: 10px;
            font-weight: bold;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)


cargar_fondo_local()

# 3. Lista de Participantes
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

ARCH_DATOS = "datos_sorteo.json"


# 4. Funciones de Persistencia en Archivo JSON
def realizar_sorteo(lista):
    amigos = lista.copy()
    for _ in range(1000):
        random.shuffle(amigos)
        if all(lista[i] != amigos[i] for i in range(len(lista))):
            return {lista[i]: amigos[i] for i in range(len(lista))}
    return None


def inicializar_o_cargar_datos(forzar_reinicio=False):
    if not os.path.exists(ARCH_DATOS) or forzar_reinicio:
        sorteo = realizar_sorteo(PARTICIPANTES)
        pins_num = random.sample(range(1000, 9999), len(PARTICIPANTES))
        pins = {
            nombre: str(pin) for nombre, pin in zip(PARTICIPANTES, pins_num)
        }
        revelados = {nombre: False for nombre in PARTICIPANTES}

        datos = {"sorteo": sorteo, "pins": pins, "revelados": revelados}

        with open(ARCH_DATOS, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        return datos
    else:
        with open(ARCH_DATOS, "r", encoding="utf-8") as f:
            return json.load(f)


def guardar_datos(datos):
    with open(ARCH_DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


# Cargar los datos globales
datos_globales = inicializar_o_cargar_datos()

# 5. Encabezado
st.title("🎅⚽ Santa Secreto Futbolero 🏆")
st.write("¡Descubre a quién te toca regalarle la camiseta retro!")

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
            pin_correcto = datos_globales["pins"].get(nombre_sel, "")

            if pin_ingresado.strip() == pin_correcto.strip():
                # Actualizar y guardar que ya lo consultó
                datos_globales["revelados"][nombre_sel] = True
                guardar_datos(datos_globales)

                asignado = datos_globales["sorteo"].get(
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

    if admin_pass == "admin123":
        st.success("Acceso concedido")

        st.warning("⚠️ Zona de Acciones del Administrador")
        if st.button("🔄 Reiniciar Sorteo y Generar Nuevos PINs"):
            inicializar_o_cargar_datos(forzar_reinicio=True)
            st.success(
                "¡Sorteo reiniciado y guardado globalmente con éxito!"
            )
            st.rerun()

        st.divider()

        # Seguimiento en Vivo
        st.markdown("### 📊 Seguimiento de Consultas")
        revelados_dict = datos_globales.get("revelados", {})
        total_p = len(PARTICIPANTES)
        consultados = sum(1 for e in revelados_dict.values() if e)

        st.progress(consultados / total_p)
        st.info(
            f"**{consultados} de {total_p}** personas ya descubrieron a su amigo secreto."
        )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🟢 Ya consultaron:**")
            vistos = [n for n, e in revelados_dict.items() if e]
            if vistos:
                for nombre in vistos:
                    st.write(f"✅ {nombre}")
            else:
                st.caption("Nadie ha consultado aún.")

        with col2:
            st.markdown("**⏳ Pendientes por consultar:**")
            pendientes = [n for n, e in revelados_dict.items() if not e]
            if pendientes:
                for nombre in pendientes:
                    st.write(f"⏳ {nombre}")
            else:
                st.success("¡Todos han visto a su amigo secreto!")

        st.divider()

        # Credenciales fijas y persistentes
        st.markdown("### 🔑 Credenciales para enviar a los participantes")
        st.write(
            "Los PINs guardados actualmente son fijos para todos los dispositivos:"
        )

        for nombre in PARTICIPANTES:
            pin = datos_globales["pins"].get(nombre, "N/A")
            msg_wa = f"Hola {nombre}! 🎅⚽ Tu PIN para ver quién te tocó en el Santa Secreto Futbolero es: *{pin}*"
            st.code(
                f"{nombre}: PIN [{pin}] | Mensaje: {msg_wa}", language="text"
            )

        st.divider()

        with st.expander("👁️ Ver matriz completa del sorteo (CONFIDENCIAL)"):
            st.json(datos_globales["sorteo"])

    elif admin_pass != "":
        st.error("Contraseña de administrador incorrecta.")
