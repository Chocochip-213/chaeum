from django.urls import path
from .views import (
    RegisterView,
    PasswordChangeView,
    LogoutView, UserDeleteView,
    PasswordResetRequestView,
    PasswordResetConfirmView
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/', UserDeleteView.as_view(), name='user_delete'),
    path('password/reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]