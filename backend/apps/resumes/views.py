from rest_framework import viewsets, permissions, parsers, status
from rest_framework.response import Response
from .models import Resume
from .serializers import ResumeSerializer
from apps.analysis.utils.parsers import PDFParser # 이력서 파싱 스크립트임.


class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        uploaded_file = self.request.FILES.get('file')
        if not uploaded_file:
            return

        parser = PDFParser()
        parsed_text = ""

        try:
            file_bytes = uploaded_file.read()
            parsed_text = parser.parse_stream(file_bytes)
        except Exception as e:
            print(f"Parsing Error: {e}")

        serializer.save(
            user=self.request.user,
            file_name=uploaded_file.name,
            parsed_content=parsed_text,
            status='SUCCESS'
        )