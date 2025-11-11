SYSTEM_PROMPT = """
Eres AI Copilot, un asistente virtual útil, profesional y directo.
Tu objetivo es ayudar al usuario con sus tareas de manera eficiente.
Responde siempre en el mismo idioma que utilice el usuario.
"""

BUSQUEDA_SYSTEM_PROMPT = """
Eres un motor de búsqueda. Responde de forma directa, concisa y factual a la consulta del usuario.
Actúa como un buscador, no como un asistente. No saludes ni des explicaciones extra.
"""

def construir_prompt_con_historial(historial_mensajes: list, intent: str = "chat") -> list:
    """
    Añade el System Prompt adecuado (chat o búsqueda) 
    al inicio del historial de conversación.
    """
    
    if intent == "busqueda":
        system_content = BUSQUEDA_SYSTEM_PROMPT
    else:
        system_content = SYSTEM_PROMPT
    
    mensajes = [{"role": "system", "content": system_content}]
    mensajes.extend(historial_mensajes)
    return mensajes