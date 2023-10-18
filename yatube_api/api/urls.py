"""This file contains endpoints for YaTube API project."""

from django.urls import include, path
from rest_framework import routers

import api.views as views

router_v1 = routers.DefaultRouter()
router_v1.register('posts', views.PostsViewSet, basename='posts')
router_v1.register('groups', views.GroupViewSet, basename='groups')
router_v1.register('follow', views.FollowViewSet, basename='follows')
router_v1.register(r'posts/(?P<post_id>\d+)/comments',
                   views.CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),
]
