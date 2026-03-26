<<<<<<< HEAD
# Document_translation
Based on the Streamli website's support for.docx, .ppt and.pdf document translations (currently in Chinese and English)
=======
#  DocTrans: Python Document Translator

DocTrans is a modern, lightweight, and easy-to-use document translation software built with Python. It allows users to translate documents (`.docx`, `.pdf`, `.pptx`) between English and Simplified Chinese while striving to maintain the original layout.

##  Features
- **Multi-Format Support**: Handle Word documents, PDFs, and PowerPoint presentations.
- **Bi-Directional Translation**: Supports English (EN) to Simplified Chinese (ZH) and vice versa.
- **Modern UI**: Powered by [Streamlit](https://streamlit.io/) for a clean, user-friendly experience.
- **Free Translation**: Uses the `deep-translator` library (Google Translate engine).
- **GitHub Ready**: Professional project structure and clean codebase.

##  Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/doctrans.git
cd doctrans
```

### 2. Set up a virtual environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

##  Usage

To start the application, run:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` to use the tool.

##  Project Structure
- `app.py`: The main Streamlit interface.
- `core/`: Core document processing handlers.
- `requirements.txt`: List of dependencies.
  
##  Contributing
Contributions are welcome! Please open an issue or submit a pull request.

---
>>>>>>> 335c39e (Initial commit: Professional document translation software with batch processing)
