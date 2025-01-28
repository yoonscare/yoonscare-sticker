import streamlit as st
import replicate
import os
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO

# 페이지 설정
st.set_page_config(
    page_title="AI Sticker Maker",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
    <style>
        .stApp {
            background-color: #1A1C1D;
            color: white;
        }
        .stButton>button {
            background-color: #FF4B4B;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
        }
        .stButton>button:hover {
            background-color: #FF3333;
        }
        .sidebar .sidebar-content {
            background-color: #2E2E2E;
        }
        .stTextInput>div>div>input {
            background-color: #2E2E2E;
            color: white;
        }
        .stExpander {
            background-color: #2E2E2E;
        }
    </style>
""", unsafe_allow_html=True)

# 메인 영역
st.title("AI Sticker Maker 🎨")
st.markdown("Generate unique stickers using AI! Just enter a description and customize your settings.")

# 사이드바 설정
with st.sidebar:
    st.header("Settings")
    
    # API 키 입력
    api_key = st.text_input(
        "Replicate API Key",
        type="password",
        help="Get your API key from https://replicate.com/account",
        placeholder="r8_xxxx..."
    )
    
    st.markdown("---")
    
    # 스티커 설정
    st.header("Sticker Settings")
    
    # 프롬프트 입력
    prompt = st.text_area(
        "Description",
        placeholder="Enter a description (e.g., a cute nurse)",
        help="Describe what you want your sticker to look like"
    )
    
    # 품질 설정
    steps = st.slider(
        "Quality Steps",
        min_value=10,
        max_value=50,
        value=20,
        help="Higher values = better quality but slower"
    )
    
    # 크기 설정
    size_option = st.selectbox(
        "Sticker Size",
        options=["Small (576x576)", "Medium (768x768)", "Large (1152x1152)"],
        index=1
    )
    
    size_map = {
        "Small (576x576)": 576,
        "Medium (768x768)": 768,
        "Large (1152x1152)": 1152
    }
    image_size = size_map[size_option]

# 생성 버튼
if st.button("Generate Sticker", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ Please enter your Replicate API key first!")
    elif not prompt:
        st.error("⚠️ Please enter a description for your sticker!")
    else:
        try:
            with st.spinner("✨ Creating your sticker... Please wait..."):
                os.environ["REPLICATE_API_TOKEN"] = api_key
                
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
                
                image_url = str(output[0])
                response = requests.get(image_url)
                
                if response.status_code == 200:
                    st.success("✅ Sticker generated successfully!")
                    
                    # 이미지 표시를 중앙에 배치
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.image(response.content, caption="Your Generated Sticker")
                        
                        # 다운로드 버튼
                        st.download_button(
                            label="⬇️ Download Sticker",
                            data=response.content,
                            file_name="ai_sticker.png",
                            mime="image/png",
                            use_container_width=True
                        )
                else:
                    st.error("Failed to download the generated image.")
                    
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# 사용 방법
with st.expander("How to Use"):
    st.markdown("""
    1. Get your Replicate API key from [replicate.com/account](https://replicate.com/account)
    2. Enter your API key in the sidebar
    3. Write a detailed description of the sticker you want
    4. Adjust quality and size settings
    5. Click 'Generate Sticker' and wait for the magic!
    6. Download your sticker when ready
    """)

st.markdown("---")
st.markdown("Made with ❤️ using Replicate's Sticker Maker API")
