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

# --- Sidebar ---
with st.sidebar:
    st.header("Estado de Sesión")
    turnos_restantes = conversation.MAX_TURNOS - st.session_state.turn_count
    st.metric("Turnos restantes", turnos_restantes)
    
    st.metric("Tokens usados (sesión)", st.session_state.total_tokens)
    
    if st.session_state.notas:
        st.subheader("Mis Notas")
        for i, nota in enumerate(st.session_state.notas, 1):
            st.caption(f"{i}. {nota}")
            
    if st.session_state.recordatorios:
        st.subheader("Mis Recordatorios")
        for i, recordatorio in enumerate(st.session_state.recordatorios, 1):
            st.caption(f"{i}. {recordatorio}")

# --- Mostrar historial principal ---
for mensaje in st.session_state.messages:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# --- Manejo del Input del Usuario ---
if prompt := st.chat_input("Escribe aquí..."):
    if st.session_state.turn_count >= conversation.MAX_TURNOS:
        st.error("Has alcanzado el límite de turnos para esta sesión demo. Por favor, recarga la página para iniciar una nueva.")
        st.stop()

    with st.chat_message("user"):
        st.markdown(prompt)
    conversation.agregar_mensaje(st.session_state, "user", prompt)

    # Intents Simples
    if prompt.lower().startswith("/nota "):
        texto_nota = prompt[6:].strip()
        respuesta_nota = conversation.guardar_nota(st.session_state, texto_nota)
        with st.chat_message("assistant"):
            st.markdown(respuesta_nota)
        conversation.agregar_mensaje(st.session_state, "assistant", respuesta_nota)
        st.rerun()

    elif prompt.lower().startswith("/recordatorio "):
        texto_recordatorio = prompt[14:].strip()
        respuesta_recordatorio = conversation.guardar_recordatorio(st.session_state, texto_recordatorio)
        with st.chat_message("assistant"):
            st.markdown(respuesta_recordatorio)
        conversation.agregar_mensaje(st.session_state, "assistant", respuesta_recordatorio)
        st.rerun()

    # Flujo normal con LLM
    else:
        with st.chat_message("assistant"):
            contenedor = st.empty()
            contenedor.markdown("Pensando...")
            try:
                intent_actual = "chat"
                if prompt.lower().startswith("/busqueda "):
                    intent_actual = "busqueda"

                inicio = time.time()
                historial = conversation.obtener_historial_truncado(st.session_state)
                mensajes = prompting.construir_prompt_con_historial(historial, intent=intent_actual)

                respuesta_groq_obj = llm.client.chat.completions.create(
                    messages=mensajes,
                    model=llm.MODELO,
                    temperature=0.7,
                    max_tokens=1024,
                    top_p=0.8,
                    seed=42
                )
                
                texto_respuesta = respuesta_groq_obj.choices[0].message.content
                tokens_usados = respuesta_groq_obj.usage.total_tokens
                conversation.agregar_tokens(st.session_state, tokens_usados)

                fin = time.time()
                contenedor.markdown(texto_respuesta)
                st.caption(f"Tiempo de respuesta: {fin - inicio:.2f}s")
                conversation.agregar_mensaje(st.session_state, "assistant", texto_respuesta)

            except Exception as e:
                contenedor.error(f"Error: {e}")