import io
import streamlit as st
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="Nono AI Chatbot", page_icon="✨", layout="centered")
st.title("✨ Nono AI Chatbot ✨")

# Your AQ. key works directly here
GEMINI_API_KEY = "AQ.Ab8RN6JM8Zmz4jiWhiWyaW86xbeOqJvIAkKnnPmQeQA57dQypA"

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = "You are Nono, a playful, friendly, and educational AI assistant. Keep responses helpful and clear."

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "type": "text", "content": "Hey there! I am Nono! Ask me anything or tell me to draw something!"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.write(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"], use_container_width=True)

if user_input := st.chat_input("Ask Nono or tell him to draw something..."):
    st.session_state.messages.append({"role": "user", "type": "text", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    image_triggers = ["draw", "image of", "picture of", "generate image", "create picture", "show me a picture"]
    is_image_request = any(trigger in user_input.lower() for trigger in image_triggers)

    with st.chat_message("assistant"):
        if is_image_request:
            with st.spinner("Generating your picture... 🎨"):
                try:
                    imagen_model = genai.GenerativeModel("imagen-3.0-generate-002")
                    result = imagen_model.generate_images(prompt=user_input)
                    image_bytes = result.images[0]._image_bytes
                    img = Image.open(io.BytesIO(image_bytes))
                    st.image(img, use_container_width=True)
                    st.session_state.messages.append({"role": "assistant", "type": "image", "content": img})
                except Exception as e:
                    st.error(f"Could not generate image: {e}")
        else:
            with st.spinner("Nono is thinking..."):
                try:
                    chat_model = genai.GenerativeModel(
                        model_name="gemini-1.5-flash",
                        system_instruction=SYSTEM_PROMPT
                    )
                    response = chat_model.generate_content(user_input)
                    st.write(response.text)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": response.text})
                except Exception as e:
                    st.error(f"Error: {e}")
