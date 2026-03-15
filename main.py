import streamlit as st
import requests
from PIL import Image
import io
import os

# Hugging Face API
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"

# Read token from Hugging Face Space secret
HF_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def generate_image(prompt):
    payload = {"inputs": prompt}

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )

        # If request failed
        if response.status_code != 200:
            return None, response.text

        # If response is an image
        if response.headers.get("content-type", "").startswith("image"):
            return response.content, None   # FIXED

        return None, response.text

    except Exception as e:
        return None, str(e)


# Streamlit UI
st.set_page_config(page_title="AI Image Generator", page_icon="🎨")

st.title("🎨 Text to Image Generator")
st.write("Generate images using Generative AI (Stable Diffusion)")

prompt = st.text_input("Enter your prompt")

if st.button("Generate Image"):

    if prompt.strip() == "":
        st.warning("Please enter a prompt")

    else:
        with st.spinner("Generating image..."):

            image_bytes, error = generate_image(prompt)

            if image_bytes is None:
                st.error("API Error: " + error)

            else:
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption="Generated Image", use_column_width=True)

                st.download_button(
                    label="Download Image",
                    data=image_bytes,
                    file_name="generated_image.png",
                    mime="image/png"
                )
