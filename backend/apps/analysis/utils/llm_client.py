import json
import logging
from gradio_client import Client
from typing import Dict, Any

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Gradio 호스팅 LLM과 상호작용하기 위한 클라이언트입니다.
    """

    def __init__(self, gradio_url: str):
        self.client = Client(gradio_url)
        logger.info(f"Gradio 서버 연결됨: {gradio_url}")

    def analyze_gap(self, resume_text: str, job_text: str) -> Dict[str, Any]:
        """
        이력서와 직무 기술서를 LLM에 전송하여 갭 분석(Gap Analysis)을 수행합니다.
        """
        system_prompt = (
            "당신은 전문 테크니컬 리크루터이자 커리어 코치입니다.\n"
            "지원자의 이력서를 분석하여 보유 기술(Extracted Skills)을 파악하고, "
            "직무 기술서(JD)와의 격차(Gap)를 분석하는 것이 당신의 임무입니다.\n"
            "부족한 기술(Missing Skills)을 식별하고, 왜 그것이 부족한지 상세한 이유를 한국어로 설명하십시오."
            "모든 분석 결과(main_tasks, missing_skills_chapter 등)는 반드시 **한국어**로 작성되어야 합니다. "
            "(단, 기술 스택 명칭은 영문 유지)\n"
            "missing_skills_chapters를 포함하여 JSON을 생성하라"
        )

        user_prompt = f"""
        ### Resume:
        {resume_text[:10000]}
        ### Job Description:
        {job_text[:5000]}
        Please analyze the resume skills and perform a Gap Analysis to use Korean.
        
        """

        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        try:
            result = self.client.predict(
                full_prompt,
                api_name="/predict"
            )
            return self._parse_json_response(str(result))
        except Exception as e:
            logger.error(f"LLM 예측 실패: {e}")
            raise

    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """
        LLM 응답에서 JSON을 견고하게 추출합니다.
        """
        text = text.strip()

        # 시도 1: 직접 파싱
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # 시도 2: 마크다운 코드 블록
        try:
            if "```json" in text:
                content = text.split("```json")[1].split("```")[0].strip()
                return json.loads(content)
            elif "```" in text:
                content = text.split("```")[1].split("```")[0].strip()
                return json.loads(content)
        except Exception:
            pass

        # 시도 3: 중괄호 { } 찾기
        try:
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1:
                return json.loads(text[start:end + 1])
        except Exception:
            pass

        logger.error(f"응답에서 JSON 파싱 실패: {text[:200]}...")
        return {"error": "JSON 파싱 실패", "raw_response": text}