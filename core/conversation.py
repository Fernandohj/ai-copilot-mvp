MAX_HISTORIAL = 10
MAX_TURNOS = 20  # Límite requerido por la rúbrica

def inicializar_estado(st_session_state):
    """Inicializa el historial y contadores si no existen."""
    if "messages" not in st_session_state:
        st_session_state.messages = []
    if "turn_count" not in st_session_state:
        st_session_state.turn_count = 0
    if "notas" not in st_session_state:
        st_session_state.notas = []

def agregar_mensaje(st_session_state, role: str, content: str):
    """Guarda un mensaje e incrementa el contador de turnos si es el usuario."""
    st_session_state.messages.append({"role": role, "content": content})
    if role == "user":
        st_session_state.turn_count += 1

def obtener_historial_truncado(st_session_state):
    """Devuelve los últimos N mensajes."""
    return st_session_state.messages[-MAX_HISTORIAL:]

def guardar_nota(st_session_state, nota: str) -> str:
    """Maneja el intent simple /nota sin llamar al LLM."""
    st_session_state.notas.append(nota)
    return f"📝 Nota guardada: '{nota}'"