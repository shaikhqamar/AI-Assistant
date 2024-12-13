# VisionAssist

**VisionAssist** is an AI-powered application designed to help visually impaired individuals interact with their environment. The app provides scene understanding, text extraction from images, and text-to-speech conversion, all in real time. It utilizes cutting-edge technologies like **Google Gemini API**, **Tesseract OCR**, and **pyttsx3** to create an accessible interface using **Streamlit**.

## Features

- **Scene Understanding**: Uses AI to describe the contents of an image, identify objects, and provide suggestions for the user.
- **Text Extraction**: Extracts visible text from images using **Tesseract OCR**.
- **Text-to-Speech**: Converts the extracted or generated text into speech for better accessibility using **pyttsx3** and **gTTS**.

## Technologies Used

- **Google Gemini API**: For scene understanding and generating image descriptions.
- **Tesseract OCR**: For extracting text from images.
- **pyttsx3**: For offline text-to-speech conversion.
- **gTTS**: For online text-to-speech conversion.
- **Streamlit**: For building the web interface.

## How It Works

1. **Upload an Image**: The user uploads an image for processing.
2. **Select a Feature**:
    - **Describe the Scene**: AI generates a description of the scene, identifying key objects and suggesting actions.
    - **Extract Text**: Extracts any text present in the image using OCR.
    - **Text-to-Speech**: Converts the extracted or generated text into speech.
3. **Listen to Descriptions**: The app reads aloud the text or description from the image, enabling visually impaired users to access the content.

## Installation

To run **VisionAssist** locally, you need to have Python installed on your system. Then, install the required dependencies:

```bash
pip install streamlit pyttsx3 gtts pytesseract google-generativeai langchain_google_genai
```

Make sure you have Tesseract OCR installed on your system. You can download it from [Tesseract OCR's official website](https://github.com/tesseract-ocr/tesseract).

## Usage

1. Clone this repository:
    ```bash
    git clone <repository-url>
    cd VisionAssist
    ```

2. Run the application:
    ```bash
    streamlit run app.py
    ```

3. Upload an image, select a feature (Describe Scene, Extract Text, Text-to-Speech), and interact with the AI assistant.

## Contributing

If you want to contribute to **VisionAssist**, feel free to fork this repository, create a new branch, and submit a pull request with your changes. Please make sure to follow the project's coding guidelines.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Built with ❤️ by **MD QAMAR** using **Streamlit**.
