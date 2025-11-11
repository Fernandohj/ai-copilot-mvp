import os
from groq import Groq
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("ERROR: No se encontró GROQ_API_KEY en .env")

client = Groq(api_key=api_key)
MODELO = "llama-3.3-70b-versatile"

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception)
)
def llamar_llm_robusto(prompt: str) -> str:
    """Llama a Groq con reintentos automáticos en caso de fallo."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODELO,
            temperature=0.7,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error en Groq: {e}")
        raise e

if __name__ == "__main__":
    # Prueba rápida si se ejecuta este archivo directamente
    print(llamar_llm_robusto("Di 'OK' si funciono."))