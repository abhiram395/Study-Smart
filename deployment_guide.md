# 🚀 Deployment Guide: How to Make Your App Public

This guide will help you host your **Question Predictor App** on the web for free using **Streamlit Cloud**.

## Prerequisites

1.  A **GitHub Account** ([Sign up here](https://github.com/join)).
2.  A **Streamlit Cloud Account** (Sign up with your GitHub account at [share.streamlit.io](https://share.streamlit.io/)).

---

## Step 1: Upload Your Code to GitHub

You need to put your code in a GitHub repository.

1.  **Initialize Git** (if you haven't already):
    Open your terminal in the project folder (`question_predictor`) and run:
    ```bash
    git init
    git add .
    git commit -m "Initial commit of Question Predictor App"
    ```

2.  **Create a New Repository on GitHub**:
    *   Go to [GitHub.com/new](https://github.com/new).
    *   Name it `question-predictor`.
    *   Select **Public**.
    *   Click **Create repository**.

3.  **Push Code**:
    *   Copy the commands under "…or push an existing repository from the command line".
    *   Run them in your terminal. They will look like this:
    ```bash
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/question-predictor.git
    git push -u origin main
    ```

---

## Step 2: Deploy on Streamlit Cloud

1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **"New app"**.
3.  **Select Repository**: Choose `YOUR_USERNAME/question-predictor`.
4.  **Branch**: `main`.
5.  **Main file path**: `main.py`.
6.  **Advanced Settings (Secrets)**:
    *   This is where you hide your API Key so it's not public.
    *   Click "Advanced settings..." -> "Secrets".
    *   Add your Gemini API Key like this (optional, or users can enter their own):
        ```toml
        GEMINI_API_KEY = "your-secret-api-key-here"
        ```
    *   *Note: Since your app has an input field for the API Key, you can skip this if you want users to provide their own key.*

7.  Click **"Deploy!"**.

---

## Step 3: Verify Deployment

Streamlit will start building your app. It might take 2-3 minutes.
*   It will automatically read `packages.txt` and install **Tesseract** and **Poppler**.
*   It will read `requirements.txt` and install Python libraries.

Once finished, you will get a public URL (e.g., `https://question-predictor.streamlit.app`) that you can share with college students! 🎓
