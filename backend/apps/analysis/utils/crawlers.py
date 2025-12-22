import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


class JobCrawler:
    """
    채용 공고 URL을 크롤링하여 내용을 추출합니다.
    알려진 플랫폼(예: 원티드)에 대한 별도 로직을 지원합니다.
    """

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch(self, url: str) -> str:
        """
        URL에서 콘텐츠를 가져옵니다. URL 패턴에 따라 적절한 핸들러로 분기합니다.
        """
        try:
            if "wanted.co.kr/wd/" in url:
                return self._fetch_wanted(url)
            else:
                return self._fetch_generic(url)
        except Exception as e:
            logger.error(f"URL 크롤링 실패 {url}: {e}")
            raise

    def _fetch_wanted(self, url: str) -> str:
        """
        원티드(Wanted.co.kr) 내부 API를 사용하는 특수 핸들러입니다.
        """
        try:
            job_id = url.split("/wd/")[-1].split("/")[0]
            api_url = f"https://www.wanted.co.kr/api/v4/jobs/{job_id}"

            response = requests.get(api_url, headers=self.headers)
            response.raise_for_status()

            data = response.json()
            job = data.get('job', {})
            detail = job.get('detail', {})

            # 구조화된 텍스트 표현 생성
            content = [
                f"포지션: {job.get('position')}",
                f"회사명: {job.get('company', {}).get('name')}",
                f"회사 소개: {detail.get('intro')}",
                f"주요 업무: {detail.get('main_tasks')}",
                f"자격 요건: {detail.get('requirements')}",
                f"우대 사항: {detail.get('preferred_points')}"
            ]

            return "\n\n".join(filter(None, content))

        except Exception as e:
            logger.warning(f"원티드 API 가져오기 실패, 일반 방식으로 전환: {e}")
            return self._fetch_generic(url)

    def _fetch_generic(self, url: str) -> str:
        """
        BeautifulSoup을 사용하는 일반 핸들러입니다.
        """
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # 스크립트 및 스타일 요소 제거
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        text = soup.get_text(separator='\n', strip=True)
        return text