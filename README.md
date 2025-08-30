# 📚 Personal English Corpus

A lightweight **English learning corpus management tool** built with **Python + JSON + Streamlit**.  
Inspired by the thematic unit design of *English Vocabulary in Use*, this project helps you organize words and phrases by **topics**, while tracking phonetics, meanings, examples, familiarity levels, and notes.

---

## ✨ Features

- 📝 **Word & Phrase Management**
  - Organize vocabulary entries by topic
  - Support phonetics, Chinese meaning, example sentences, familiarity level, and notes

- 📂 **Lightweight Data Storage**
  - All vocabulary is stored in `corpus.db` (SQLite) or `data/vocab.json`
  - Automatic backups before every update

- 📊 **Interactive Web Interface**
  - Browse, search, and filter via a Streamlit-powered interface
  - Filter entries by topic or familiarity

- 📤 **Import & Export**
  - Import from CSV (with mandatory columns: `word, topic`)
  - Export to Excel (`.xlsx`) for backup or printing

---

## 📦 Installation

### 1. Clone or Download the Project

Assume the project is placed under `G:\corpus`:

```powershell
cd G:\corpus
```

Project structure:

```
corpus/
│── app/
│   ├── __init__.py
│   ├── streamlit_app.py
│   ├── config.py
│   ├── storage.py
│   └── models.py
│── data/
│   └── vocab.json
│── backups/
│── exports/
│── run_app.bat
│── README.md
│── requirements.txt
```

---

### 2. Create Conda Environment

```powershell
conda create -n corpus python=3.10
conda activate corpus
```

---

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

(If `requirements.txt` is missing, install manually:)

```powershell
pip install streamlit pandas sqlalchemy openpyxl
```

---

## 🚀 Usage

### Method 1: Run via Command Line

```powershell
$env:PYTHONPATH="G:\corpus"
streamlit run app/streamlit_app.py
```

### Method 2: Run via Batch Script (Recommended ✅)

Double-click `run_app.bat`. It will automatically:

1. Activate the Conda environment  
2. Set `PYTHONPATH`  
3. Start Streamlit server  

Access in your browser:

```
http://localhost:8501
```

---

## 🌐 Web App Workflow

### 1. Launch

A local browser page will open automatically. If not, copy the terminal link into your browser.

### 2. Main Functions

**🔍 Browse & Review**  
- Filter by topic and familiarity  
- Keyword search (matches words, meanings, examples, or phrases)  
- Quick actions:  
  - Increase/Decrease familiarity  
  - Directly set familiarity level  
  - Delete entry  

**➕ Add / Edit Entries**  
- Input word/phrase, topic, meaning, etc.  
- Multiple phrases supported (semicolon or line break separated)  
- Duplicate entries under the same topic will be merged automatically (definitions/phrases merged, familiarity kept as the higher value)  

**📥 Import / 📤 Export**  
- **Import**: Upload a CSV file  
  - Required: `word, topic`  
  - Optional: `phonetic, meaning, example, phrases, familiarity, notes`  
  - Use semicolons (`;`) to separate multiple phrases  
- **Export**: One-click export to `exports/vocab_export.xlsx`  

### 3. Data & Backup

- **Main Data**: `G:\corpus\data\vocab.json` (UTF-8 JSON)  
- **Backups**: Auto-saved to `G:\corpus\backups\` with timestamps  
- **Exports**: Saved under `G:\corpus\exports\`  

### 4. Tips & Extensions

- Keep **topic names** consistent (e.g., `Food`, `Travel`, `Health`) for easier retrieval  
- Suggested **familiarity levels**: 1 = unfamiliar, 3 = somewhat familiar, 5 = very familiar  
- For **bulk import**, save your Excel sheet as CSV and ensure headers follow:  
  `word, phonetic, meaning, topic, example, phrases, familiarity, notes` (at least `word, topic`)  

---

## 🛠️ Future Improvements

- [ ] Familiarity learning curve (like Anki review stats)  
- [ ] Audio pronunciation support  
- [ ] Markdown notes field  
- [ ] Mobile-friendly UI  

---

## 📝 Author

- **Wu Guojia**  
  Tianjin Medical University  
  📧 wuguojia@tmu.edu.cn  

## 🌍 Live Demo

- **https://wuguojia-corpus.streamlit.app/**

---
