from random import random
from rest_framework import viewsets
from rest_framework.response import Response
from blogs.producer import publish
from blogs.models import Blog, User
from blogs.serializers import BlogSerializer
from django.shortcuts import get_object_or_404

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def list(self, request):
        queryset = Blog.objects.all()
        print(queryset)
        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish('blog_created', serializer.data)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def retrieve(self, request, pk=None):
        queryset = Blog.objects.all()
        blog = get_object_or_404(queryset, pk=pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        blog = Blog.objects.get(pk=pk)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish('blog_updated', serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    
    def destroy(self, request, pk=None):
        blog = Blog.objects.get(pk=pk)
        blog.delete()
        publish('blog_deleted', {'id': pk})
        return Response(status=204)
    


class UserViewSet(viewsets.ModelViewSet):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        random_u = random.choice(users)

        return Response({'id': random_u.id})