import streamlit as st
import requests
from PIL import Image
import io

# Hugging Face API
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-2"

headers = {
    "Authorization": "Bearer hf_your_token_here"
}

def generate_image(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)

    # Check if response is an image
    if response.headers.get("content-type", "").startswith("image"):
        return response.content
    else:
        return None, response.text


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

            result = generate_image(prompt)

            if isinstance(result, tuple):
                st.error("API Error: " + result[1])
            else:
                image = Image.open(io.BytesIO(result))
                st.image(image, caption="Generated Image", use_column_width=True)

                st.download_button(
                    label="Download Image",
                    data=result,
                    file_name="generated_image.png",
                    mime="image/png"
                )
