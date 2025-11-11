SYSTEM_PROMPT = """
Eres AI Copilot, un asistente virtual útil, profesional y directo.
Tu objetivo es ayudar al usuario con sus tareas de manera eficiente.
Responde siempre en el mismo idioma que utilice el usuario.
"""

def construir_prompt_con_historial(historial_mensajes: list) -> list:
    """Añade el System Prompt al inicio del historial de conversación."""
    mensajes = [{"role": "system", "content": SYSTEM_PROMPT}]
    mensajes.extend(historial_mensajes)
    return mensajes