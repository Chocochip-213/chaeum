from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
import uuid
from django.contrib.auth import login
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserSerializer, 
    PasswordChangeSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "회원가입 성공",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            
            token.blacklist()
            
            return Response({"message": "성공적으로 로그아웃되었습니다."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "잘못된 토큰이거나 이미 로그아웃된 상태입니다."}, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        
        return Response({"message": "회원 탈퇴가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            User = get_user_model()

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "해당 이메일로 가입된 회원을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = f"http://localhost:5173/reset-password/{uid}/{token}"
            
            subject = "[채움] 비밀번호 재설정 안내"
            message = f"안녕하세요, {getattr(user, 'nickname', '회원')}님.\n\n아래 링크를 클릭하여 비밀번호를 재설정해주세요.\n\n{reset_url}\n\n"
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                return Response({"message": "비밀번호 재설정 이메일을 발송했습니다."}, status=status.HTTP_200_OK)
            except Exception as e:
                print(f"Email sending error: {e}")
                return Response({"error": "이메일 전송 중 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "비밀번호가 성공적으로 재설정되었습니다."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def demo_login(request):
    # 1. 랜덤한 유니크 ID 생성
    random_suffix = str(uuid.uuid4())[:8]
    email = f'demo_{random_suffix}@example.com'
    nickname = f'Guest_{random_suffix}'
    password = 'demopassword'

    # 2. 유저 생성
    User = get_user_model()
    # 이메일 기반이므로 email 필드 사용, nickname은 필수 필드
    user, created = User.objects.get_or_create(
        email=email,
        defaults={'nickname': nickname}
    )
    
    if created:
        user.set_password(password)
        user.save()

    # 3. 로그인 처리 (세션 생성)
    # backend를 명시해주어야 login()이 정상 작동함 (authenticate를 거치지 않았으므로)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    
    # 4. JWT 토큰 생성
    refresh = RefreshToken.for_user(user)

    return JsonResponse({
        'message': 'Guest login success', 
        'email': email,
        'nickname': nickname,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })