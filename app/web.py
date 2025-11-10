import streamlit as st

# Título de la aplicación
st.title("Mi AI Copilot")

# Un mensaje de bienvenida simple
st.write("¡Hola mundo! Esta es la primera versión de mi asistente inteligente.")

# Un pequeño input para probar que interactúa
nombre = st.text_input("¿Cómo te llamas?")
if nombre:
    st.write(f"¡Mucho gusto, {nombre}! Pronto podré ayudarte con muchas más cosas.")