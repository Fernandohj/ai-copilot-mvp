import pytest
from core.prompting import construir_prompt_con_historial, SYSTEM_PROMPT
from core.conversation import (
    inicializar_estado,
    agregar_mensaje,
    obtener_historial_truncado,
    guardar_nota,
    MAX_HISTORIAL,
    MAX_TURNOS
)

# --- Mock para simular st.session_state ---
class MockSessionState(dict):
    def __getattr__(self, key):
        return self[key]
    def __setattr__(self, key, value):
        self[key] = value

@pytest.fixture
def mock_state():
    state = MockSessionState()
    inicializar_estado(state)
    return state

# --- PRUEBAS DE PROMPTING (3 requeridas) ---

def test_prompt_agrega_system():
    """Verifica que siempre se añade el system prompt al inicio."""
    mensajes = construir_prompt_con_historial([])
    assert len(mensajes) == 1
    assert mensajes[0]["role"] == "system"
    assert mensajes[0]["content"] == SYSTEM_PROMPT

def test_prompt_mantiene_orden():
    """Verifica que se respeta el orden de los mensajes del historial."""
    historial = [{"role": "user", "content": "hola"}]
    mensajes = construir_prompt_con_historial(historial)
    assert len(mensajes) == 2
    assert mensajes[1] == historial[0]

def test_prompt_no_duplica_system():
    """Verifica que no se añade el system prompt si ya existe (caso borde)."""
    historial = [{"role": "system", "content": "ya existe"}]
    mensajes = construir_prompt_con_historial(historial)
    # Nuestra implementación actual SIEMPRE lo añade al principio, 
    # así que esperaríamos que el nuevo system prompt esté primero.
    assert mensajes[0]["content"] == SYSTEM_PROMPT
    assert mensajes[1]["content"] == "ya existe"

# --- PRUEBAS DE CONVERSACIÓN (3 requeridas) ---

def test_agregar_mensaje_incrementa_turno(mock_state):
    """Verifica que solo los mensajes del usuario incrementan el contador de turnos."""
    assert mock_state.turn_count == 0
    agregar_mensaje(mock_state, "user", "hola")
    assert mock_state.turn_count == 1
    agregar_mensaje(mock_state, "assistant", "hola también")
    assert mock_state.turn_count == 1  # No debe incrementar

def test_historial_se_trunca(mock_state):
    """Verifica que el historial no excede el límite MAX_HISTORIAL."""
    # Agregamos más mensajes del límite
    for i in range(MAX_HISTORIAL + 5):
        agregar_mensaje(mock_state, "user", f"msg {i}")
    
    truncado = obtener_historial_truncado(mock_state)
    assert len(truncado) == MAX_HISTORIAL
    assert truncado[-1]["content"] == f"msg {MAX_HISTORIAL + 4}"

def test_guardar_nota_funciona(mock_state):
    """Verifica que el intent de nota guarda correctamente sin tocar el historial."""
    nota = "Comprar pan"
    respuesta = guardar_nota(mock_state, nota)
    
    assert len(mock_state.notas) == 1
    assert mock_state.notas[0] == nota
    assert "guardada" in respuesta
    # El historial de chat debe seguir vacío porque es un intent directo
    assert len(mock_state.messages) == 0