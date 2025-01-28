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
        /* 전체 배경 */
        .stApp {
            background-color: #1A1C1D;
            color: white;
        }
        
        /* 버튼 스타일 */
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
        
        /* 입력 필드 스타일 */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #1E1E1E;
            color: white;
            border: 1px solid #333;
            border-radius: 8px;
        }
        
        /* 슬라이더 스타일 */
        .stSlider>div>div>div {
            background-color: #FF4B4B;
        }
        
        /* 셀렉트박스 스타일 */
        .stSelectbox>div>div {
            background-color: #1E1E1E;
            border: 1px solid #333;
            border-radius: 8px;
        }
        
        /* 에러 메시지 스타일 */
        .stAlert {
            background-color: rgba(255, 75, 75, 0.1);
            border: 1px solid #FF4B4B;
            border-radius: 8px;
            padding: 1rem;
        }
        
        /* 익스팬더 스타일 */
        .streamlit-expanderHeader {
            background-color: #1E1E1E;
            border: 1px solid #333;
            border-radius: 8px;
        }
        
        /* 사이드바 스타일 */
        .css-1d391kg {
            background-color: #1E1E1E;
        }
        
        /* 구분선 스타일 */
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

# 나머지 코드는 동일하게 유지...
