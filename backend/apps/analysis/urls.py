from django.urls import path
from .views import AnalysisView, AnalysisHistoryView

app_name = 'analysis'

urlpatterns = [
    path('', AnalysisView.as_view(), name='analysis'), # /api/analysis/
    path('history/', AnalysisHistoryView.as_view(), name='analysis_history'),
]