import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)

class PDFParser:
    """
    PDF 파일을 파싱하여 텍스트 내용을 추출합니다.
    """

    def parse(self, file_path: str) -> str:
        """
        PDF 파일에서 텍스트를 추출합니다.
        Args:
            file_path (str): PDF 파일 경로.
        Returns:
            str: 추출된 텍스트 내용.
        """
        try:
            doc = fitz.open(file_path)
            text = []
            for page_num, page in enumerate(doc):
                page_text = page.get_text()
                if page_text:
                    text.append(page_text)
                else:
                    logger.warning(f"{file_path}의 {page_num + 1} 페이지가 비어있거나 읽을 수 없습니다.")

            full_text = "\n".join(text)
            logger.info(f"PDF 파싱 성공: {file_path} ({len(full_text)} 자)")
            return full_text

        except Exception as e:
            logger.error(f"PDF 파싱 실패 {file_path}: {e}")
            raise

    def parse_stream(self, file_bytes: bytes) -> str:
        """
        PDF 파일 바이너리 데이터에서 텍스트를 추출합니다.
        """
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text = []
            for page_num, page in enumerate(doc):
                page_text = page.get_text()
                if page_text:
                    text.append(page_text)

            full_text = "\n".join(text)
            logger.info(f"PDF 메모리 파싱 성공 ({len(full_text)} 자)")
            return full_text

        except Exception as e:
            logger.error(f"PDF 메모리 파싱 실패: {e}")
            raise