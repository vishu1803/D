from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer, CommentSerializer, BlogSerializer
from .utils import summarize_text
from .models import BlogPost, Comment, Like
from rest_framework.pagination import PageNumberPagination

@api_view(["GET"])
@permission_classes([AllowAny])
def list_blogs(request):
    blogs = BlogPost.objects.all().order_by("-created_at")
    return Response(BlogSerializer(blogs, many=True).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_blog(request):
    serializer = BlogSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    blog = serializer.save(author=request.user)
    return Response(BlogSerializer(blog).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def summarize_blog(request, pk):
    blog = BlogPost.objects.get(id=pk, author=request.user)
    blog.summary = summarize_text(blog.content)
    blog.save()
    return Response({"summary": blog.summary})

# Add comment
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_comment(request, blog_id):
    try:
        blog = BlogPost.objects.get(id=blog_id)
    except BlogPost.DoesNotExist:
        return Response({"error": "Blog not found"}, status=404)

    comment = Comment.objects.create(
        blog=blog, author=request.user, content=request.data.get("content", "")
    )
    return Response(CommentSerializer(comment).data, status=201)


# Toggle like (like/unlike)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_like(request, blog_id):
    try:
        blog = BlogPost.objects.get(id=blog_id)
    except BlogPost.DoesNotExist:
        return Response({"error": "Blog not found"}, status=404)

    like, created = Like.objects.get_or_create(blog=blog, user=request.user)
    if not created:  # already liked → unlike
        like.delete()
        return Response({"message": "Unliked"}, status=200)

    return Response({"message": "Liked"}, status=201)

class CommentPagination(PageNumberPagination):
    page_size = 5  # default number of comments per page
    page_size_query_param = "page_size"
    max_page_size = 20

@api_view(["GET"])
def list_comments(request, blog_id):
    try:
        blog = BlogPost.objects.get(id=blog_id)
    except BlogPost.DoesNotExist:
        return Response({"error": "Blog not found"}, status=404)

    comments = blog.comments.all().order_by("-created_at")  # latest first
    paginator = CommentPagination()
    result_page = paginator.paginate_queryset(comments, request)
    serializer = CommentSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

class BlogPagination(PageNumberPagination):
    page_size = 5  # default blogs per page
    page_size_query_param = "page_size"
    max_page_size = 20

@api_view(["GET"])
def list_blogs(request):
    blogs = BlogPost.objects.all().order_by("-created_at")  # latest first
    paginator = BlogPagination()
    result_page = paginator.paginate_queryset(blogs, request)
    serializer = BlogPostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
