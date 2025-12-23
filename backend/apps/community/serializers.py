from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = Comment
        fields = ['id', 'user_nickname', 'content', 'created_at']
        read_only_fields = ['user_nickname']

class PostSerializer(serializers.ModelSerializer):
    user_nickname = serializers.ReadOnlyField(source='user.nickname')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'user_id', 'id', 'user_nickname', 'title', 'content',
            'book_isbn', 'view_count', 'comments',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user_nickname', 'view_count', 'comments']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)