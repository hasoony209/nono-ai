
import io
import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

st.set_page_config(page_title="Nono AI Chatbot", page_icon="✨", layout="centered")
st.title("✨ Nono AI Chatbot ✨")

GEMINI_API_KEY = "AQ.Ab8RN6JmmMbhfhk-Kcut0EjYceZDuIbMpew0EKvQq7_2Rzd7mw"
SYSTEM_PROMPT = "You are Nono, a playful, friendly, and educational AI assistant. Keep responses helpful and clear."

@st.cache_resource
def get_client():
    return genai.Client(api_key=GEMINI_API_KEY)

client = get_client()

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
                    result = client.models.generate_images(
                        model="imagen-3.0-generate-002",
                        prompt=user_input,
                        config=dict(number_of_images=1, aspect_ratio="1:1")
                    )
                    image_bytes = result.generated_images[0].image.image_bytes
                    img = Image.open(io.BytesIO(image_bytes))
                    st.image(img, use_container_width=True)
                    st.session_state.messages.append({"role": "assistant", "type": "image", "content": img})
                except Exception as e:
                    st.error(f"Could not generate image: {e}")
        else:
            with st.spinner("Nono is thinking..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=user_input,
                        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
                    )
                    st.write(response.text)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": response.text})
                except Exception as e:
                    st.error(f"Error: {e}")
