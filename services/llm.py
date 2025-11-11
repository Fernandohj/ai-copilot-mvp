import os
from groq import Groq, BadRequestError, InternalServerError, Timeout
from dotenv import load_dotenv
from tenacity import (
    retry, 
    stop_after_attempt, 
    wait_exponential, 
    retry_if_exception_type,
    RetryError
)

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("ERROR: No se encontró GROQ_API_KEY en .env")

client = Groq(api_key=api_key)
MODELO = "llama-3.1-8b-instant" 

@retry(
    stop=stop_after_attempt(3), # Límite de 2 reintentos (total 3 llamadas)
    wait=wait_exponential(multiplier=1, min=2, max=10), # Backoff exponencial
    
    # --- LA CORRECCIÓN ---
    # Le pasamos una tupla de los errores que SÍ queremos reintentar
    retry=retry_if_exception_type((InternalServerError, Timeout))
)
def llamar_llm_robusto(prompt: str) -> str:
    """Llama a Groq con reintentos inteligentes."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODELO,
            temperature=0.7,
            timeout=12.0 # Timeout de 12 segundos
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        # Volver a lanzar para que tenacity lo atrape
        raise e

if __name__ == "__main__":
    print(llamar_llm_robusto("Di 'OK' si funciono."))