# 🎬 YouTube Summarizer AI → Article & PDF

> Convert any YouTube video into a structured AI-generated article and downloadable PDF in seconds.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-LLaMA--3-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🚀 Live Demo

👉 *(Add your deployed Streamlit link here)*

---

## 📌 Key Features

* 🎥 Extracts transcript from any YouTube video
* 🤖 Generates high-quality AI articles using LLaMA-3 (Groq)
* 📝 Supports multiple article styles (Blog, Notes, Explanation, Summary)
* 📏 Adjustable article length (Short / Medium / Long)
* 📄 One-click PDF export with professional formatting
* ⚡ Fast and lightweight Streamlit interface
* 🔐 Secure API key handling via environment variables or UI

---

## 🧠 How It Works

### 1️⃣ Transcript Extraction

* Uses `youtube-transcript-api`
* Works without YouTube API key
* Supports multiple URL formats

### 2️⃣ AI Article Generation

* Model: `llama3-70b-8192`
* Powered by Groq API
* Converts raw transcript → structured article

### 3️⃣ PDF Generation

* Converts Markdown → formatted PDF
* Includes headings, spacing, and layout styling

---

## 🗂 Project Structure

```
yt_to_article/
│
├── app.py
├── utils/
│   ├── transcript.py
│   ├── article_generator.py
│   └── pdf_generator.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/youtube-summarizer-ai.git
cd yt_to_article
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set API Key (Choose One)

#### Option 1 — UI Input (Recommended for beginners)

* Enter API key inside app

#### Option 2 — Environment Variable

```bash
export GROQ_API_KEY=gsk_your_key_here
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 📦 Tech Stack

* **Frontend**: Streamlit
* **Backend**: Python
* **AI Model**: Groq (LLaMA-3 70B)
* **Transcript Extraction**: youtube-transcript-api
* **Video Metadata**: yt-dlp
* **PDF Generation**: FPDF2

---

## 💡 Supported YouTube URLs

* Standard videos
* Shorts
* Embedded links
* youtu.be links

---

## ⚠️ Limitations

* Videos without captions are not supported
* Very long transcripts are truncated (~12k chars)
* Auto-generated captions may contain minor errors

---

## 📈 Future Improvements

* 🌍 Multi-language support
* 🎧 Audio summarization
* 📊 Keyword extraction & highlights
* ☁️ Deployment on cloud (Streamlit / AWS)

---

## 📄 License

MIT License — free to use and modify.

---

## 🙌 Acknowledgment

Built as part of an AI/ML internship project — focused on transforming video content into structured knowledge.
