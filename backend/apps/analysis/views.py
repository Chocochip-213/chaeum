from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.resumes.models import Resume
from apps.jobs.models import JobPosting
from .tasks import analyze_application_task


class AnalysisCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        resume_id = request.data.get('resume_id')
        job_posting_id = request.data.get('job_posting_id')

        if not resume_id or not job_posting_id:
            return Response(
                {"error": "resume_id and job_posting_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Task 실행
        task = analyze_application_task.delay(
            resume_id=resume_id,
            job_posting_id=job_posting_id,
            user_id=request.user.id
        )

        return Response(
            {"message": "Analysis started", "task_id": task.id},
            status=status.HTTP_202_ACCEPTED
        )