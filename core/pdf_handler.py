import fitz  # PyMuPDF

class PdfHandler:
    @staticmethod
    def translate_pdf(file_path, translator, output_path=None):
        doc = fitz.open(file_path)
        out_doc = fitz.open()

        # 1. Collect all translatable blocks
        all_blocks = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            blocks = page.get_text("blocks")
            for block in blocks:
                if block[4].strip():
                    # (x0, y0, x1, y1, text, block_no, block_type)
                    all_blocks.append({
                        "page_num": page_num,
                        "rect": (block[0], block[1]),
                        "text": block[4]
                    })
        
        # 2. Extract texts and batch translate
        texts_to_translate = [b["text"] for b in all_blocks]
        translated_texts = translator.translate_texts(texts_to_translate)
        
        # 3. Create out_doc and write translated text
        # Initialize pages
        for page in doc:
            out_doc.new_page(width=page.rect.width, height=page.rect.height)
            
        for block_data, translated_text in zip(all_blocks, translated_texts):
            new_page = out_doc[block_data["page_num"]]
            try:
                new_page.insert_text(block_data["rect"], translated_text, fontname="china-s", fontsize=10)
            except:
                new_page.insert_text(block_data["rect"], translated_text, fontsize=10)

        if output_path is None:
            output_path = file_path.replace(".pdf", "_translated.pdf")
            
        out_doc.save(output_path)
        return output_path
