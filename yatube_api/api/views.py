from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostsSerializer)
from posts.models import Group, Post


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment model.

    Allows GET, POST, PUT, DELETE, PATCH methods.
    """

    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Return filtered queryset."""
        return self.get_post_id_or_404().comments.all()

    def perform_create(self, serializer):
        """Add correct author id to database."""
        serializer.save(author=self.request.user,
                        post=self.get_post_id_or_404())

    def get_post_id_or_404(self):
        """Return post object filtered by post_id."""
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Group model.

    Allows GET method only.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for Follow model.

    Allows GET and POST methods only.
    """

    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        """Return filtered queryset."""
        return self.request.user.follows.all()

    def perform_create(self, serializer):
        """Add correct user id to database."""
        serializer.save(user=self.request.user)


class PostsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model.

    Allows GET, POST, PUT, DELETE, PATCH methods.
    """

    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Add correct author id to database."""
        serializer.save(author=self.request.user)
