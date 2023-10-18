"""This file contains serializers for YaTube API project."""
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User


class PostsSerializer(serializers.ModelSerializer):
    """Post model serializer."""

    author = SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True)

    class Meta:
        """Meta class for PostsSerializer."""

        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Comment model serializer."""

    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username')

    class Meta:
        """Meta class for CommentSerializer."""

        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    """Group model serializer."""

    class Meta:
        """Meta class for GroupSerializer."""

        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    """Follow model serializer."""

    user = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username')
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username')

    class Meta:
        """Meta class for FollowSerializer."""

        model = Follow
        exclude = ('id',)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate_following(self, value):
        """Following field validator for FollowSerializer."""
        if self.context['request'].user == value:
            raise serializers.ValidationError('Нельзя подписаться на себя.')
        return value
