import pytest
from groq import BadRequestError, InternalServerError, Timeout
from services.llm import llamar_llm_robusto, client
from tenacity import RetryError # Importar el error de reintento

def test_llm_exitoso(mocker):
    """Prueba el camino feliz: la API responde bien a la primera."""
    mock_message = mocker.Mock()
    mock_message.content = "Respuesta exitosa"
    mock_choice = mocker.Mock()
    mock_choice.message = mock_message
    mock_respuesta_completa = mocker.Mock()
    mock_respuesta_completa.choices = [mock_choice]
    
    mocker.patch.object(client.chat.completions, 'create', return_value=mock_respuesta_completa)
    
    respuesta = llamar_llm_robusto("test")
    assert respuesta == "Respuesta exitosa"
    client.chat.completions.create.assert_called_once()

def test_llm_reintenta_en_500_y_falla(mocker):
    """
    Prueba que SÍ reintenta en un error 500 y falla con RetryError.
    """
    mock_request = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.request = mock_request

    mocker.patch.object(
        client.chat.completions, 
        'create', 
        side_effect=InternalServerError(message="Error de servidor simulado", response=mock_response, body={})
    )
    
    # La lógica SÍ reintenta en 500, así que esperamos un RetryError
    with pytest.raises(RetryError):
        llamar_llm_robusto("test")
    
    # Verificar que se llamó 3 VECES
    assert client.chat.completions.create.call_count == 3

def test_llm_NO_reintenta_en_400(mocker):
    """
    Prueba que NO reintenta en un error 400.
    """
    mock_request = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.request = mock_request
    
    mocker.patch.object(
        client.chat.completions, 
        'create', 
        side_effect=BadRequestError(message="Error de cliente simulado", response=mock_response, body={})
    )
    
    # La lógica NO reintenta en 400, así que esperamos el error original
    with pytest.raises(BadRequestError):
        llamar_llm_robusto("test")
    
    # Verificar que se llamó SOLO 1 VEZ
    assert client.chat.completions.create.call_count == 1