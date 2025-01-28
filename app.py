import streamlit as st
import replicate
import os
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="AI Sticker Maker",
    page_icon="🎨",
    layout="centered"
)

# Add title and description
st.title("AI Sticker Maker 🎨")
st.markdown("Generate unique stickers using AI! Just enter a description and customize your settings.")

# Initialize session state for the generated image
if 'generated_image_url' not in st.session_state:
    st.session_state.generated_image_url = None

# Sidebar for inputs
with st.sidebar:
    st.header("Sticker Settings")
    
    # Input for prompt
    prompt = st.text_area(
        "Description",
        placeholder="Enter a description (e.g., a cute cat playing with yarn)",
        help="Describe what you want your sticker to look like"
    )
    
    # Slider for steps
    steps = st.slider(
        "Generation Steps",
        min_value=10,
        max_value=50,
        value=20,
        help="Higher values generally result in better quality but take longer"
    )
    
    # Image size selection
    size_option = st.selectbox(
        "Image Size",
        options=["Small (576x576)", "Medium (768x768)", "Large (1152x1152)"],
        index=1
    )
    
    # Convert size option to dimensions
    size_map = {
        "Small (576x576)": 576,
        "Medium (768x768)": 768,
        "Large (1152x1152)": 1152
    }
    image_size = size_map[size_option]

# Generate button
if st.button("Generate Sticker", type="primary", use_container_width=True):
    if not prompt:
        st.error("Please enter a description for your sticker!")
    else:
        try:
            with st.spinner("✨ Generating your sticker... This may take a minute..."):
                # Set up your Replicate API token
                os.environ["REPLICATE_API_TOKEN"] = "r8_Qk1zrKnhQuqxS5xLYYpYLGnp89GZ4HM1Ka83F"
                
                # Generate the image
                output = replicate.run(
                    "fofr/sticker-maker:4acb778eb059772225ec213948f0660867b2e03f277448f18cf1800b96a65a1a",
                    input={
                        "prompt": prompt,
                        "steps": steps,
                        "width": image_size,
                        "height": image_size,
                        "output_format": "png",
                        "output_quality": 100,
                        "negative_prompt": "",
                        "number_of_images": 1
                    }
                )
                
                # Get the image URL
                image_url = str(output[0])
                st.session_state.generated_image_url = image_url
                
                # Download and display the image
                response = requests.get(image_url)
                if response.status_code == 200:
                    # Display the generated image
                    st.image(response.content, caption="Your Generated Sticker")
                    
                    # Add download button
                    st.download_button(
                        label="Download Sticker",
                        data=response.content,
                        file_name="ai_sticker.png",
                        mime="image/png"
                    )
                else:
                    st.error("Failed to download the generated image.")
                    
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Display usage instructions
with st.expander("How to Use"):
    st.markdown("""
    1. Enter a detailed description of the sticker you want to create
    2. Adjust the generation steps (higher values = better quality but slower)
    3. Select your preferred image size
    4. Click 'Generate Sticker' and wait for the magic to happen!
    5. Download your sticker when it's ready
    """)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Replicate's Sticker Maker API")
