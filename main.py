import streamlit as st
import requests
from PIL import Image
import io

# Hugging Face API
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {
    "Authorization": "Bearer YOUR_HF_API_KEY"
}

def generate_image(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

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

            image_bytes = generate_image(prompt)

            image = Image.open(io.BytesIO(image_bytes))

            st.image(image, caption="Generated Image", use_column_width=True)

            st.download_button(
                label="Download Image",
                data=image_bytes,
                file_name="generated_image.png",
                mime="image/png"
            )
