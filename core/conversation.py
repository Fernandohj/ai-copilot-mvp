MAX_HISTORIAL = 10

def inicializar_estado(st_session_state):
    """Inicializa el historial si no existe."""
    if "messages" not in st_session_state:
        st_session_state.messages = []

def agregar_mensaje(st_session_state, role: str, content: str):
    """Guarda un mensaje en el historial."""
    st_session_state.messages.append({"role": role, "content": content})

def obtener_historial_truncado(st_session_state):
    """Devuelve los últimos N mensajes."""
    return st_session_state.messages[-MAX_HISTORIAL:]