from core.prompting import construir_prompt_con_historial, SYSTEM_PROMPT

def test_construir_prompt_agrega_system():
    historial_vacio = []
    resultado = construir_prompt_con_historial(historial_vacio)
    # Debe tener al menos 1 mensaje: el del sistema
    assert len(resultado) == 1
    assert resultado[0]["role"] == "system"
    assert resultado[0]["content"] == SYSTEM_PROMPT

def test_construir_prompt_mantiene_orden():
    historial = [
        {"role": "user", "content": "Hola"},
        {"role": "assistant", "content": "Hola, ¿en qué ayudo?"}
    ]
    resultado = construir_prompt_con_historial(historial)
    # Debe tener 3 mensajes: system + user + assistant
    assert len(resultado) == 3
    assert resultado[0]["role"] == "system"
    assert resultado[1]["role"] == "user"
    assert resultado[2]["role"] == "assistant"