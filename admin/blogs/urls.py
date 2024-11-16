from django.urls import path
from blogs.views import BlogViewSet, UserViewSet

urlpatterns = [
    path('blogs/', BlogViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('blogs/<str:pk>/', BlogViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('users/', UserViewSet.as_view({
        'get': 'get',
    })),
]