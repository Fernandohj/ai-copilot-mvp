MAX_HISTORIAL = 10
MAX_TURNOS = 20

def inicializar_estado(session_state):
    """Inicializa el historial y contadores si no existen."""
    if "messages" not in session_state:
        session_state.messages = []
    if "turn_count" not in session_state:
        session_state.turn_count = 0
    if "notas" not in session_state:
        session_state.notas = []
    if "recordatorios" not in session_state:
        session_state.recordatorios = []
    if "total_tokens" not in session_state:
        session_state.total_tokens = 0

def agregar_mensaje(session_state, role: str, content: str):
    """Guarda un mensaje e incrementa el contador de turnos si es el usuario."""
    session_state.messages.append({"role": role, "content": content})
    if role == "user":
        session_state.turn_count += 1

def agregar_tokens(session_state, tokens: int):
    """Suma los tokens usados al total de la sesión."""
    session_state.total_tokens += tokens

def obtener_historial_truncado(session_state):
    """Devuelve los últimos N mensajes."""
    return session_state.messages[-MAX_HISTORIAL:]

def guardar_nota(session_state, nota: str) -> str:
    """Maneja el intent simple /nota sin llamar al LLM."""
    session_state.notas.append(nota)
    return f"Nota guardada: '{nota}'"

def guardar_recordatorio(session_state, recordatorio: str) -> str:
    """Maneja el intent simple /recordatorio sin llamar al LLM."""
    session_state.recordatorios.append(recordatorio)
    return f"Recordatorio guardado: '{recordatorio}'"