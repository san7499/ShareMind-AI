from pathlib import Path

import fitz  # PyMuPDF
from docx import Document

from app.utils.logger import logger


class DocumentParser:
    """
    Extract text from supported document types.
    """

    def parse(self, file_path: str) -> str:
        """
        Detect file type and parse accordingly.
        """

        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return self.parse_pdf(file_path)

        elif extension == ".docx":
            return self.parse_docx(file_path)

        elif extension == ".txt":
            return self.parse_txt(file_path)

        else:
            logger.warning(f"Unsupported file type: {extension}")
            return ""

    def parse_pdf(self, file_path: str) -> str:
        """
        Extract text from PDF.
        """

        logger.info(f"Reading PDF: {file_path}")

        text = ""

        try:
            pdf = fitz.open(file_path)

            for page in pdf:
                text += page.get_text()

            pdf.close()

        except Exception as e:
            logger.error(f"PDF parsing failed: {e}")

        return text

    def parse_docx(self, file_path: str) -> str:
        """
        Extract text from Word document.
        """

        logger.info(f"Reading DOCX: {file_path}")

        text = ""

        try:
            document = Document(file_path)

            for paragraph in document.paragraphs:
                text += paragraph.text + "\n"

        except Exception as e:
            logger.error(f"DOCX parsing failed: {e}")

        return text

    def parse_txt(self, file_path: str) -> str:
        """
        Extract text from TXT file.
        """

        logger.info(f"Reading TXT: {file_path}")

        try:
            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                return file.read()

        except Exception as e:
            logger.error(f"TXT parsing failed: {e}")
            return ""


# Singleton instance
document_parser = DocumentParser()