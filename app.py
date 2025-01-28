import streamlit as st
import replicate
import os
from dotenv import load_dotenv
import requests
import time
from PIL import Image
from io import BytesIO

# 앱 시작 시 세션 초기화
if 'initialized' not in st.session_state:
   st.session_state.initialized = True
   if 'api_key_input' in st.session_state:
       del st.session_state.api_key_input
   if 'prompt_input' in st.session_state:
       del st.session_state.prompt_input

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
           border-radius: 8px;
           padding: 0.75rem 1rem;
           width: 100%;
       }
       .stButton>button:hover {
           background-color: #FF3333;
       }
       .stTextInput>div>div>input, .stTextArea>div>div>textarea {
           background-color: #1E1E1E;
           color: white;
           border: 1px solid #333;
           border-radius: 8px;
       }
       .stSlider>div>div>div {
           background-color: #FF4B4B;
       }
       .stSelectbox>div>div {
           background-color: #1E1E1E;
           border: 1px solid #333;
           border-radius: 8px;
       }
       .stAlert {
           background-color: rgba(255, 75, 75, 0.1);
           border: 1px solid #FF4B4B;
           border-radius: 8px;
           padding: 1rem;
       }
       .streamlit-expanderHeader {
           background-color: #1E1E1E;
           border: 1px solid #333;
           border-radius: 8px;
       }
       .css-1d391kg {
           background-color: #1E1E1E;
       }
       hr {
           border-color: #333;
       }
   </style>
""", unsafe_allow_html=True)

# 메인 영역
st.title("AI Sticker Maker 🎨")
st.markdown("Generate unique stickers using AI! Just enter a description and customize your settings.")

# 사이드바 설정
with st.sidebar:
   st.header("Settings")
   
   # API 키 입력 - 초기값을 빈 값으로 설정하고 key 파라미터 추가
   api_key = st.text_input(
       "Replicate API Key",
       value="",  # 빈 값으로 초기화
       type="password",
       help="Get your API key from https://replicate.com/account",
       placeholder="r8_xxxx...",
       key="api_key_input"  # 고유 키 설정
   )
   
   st.markdown("---")
   
   st.header("Sticker Settings")
   
   # 프롬프트 입력 - 초기값을 빈 값으로 설정하고 key 파라미터 추가
   prompt = st.text_area(
       "Description",
       value="",  # 빈 값으로 초기화
       placeholder="Enter a description (e.g., a cute nurse)",
       help="Describe what you want your sticker to look like",
       key="prompt_input"  # 고유 키 설정
   )
   
   # 품질 설정
   steps = st.slider(
       "Quality Steps",
       min_value=10,
       max_value=50,
       value=20,
       help="Higher values = better quality but slower",
       key="steps_slider"  # 고유 키 설정
   )
   
   # 크기 설정
   size_option = st.selectbox(
       "Sticker Size",
       options=["Small (576x576)", "Medium (768x768)", "Large (1152x1152)"],
       index=1,
       key="size_select"  # 고유 키 설정
   )
   
   size_map = {
       "Small (576x576)": 576,
       "Medium (768x768)": 768,
       "Large (1152x1152)": 1152
   }
   image_size = size_map[size_option]

# 생성 버튼
if st.button("Generate Sticker", type="primary"):
   if not api_key:
       st.error("⚠️ Please enter your Replicate API key first!")
   elif not prompt:
       st.error("⚠️ Please enter a description for your sticker!")
   else:
       try:
           with st.spinner("✨ Creating your sticker... Please wait..."):
               headers = {"Authorization": f"Token {api_key}"}
               
               response = requests.post(
                   "https://api.replicate.com/v1/predictions",
                   headers=headers,
                   json={
                       "version": "4acb778eb059772225ec213948f0660867b2e03f277448f18cf1800b96a65a1a",
                       "input": {
                           "prompt": prompt,
                           "steps": steps,
                           "width": image_size,
                           "height": image_size,
                           "output_format": "png",
                           "output_quality": 100,
                           "negative_prompt": "",
                           "number_of_images": 1
                       }
                   }
               )
               
               if response.status_code != 201:
                   st.error(f"Error: {response.text}")
                   st.stop()

               prediction = response.json()
               
               while prediction['status'] not in ['succeeded', 'failed']:
                   time.sleep(1)
                   response = requests.get(
                       f"https://api.replicate.com/v1/predictions/{prediction['id']}",
                       headers=headers
                   )
                   prediction = response.json()
               
               if prediction['status'] == 'succeeded':
                   image_url = prediction['output'][0]
                   img_response = requests.get(image_url)
                   
                   if img_response.status_code == 200:
                       st.success("✅ Sticker generated successfully!")
                       
                       col1, col2, col3 = st.columns([1, 2, 1])
                       with col2:
                           st.image(img_response.content, caption="Your Generated Sticker", use_column_width=True)
                           
                           st.download_button(
                               label="⬇️ Download Sticker",
                               data=img_response.content,
                               file_name="ai_sticker.png",
                               mime="image/png",
                               use_container_width=True
                           )
                   else:
                       st.error("Failed to download the generated image.")
               else:
                   st.error(f"Generation failed: {prediction.get('error', 'Unknown error')}")
                   
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

# 푸터
st.markdown("---")
st.markdown("Made with ❤️ using Replicate's Sticker Maker API")
