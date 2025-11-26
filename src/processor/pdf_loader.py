import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os
import shutil

class PDFLoader:
    def __init__(self, tesseract_cmd=None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        else:
            # Try to auto-detect common paths if not in PATH
            common_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\Tesseract-OCR\tesseract.exe"),
                "/usr/bin/tesseract",
                "/usr/local/bin/tesseract"
            ]
            for path in common_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break

    def extract_text(self, file_path):
        """
        Extracts text from a file (PDF or Image).
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in ['.jpg', '.jpeg', '.png']:
            return self._extract_text_from_image(file_path)
        elif ext == '.pdf':
            return self._extract_text_from_pdf(file_path)
        else:
            return ""

    def _extract_text_from_image(self, file_path):
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Error reading image {file_path}: {e}")
            return ""

    def _extract_text_from_pdf(self, file_path):
        text = ""
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            # Fallback to OCR if text is sparse
            if len(text.strip()) < 50:
                print(f"Text extraction yielded low content for {file_path}. Attempting OCR...")
                text = self._extract_text_ocr(file_path)
                
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return None
            
        return text

    def _extract_text_ocr(self, file_path):
        """
        Fallback method using OCR for PDFs.
        """
        text = ""
        try:
            images = convert_from_path(file_path)
            for i, image in enumerate(images):
                page_text = pytesseract.image_to_string(image)
                text += page_text + "\n"
        except Exception as e:
            print(f"OCR failed for {file_path}: {e}")
            return ""
        
        return text
