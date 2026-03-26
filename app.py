import streamlit as st
import os

# Only set CN region automatically if we suspect we are in a China network environment
if os.environ.get("translators_default_region") is None:
    if os.path.exists('/Users/'): # Local Mac
        os.environ["translators_default_region"] = "CN"

import tempfile
from core.translator import DocTranslator
from core.docx_handler import DocxHandler
from core.pptx_handler import PptxHandler
from core.pdf_handler import PdfHandler

# Page Configuration
st.set_page_config(page_title="DocTrans - Python Document Translator", page_icon="🌐", layout="wide")

# Custom CSS for modern UI
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stHeader {
        color: #1e3a8a;
    }
</style>
""", unsafe_allow_html=True)

# App Sidebar
with st.sidebar:
    st.title("DocTrans")
    st.info("Translate documents effortlessly between English and Simplified Chinese while maintaining layout.")
    
    st.subheader("Language Selection")
    source_lang = st.selectbox("From (Source)", options=["en", "zh-CN"], index=0)
    target_lang = st.selectbox("To (Target)", options=["zh-CN", "en"], index=0)
    
    st.divider()

# Main Content
st.header("Document Translation Software")
st.write("Upload a `.docx`, `.pdf`, or `.pptx` file and get its translated version.")

uploaded_file = st.file_uploader("Choose a file to translate", type=["docx", "pdf", "pptx"])

# Initialize Translator
translator = DocTranslator(source=source_lang, target=target_lang)

if uploaded_file is not None:
    # Save uploaded file to a temporary location
    file_extension = os.path.splitext(uploaded_file.name)[1]
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    
    # Process translation button
    if st.button("Start Translation", use_container_width=True):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text(f"Analyzing {uploaded_file.name} structure...")
            progress_bar.progress(10)
            
            output_path = f"translated_{uploaded_file.name}"
            
            # Start actual multi-step progress report
            with st.spinner("Processing document content..."):
                # Select handler based on extension
                if file_extension == ".docx":
                    status_text.text("Extracting and batching text blocks...")
                    progress_bar.progress(30)
                    translated_file_path = DocxHandler.translate_docx(tmp_file_path, translator, output_path)
                elif file_extension == ".pptx":
                    status_text.text("Scanning slides and text shapes...")
                    progress_bar.progress(30)
                    translated_file_path = PptxHandler.translate_pptx(tmp_file_path, translator, output_path)
                elif file_extension == ".pdf":
                    status_text.text("Extracting PDF text layers...")
                    progress_bar.progress(30)
                    translated_file_path = PdfHandler.translate_pdf(tmp_file_path, translator, output_path)
                else:
                    st.error("Unsupported file format!")
                    translated_file_path = None
                
            progress_bar.progress(100)
            status_text.text("Finalizing document...")
            
            # Save to session_state
            if translated_file_path and os.path.exists(translated_file_path):
                with open(translated_file_path, "rb") as f:
                    st.session_state['translated_data'] = f.read()
                st.session_state['translated_name'] = output_path
                # Cleanup output file
                os.remove(translated_file_path)

        except Exception as e:
            st.error(f"Error during translation: {e}")
            import traceback
            st.code(traceback.format_exc())
        
        finally:
            progress_bar.empty()
            status_text.empty()
            # Cleanup temporary source file
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    # Show download button if data is in session_state and it's for the same file
    if 'translated_data' in st.session_state and st.session_state.get('translated_name') == f"translated_{uploaded_file.name}":
        st.success("✅ Translation Complete!")
        st.download_button(
            label="⬇️ Download Translated Document",
            data=st.session_state['translated_data'],
            file_name=st.session_state['translated_name'],
            mime="application/octet-stream"
        )
else:
    # Clear state when no file is uploaded
    if 'translated_data' in st.session_state:
        del st.session_state['translated_data']
    if 'translated_name' in st.session_state:
        del st.session_state['translated_name']
    st.info("Please upload a file to begin.")

# Documentation
with st.expander("❓ Help & Documentation"):
    st.markdown("""
    ### Supported Formats
    - **Microsoft Word (.docx)**: Translates paragraphs and tables while preserving basic formatting.
    - **PowerPoint (.pptx)**: Translates text box content in slides.
    - **Adobe PDF (.pdf)**: Best for text extraction and translation.
    
    ### How it works
    DocTrans uses the `translators` library with **Batch Processing** technology. This allows the app to group hundreds of paragraphs together into single requests, making the translation significantly faster than traditional line-by-line tools.
    """)
