from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.ResumeViewSet, basename='resume') # /api/resumes/

urlpatterns = [
    path('', include(router.urls)),
]