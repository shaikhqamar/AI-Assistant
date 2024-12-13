import re
import streamlit as st
from PIL import Image
import pyttsx3
from gtts import gTTS
import io
import os
import pytesseract
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class VisionAssist:
    def __init__(self):
        # Initialize Google Generative AI with API Key
        self.GEMINI_API_KEY = 'Your Api Key'
        os.environ["GOOGLE_API_KEY"] = self.GEMINI_API_KEY
        self.llm = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=self.GEMINI_API_KEY)

        # Initialize Text-to-Speech engine
        self.engine = pyttsx3.init()

    def extract_text_from_image(self, image):
        """Extracts text from the given image using OCR."""
        return pytesseract.image_to_string(image)

    def text_to_speech(self, content):
        """Converts the given text to speech."""
        try:
            tts = gTTS(text=content, lang='en')
            audio_stream = io.BytesIO()
            tts.write_to_fp(audio_stream)
            audio_stream.seek(0)  # Reset stream pointer to the beginning
            return audio_stream
        except Exception as e:
            st.error(f"Error: {e}")
            return None

    def generate_scene_description(self, input_prompt, image_data):
        """Generates a scene description using Google Generative AI."""
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content([input_prompt, image_data[0]])
        return response.text if hasattr(response, 'text') else "No valid response text"

    def input_image_setup(self, uploaded_file):
        """Prepares the uploaded image for processing."""
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            image_parts = [
                {
                    "mime_type": uploaded_file.type,
                    "data": bytes_data,
                }
            ]
            return image_parts
        else:
            raise FileNotFoundError("No file uploaded.")

    def extract_overall_description(self,content):
        """
        Extracts the 'Overall description' section from the given content
        and removes special characters like *, **, and extra whitespaces.
        """
        # Match the "Overall description" paragraph
        match = re.search(r"2\.\s\*\*Overall description:\*\*(.*?)(?:\n\n|\Z)", content, re.S)
        if match:
            description = match.group(1).strip()
            # Remove markdown formatting (e.g., **, *, etc.)
            description = re.sub(r"[\*]+", "", description)
            description = re.sub(r"\s{2,}", " ", description)  # Normalize extra spaces
            return description
        return "No overall description found."


# Initialize VisionAssist
vision_assist = VisionAssist()

# Page Configurations
st.set_page_config(
    page_title="VisionAssist",
    layout="wide",
    page_icon="👁️",
)

# CSS Styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #0052cc;
        margin-top: -10px;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 20px;
        color: #666;
        text-align: center;
        margin-bottom: 30px;
    }
    .feature-header {
        font-size: 24px;
        color: #333;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .footer {
        text-align: center;
        font-size: 14px;
        color: #888;
        margin-top: 20px;
    }
    .sidebar-text {
        font-size: 16px;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.markdown('<div class="main-title">VisionAssist 👁️</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI for Scene Understanding, Text Extraction & Speech for the Visually Impaired 🗣️</div>',
    unsafe_allow_html=True,
)

# Sidebar Features
st.sidebar.image(
    r"StaticFiles/inno_black_logo-removebg-preview.png",
    caption="Innomatics Research Labs",
    use_container_width=True,
)

st.sidebar.title("ℹ️ About")
st.sidebar.markdown(
    """
    <div class="sidebar-text">
    📌 **Features** :\n
    - 🔍 **Describe Scene**: Get AI insights about the image, including objects and suggestions.\n
    - 🗋 **Extract Text**: Extract visible text using OCR.\n
    - 🔊 **Text-to-Speech**: Hear the extracted text aloud.\n

    💡 **How it helps**:
    Assists visually impaired users by providing scene descriptions, text extraction, and speech.

    🤖 **Powered by**:
    - **Google Gemini API** for scene understanding.
    - **Tesseract OCR** for text extraction.
    - **pyttsx3** for text-to-speech.
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("📜 Instructions")
st.sidebar.text_area(
    "How to use:",
    "1. Upload an image.\n"
    "2. Choose a feature to interact with:\n"
    "   - 🔍 Describe the Scene\n"
    "   - 🗋 Extract Text\n"
    "   - 🔊 Listen to Text",
    height=150,
)

# Upload Image Section
st.markdown("<h3 class='feature-header'>📄 Upload an Image</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop or browse an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Buttons Section
st.markdown("<h3 class='feature-header'>⚙️ Features</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

scene_button = col1.button("🔍 Describe Scene")
ocr_button = col2.button("🗋 Extract Text")
tts_button = col3.button("🔊 Text-to-Speech")

# Input Prompt for Scene Understanding
input_prompt = """
You are an AI assistant helping visually impaired individuals by describing the scene in the image. Provide:
1. List of items detected in the image with their purpose.
2. Overall description of the image.
3. Suggestions for actions or precautions for the visually impaired.
"""

content = ""  # Initialize content variable

# Process user interactions
if uploaded_file:
    try:
        image_data = vision_assist.input_image_setup(uploaded_file)

        # Ensure `content` exists in session state
        if "content" not in st.session_state:
            st.session_state["content"] = ""

        if scene_button:
            with st.spinner("Generating scene description..."):
                st.session_state["content"] = vision_assist.generate_scene_description(input_prompt, image_data)
                st.markdown("<h3 class='feature-header'>🔍 Scene Description</h3>", unsafe_allow_html=True)
                st.write(st.session_state["content"])
                #print(st.session_state["content"])

        if ocr_button:
            with st.spinner("Extracting text from the image..."):
                st.session_state["content"] = vision_assist.extract_text_from_image(image)
                st.markdown("<h3 class='feature-header'>📝 Extracted Text</h3>", unsafe_allow_html=True)
                st.text_area("Extracted Text", st.session_state["content"], height=150)

        # Corrected Code for Text-to-Speech (TTS) Section
        if tts_button:
            # Extract "Overall description" from content
            if st.session_state.get("content"):
                st.session_state['overall_description'] = vision_assist.extract_overall_description(st.session_state["content"])
                if st.session_state['overall_description'] and st.session_state['overall_description'] != "No overall description found.":
                    # Only attempt TTS if there is a valid description
                    audio_stream = vision_assist.text_to_speech(st.session_state["overall_description"])
                    if audio_stream:
                        st.audio(audio_stream, format="audio/mp3")
                        st.success("✅ Text-to-Speech Conversion Completed!")
                    else:
                        st.error("Failed to generate audio.")
                else:
                    st.warning("No valid 'Overall Description' to convert.")
            else:
                st.warning("Content not available for conversion.")
    except Exception as e:
        st.error(f"An error occurred: {e}")


# Footer
st.markdown(
    """
    <hr>
    <footer class="footer">
        Powered by <strong>Google Gemini API</strong> | ©゠ MD QAMAR | Built with ❤️ using Streamlit
    </footer>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <hr>
    <footer class="footer">
        Powered by <strong>Google Gemini API</strong> | ©゠ MD QAMAR | Built with ❤️ using Streamlit
    </footer>
    """,
    unsafe_allow_html=True,
)
