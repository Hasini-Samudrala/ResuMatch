# ✨ ResuMatch — Resume vs Job Description Matcher

> **AI-powered resume analysis tool** that scores your resume against any job description, identifies skill gaps, and gives actionable improvement suggestions — all from the terminal.

---

## 📖 What It Does

ResuMatch is a Python command-line application that uses the **Google Gemini API** to analyze how well your resume matches a specific job description. You paste your resume and a job description into the terminal, and the app returns:

- A **match score** (0–100) with an explanation
- **Technical and soft skills** required by the job
- Which skills you **already have** and which are **missing**
- **3 specific, actionable suggestions** to improve your resume for that role
- A **quick tip** on the most important missing skill to learn first
- All results are saved as a **formatted report** and tracked in a **CSV history log**

This is perfect for tailoring your resume before applying to specific positions.

---

## ✅ Features

- 🎯 **Match Scoring** — Get a 0–100 score showing how well you fit the role
- 🔧 **Skill Gap Analysis** — See which required skills are in your resume and which aren't
- 🚀 **Actionable Suggestions** — 3 specific improvements (not generic advice)
- 💡 **Quick Tips** — Learn which missing skill to prioritize first
- 📄 **Report Generation** — Every analysis is saved as a formatted .txt file
- 📊 **History Tracking** — CSV log lets you track your score improvements over time
- 🔒 **Secure** — API key stored in .env, never hardcoded
- ♻️ **Reusable** — Run multiple analyses in a single session

---

## 🛠 Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.8+ | Core programming language |
| Google Gemini API | AI-powered resume analysis (`gemini-1.5-flash` model) |
| `google-generativeai` | Official Python SDK for Gemini |
| `python-dotenv` | Load API key from `.env` file securely |

---

## 📁 Project Structure

```
resumatch/
├── .env                  # Your Gemini API key (git-ignored, never committed)
├── .env.example          # Template showing what .env should look like
├── .gitignore            # Files and folders excluded from Git
├── requirements.txt      # Python dependencies with pinned versions
├── main.py               # Entry point — run this to start the app
├── gemini_analyzer.py    # Handles all Gemini API communication
├── text_processor.py     # Text cleaning and terminal input handling
├── report_generator.py   # Report formatting, saving, and history tracking
├── history/              # Stores the CSV history log
│   └── .gitkeep
├── reports/              # Stores generated analysis reports (.txt files)
│   └── .gitkeep
└── README.md             # This file
```

### File Responsibilities

| File | What It Does |
|---|---|
| `main.py` | Orchestrates the entire workflow: welcome screen → input → analysis → display → save |
| `gemini_analyzer.py` | Sends structured prompts to Gemini and parses JSON responses |
| `text_processor.py` | Cleans raw text, collects multiline input, counts words, truncates long texts |
| `report_generator.py` | Formats results for terminal display, saves .txt reports, maintains CSV history |

---

## 🚀 Setup Instructions

### Part A — Get Your Gemini API Key (Free!)

1. Go to **[Google AI Studio](https://aistudio.google.com/app/apikey)**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key — you'll need it in Part C

> 💡 **The Gemini API is completely free** — no credit card required!

### Part B — Set Up Python Environment

**macOS / Linux:**
```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Windows:**
```cmd
# Create a virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Part C — Configure the Project

```bash
# Copy the example environment file
cp .env.example .env

# Open .env in any text editor and replace the placeholder:
# GEMINI_API_KEY=paste_your_gemini_api_key_here
# Change it to:
# GEMINI_API_KEY=AIzaSyD... (your actual key)
```

### Part D — Run the Project

```bash
python main.py
```

---

## 💻 How to Run

```bash
# Make sure your virtual environment is activated first!
python main.py
```

The app will:
1. Show a welcome banner
2. Ask you to paste your resume (type `DONE` when finished)
3. Ask you to paste a job description (type `DONE` when finished)
4. Analyze the match using Gemini AI (takes ~10-15 seconds)
5. Display results in the terminal
6. Save a report to `reports/` and log to `history/`
7. Ask if you want to analyze another resume

---

## 📸 Sample Output

![Sample Output](sample_output.png)

---

## 🧠 What I Learned

- **API Integration** — How to configure and use the Google Gemini API in Python, including API key management with environment variables and error handling for network calls
- **Prompt Engineering** — How to design structured prompts that reliably produce valid JSON output, including explicit format constraints and field-level instructions
- **JSON Parsing & Validation** — How to handle real-world API responses that may contain unexpected formatting, including stripping markdown code fences and validating data types
- **Modular Code Architecture** — How to separate concerns across multiple files (input handling, API communication, report generation) for cleaner, more maintainable code
- **File I/O & Data Persistence** — How to generate timestamped report files, maintain a running CSV history log, and handle file system operations safely with error handling

---

## ⚠️ Limitations

1. **Text-only input** — The app only accepts pasted text, not PDF or DOCX files. You need to copy-paste your resume content from another document.
2. **AI accuracy** — While Gemini provides useful analysis, the match score is an AI estimate, not a guaranteed predictor of interview success. Different runs may produce slightly different scores.
3. **Token limits** — Very long resumes or job descriptions are truncated to 800 words to stay within the free API tier's limits.

---

## 🔮 Future Improvements

1. **PDF Support** — Add the ability to directly upload PDF resumes using the `PyPDF2` library, so users don't have to manually copy-paste text
2. **Side-by-Side Comparison** — Add a feature to compare two versions of a resume against the same job description, showing which version scores higher and what changed

---


## 🔧 Troubleshooting

### ❌ "Invalid API key" error
Your `.env` file has the wrong key. Go to [Google AI Studio](https://aistudio.google.com/app/apikey), create a new key, and paste it into `.env`.

### ❌ "ModuleNotFoundError: No module named 'google.generativeai'"
You haven't installed the dependencies. Run: `pip install -r requirements.txt`
Also make sure your virtual environment is activated.

### ❌ "Failed to parse Gemini's response as JSON"
Gemini sometimes gives inconsistent responses. Just run the analysis again — it usually works on the second try.

---

*Built with ❤️ using Google Gemini AI*
