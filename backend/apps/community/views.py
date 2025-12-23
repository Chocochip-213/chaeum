from rest_framework import viewsets, permissions, status, filters
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, MyCommentSerializer
from .permissions import IsOwnerOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('user').prefetch_related('comments')
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['book_isbn']
    ordering_fields = ['created_at', 'view_count']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Post.objects.filter(pk=instance.pk).update(view_count=F('view_count') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def comments(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='my', permission_classes=[permissions.IsAuthenticated])
    def my_posts(self, request):
        """
        URL: GET /api/community/posts/my/
        """
        my_posts = Post.objects.filter(user=request.user).order_by('-created_at')
        serializer = self.get_serializer(my_posts, many=True)
        return Response(serializer.data)

class MyCommentListView(generics.ListAPIView):
    """
    내 댓글 목록 조회 (최신순, 페이지네이션 없음)
    URL: GET /api/community/comments/my/
    """
    serializer_class = MyCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user).order_by('-created_at')