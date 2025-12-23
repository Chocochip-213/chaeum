from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    객체의 작성자(owner)만 쓰기(수정, 삭제) 권한을 가집니다.
    나머지 사용자는 읽기(GET, HEAD, OPTIONS) 권한만 가집니다.
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 권한(GET, HEAD, OPTIONS)은 모든 요청에 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 권한은 게시글 작성자(obj.user)와 요청자(request.user)가 같을 때만 허용
        return obj.user == request.user