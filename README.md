# MVP: AI Copilot (Prueba Técnica)

Este repositorio contiene el MVP (Minimum Viable Product) de un chatbot ("AI Copilot") desarrollado en 5 días. El objetivo principal fue demostrar la capacidad de integrar un LLM de forma robusta, con una lógica de conversación coherente, manejo de errores y despliegue en la nube.

**URL de la Demo (Streamlit Cloud):**
[https://ai-copilot-mvp-cettez3y44ydsqkpxumuwuj.streamlit.app](https://ai-copilot-mvp-cettez3y44ydsqkpxumuwuj.streamlit.app)

---

## 1. Stack Técnico y Decisiones (Trade-offs)

* **Proveedor LLM: Groq**
    * **Justificación:** Se eligió Groq por su velocidad de inferencia (latencia p95 < 0.6s), superando a otras APIs. Su compatibilidad con la API de OpenAI y su generosa capa gratuita lo hicieron ideal para un MVP rápido.
    * **Modelo:** `llama-3.1-8b-instant`. Se seleccionó este modelo ligero tras encontrar límites de tasa (Error 429) en el modelo `70b`, garantizando la disponibilidad de la demo.

* **Framework UI: Streamlit**
    * **Justificación:** Se prefirió Streamlit sobre Gradio por su rapidez para construir interfaces de chat. `st.session_state` permitió un manejo de estado (historial, contador de turnos) simple y eficaz sin necesidad de un backend o base de datos.

* **Robustez: Tenacity**
    * **Justificación:** Se implementó `tenacity` en el cliente LLM (`services/llm.py`) para manejar fallos de red y errores de servidor (5xx), cumpliendo el requisito de robustez.

---

## 2. Parámetros de Inferencia y Lógica

### Parámetros de API
La llamada a la API de Groq está configurada con los siguientes parámetros para equilibrar creatividad y consistencia:

* **`model`**: `llama-3.1-8b-instant`
* **`temperature`**: `0.7` (ligeramente creativo)
* **`max_tokens`**: `1024` (limita el costo y el abuso)
* **`top_p`**: `0.8` (evita tokens muy improbables)
* **`seed`**: `42` (permite respuestas reproducibles para propósitos de prueba)
* **`timeout`**: `12.0` (cumple el requisito de timeout <= 12s)

### Lógica Conversacional
El flujo de la conversación se maneja en la carpeta `core/`:

1.  **System Prompt (`prompting.py`):** Se define un rol claro ("AI Copilot, un asistente útil...") que se inyecta al inicio de cada conversación.
2.  **Truncado de Historial (`conversation.py`):** Para mantener el contexto relevante y controlar el costo de tokens, el bot solo recuerda los últimos **10 turnos** (5 del usuario, 5 del asistente).
3.  **Límite de Sesión (`conversation.py`):** La demo tiene un límite de **20 turnos** por sesión, con un indicador visual en la barra lateral.
4.  **Intents Simples (`app/web.py`):** El bot reconoce comandos especiales:
    * `/nota` y `/recordatorio`: Se manejan localmente sin llamar al LLM, ahorran tokens y se guardan en la barra lateral.
    * `/busqueda`: Llama al LLM pero usa un `SYSTEM_PROMPT` diferente para forzar una respuesta directa, tipo buscador.

---

## 3. Pruebas y Robustez

El proyecto incluye **9 pruebas unitarias** (`pytest`) que cubren la lógica central y el cliente de servicios.

* **`tests/test_core.py` (6 Pruebas):**
    * Verifican que el `System Prompt` se añada correctamente.
    * Aseguran que el truncado de historial (`MAX_HISTORIAL`) funciona.
    * Confirman que el contador de turnos (`MAX_TURNOS`) solo se incrementa con entradas del usuario.
    * Validan que los intents `/nota` y `/recordatorio` guardan correctamente.

* **`tests/test_services.py` (3 Pruebas):**
    * **Manejo de Errores 4xx vs 5xx:** Las pruebas simulan fallos de API (`pytest-mock`).
    * **Fallo 400 (Bad Request):** La prueba confirma que la app falla **inmediatamente** (1 solo intento), como lo pide la rúbrica.
    * **Fallo 500 (Server Error):** La prueba confirma que la app **reintenta 3 veces** con *backoff* exponencial antes de fallar.

---

## 4. Métricas de Desempeño

Métricas recopiladas desde la URL pública (`llama-3.1-8b-instant`):

* **Tokens Usados:** La app rastrea y muestra el total de tokens (prompt + respuesta) consumidos por sesión en la barra lateral.
* **Latencia p50 (Mediana):** 0.17s
* **Latencia Promedio:** 0.29s
* **Latencia p95 (Peor caso):** 0.58s
* **Latencia de Intent local (`/nota`):** 0.12s

---

## 5. Limitaciones y Mejoras

* **Límites de Tasa (Rate Limit):** Durante el desarrollo con el modelo `70b`, se encontró un límite de tasa (Error 429). La solución fue cambiar al modelo `8b`. Una mejora sería implementar un *fallback* a otro proveedor de API si Groq falla.
* **Guardrails:** No se implementó un filtro de "solicitud insegura". El bot podría intentar responder a contenido inapropiado.
* **Tasa de Reintentos:** Esta métrica no se reporta. Implementarla requeriría un sistema de *logging* complejo, considerado fuera del alcance del MVP.
* **Persistencia:** El historial de chat y las notas se pierden si se recarga la página, ya que se guardan en `st.session_state`. Una mejora sería conectar una base de datos simple.

---

## 6. Cómo ejecutar localmente

1.  Clonar el repositorio:
    ```bash
    git clone [https://github.com/Fernandohj/ai-copilot-mvp.git](https://github.com/Fernandohj/ai-copilot-mvp.git)
    cd ai-copilot-mvp
    ```
2.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```
3.  Configurar la clave de API:
    * Renombrar `.env.example` a `.env`
    * Pegar tu API Key de Groq dentro del archivo `.env`
4.  Ejecutar la app:
    ```bash
    streamlit run app/web.py
    ```
5.  (Opcional) Correr las pruebas:
    ```bash
    pytest
    ```