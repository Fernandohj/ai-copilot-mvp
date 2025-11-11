import sys
import os

# Forzar la raíz del proyecto al inicio del path para los imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import time
import core.conversation as conversation
import core.prompting as prompting
import services.llm as llm

st.set_page_config(page_title="AI Copilot MVP")
st.title("AI Copilot")

conversation.inicializar_estado(st.session_state)

# Mostrar historial
for mensaje in st.session_state.messages:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# Manejar nuevo mensaje
if prompt := st.chat_input("Escribe aquí..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    conversation.agregar_mensaje(st.session_state, "user", prompt)

    with st.chat_message("assistant"):
        contenedor = st.empty()
        contenedor.markdown("Pensando...")
        try:
            inicio = time.time()
            # Preparar contexto y llamar a Groq
            historial = conversation.obtener_historial_truncado(st.session_state)
            mensajes = prompting.construir_prompt_con_historial(historial)

            respuesta = llm.client.chat.completions.create(
                messages=mensajes,
                model=llm.MODELO,
                temperature=0.7
            ).choices[0].message.content

            fin = time.time()
            contenedor.markdown(respuesta)
            st.caption(f"Tiempo de respuesta: {fin - inicio:.2f}s")
            conversation.agregar_mensaje(st.session_state, "assistant", respuesta)

        except Exception as e:
            contenedor.error(f"Error: {e}")