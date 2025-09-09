
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import BlogSerializer, BlogPostSerializer, CommentSerializer
from .models import BlogPost, Comment, Like
from .ai_utils import generate_summary


# 🔹 Pagination classes
class BlogPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 20


class CommentPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 20


# 🔹 List blogs (paginated)
@api_view(["GET"])
@permission_classes([AllowAny])
def list_blogs(request):
    blogs = BlogPost.objects.all().order_by("-created_at")
    paginator = BlogPagination()
    result_page = paginator.paginate_queryset(blogs, request)
    serializer = BlogPostSerializer(result_page, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data)


# 🔹 Create blog
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_blog(request):
    serializer = BlogSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    blog = serializer.save(author=request.user)
    return Response(BlogSerializer(blog, context={"request": request}).data)


# 🔹 Summarize blog
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def summarize_blog(request, pk):
    try:
        blog = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response({"error": "Blog not found"}, status=404)

    if blog.summary:
        return Response({
            "blog_id": blog.id,
            "title": blog.title,
            "summary": blog.summary,
            "cached": True
        })

    summary = generate_summary(blog.content)
    blog.summary = summary
    blog.save()

    return Response({
        "blog_id": blog.id,
        "title": blog.title,
        "summary": summary,
        "cached": False
    })


# 🔹 Add comment
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


# 🔹 List comments (paginated)
@api_view(["GET"])
def list_comments(request, blog_id):
    try:
        blog = BlogPost.objects.get(id=blog_id)
    except BlogPost.DoesNotExist:
        return Response({"error": "Blog not found"}, status=404)

    comments = blog.comments.all().order_by("-created_at")
    paginator = CommentPagination()
    result_page = paginator.paginate_queryset(comments, request)
    serializer = CommentSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# 🔹 Toggle like
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_like(request, blog_id):
    try:
        blog = BlogPost.objects.get(id=blog_id)
    except BlogPost.DoesNotExist:
        return Response({"error": "Blog not found"}, status=404)

    like, created = Like.objects.get_or_create(blog=blog, user=request.user)
    if not created:
        like.delete()
        return Response({"message": "Unliked"}, status=200)

    return Response({"message": "Liked"}, status=201)

@api_view(["GET"])
def blog_detail(request, pk):
    try:
        blog = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = BlogPostSerializer(blog, context={"request": request})
    return Response(serializer.data)