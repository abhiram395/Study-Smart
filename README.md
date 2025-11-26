# 📚 Exam Question Predictor & Study Plan Generator

An AI-powered application that analyzes previous year question papers and syllabus to generate a smart, prioritized study plan. It uses semantic analysis to identify key topics and Generative AI to provide model answers.

## 🌟 Features

*   **Smart Study Plan**: Prioritizes topics based on historical frequency and weightage.
*   **AI Answer Key**: Generates academic-style model answers for any question using Google Gemini.
*   **Syllabus Mapping**: Automatically tags questions with relevant syllabus topics.
*   **Multi-Format Support**: Works with PDFs and Images (JPG/PNG).
*   **Auto-Fetch**: Can search and download question papers from the web automatically.
*   **Study Material Finder**: Finds relevant tutorials and articles for high-priority topics.

## 🚀 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/question-predictor.git
    cd question-predictor
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Tesseract OCR**:
    *   **Windows**: Download and install from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki).
    *   **Linux (Debian/Ubuntu)**:
        ```bash
        sudo apt-get update
        sudo apt-get install tesseract-ocr
        sudo apt-get install poppler-utils
        ```
    *   **Mac**:
        ```bash
        brew install tesseract
        brew install poppler
        ```

4.  **Get a Gemini API Key**:
    *   Get a free API key from [Google AI Studio](https://aistudio.google.com/).

## 🏃‍♂️ Usage

1.  Run the Streamlit app:
    ```bash
    streamlit run main.py
    ```

2.  **Upload Syllabus**: Upload your syllabus PDF or Image.
3.  **Upload Papers**: Upload previous year question papers OR use "Auto-Fetch".
4.  **Analyze**: Click "Analyze & Predict".
5.  **Study**: Review the prioritized topics, generate answers, and access study materials.

## 🛠️ Tech Stack

*   **Frontend**: Streamlit
*   **AI/NLP**: Sentence-Transformers, BERTopic, Google Gemini
*   **OCR**: Tesseract, PDF2Image
*   **Scraping**: Google Search API, Requests

## 📝 License

MIT License
