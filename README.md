<div align="center">

# 🎭 MemeForge

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Gradio](https://img.shields.io/badge/UI-Gradio-0085FF)](https://gradio.app)
[![AI](https://img.shields.io/badge/AI-Gemini%20%2B%20Stable%20Diffusion-red)](https://huggingface.co/stabilityai)

**AI-powered Meme Generator using Gemini & Stable Diffusion**

</div>

---

## 🖼️ Preview
![MemeForge UI](https://github.com/Prasaderp/Real-Time-Emotion-Analytics-System-using-OpenCV/blob/master/Preview.png)

---

## 🚀 Features
- **AI-Generated Memes**
  - 📸 Image creation using **Stable Diffusion**
  - 🤖 Text generation via **Gemini AI**
- **Customizable Styles**
  - 🎨 Choose meme styles (Modern, Classic, Dark Humor, Wholesome)
  - 🔠 Select font type (Impact, Arial, Comic Sans, Roboto)
- **One-Click Sharing & Download**
  - 📥 Save memes locally
  - 📤 Share to social media (Coming soon!)

---

## 🛠️ Setup Guide

### 1️⃣ Install Dependencies
```
git clone https://github.com/YourUsername/MemeForge.git
cd MemeForge
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 2️⃣ Set Up API Keys
Create a `.env` file and add:
```
GEMINI_API_KEY=your_gemini_api_key
HF_API_KEY=your_huggingface_api_key
```

### 3️⃣ Run the App
```
python app.py
```

---

## 📌 Workflow
### Meme Generation Pipeline
```
graph LR
    A[User Input] -->|Prompt| B[Stable Diffusion - Generate Image]
    A -->|Topic| C[Gemini AI - Generate Text]
    B --> D[Overlay Text on Image]
    C --> D
    D --> E[Display & Share Meme]
```

---

## ❗ Notes
- Ensure API keys are valid for seamless functionality.
- Generated content is AI-driven and may require review.

---

<div align="center">
💡 Have ideas? [Open an Issue](https://github.com/YourUsername/MemeForge/issues)  
📩 Contact: your.email@example.com  
</div>
