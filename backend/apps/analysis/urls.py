from django.urls import path
from .views import AnalysisCreateView

app_name = 'analysis'

urlpatterns = [
    path('analyze/', AnalysisCreateView.as_view(), name='analyze'),
]