from django.contrib import admin
from django.urls import path, include
from blog import views as blog_views
from users.views import (
    register,
    my_profile,
    update_profile,
    public_profile,
    google_login,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from blog.views import add_comment, toggle_like, list_comments, list_blogs

urlpatterns = [
    path("admin/", admin.site.urls),

    # Blog
    path("api/blogs/", list_blogs, name="list-blogs"),
    path("api/blogs/create/", blog_views.create_blog, name="create-blog"),
    path("api/blogs/<int:pk>/summarize/", blog_views.summarize_blog, name="summarize-blog"),

    # Comments & Likes
    path("api/blogs/<int:blog_id>/comment/", add_comment, name="add-comment"),
    path("api/blogs/<int:blog_id>/like/", toggle_like, name="toggle-like"),
    path("api/blogs/<int:blog_id>/comments/", list_comments, name="list-comments"),

    # Auth
    path("api/auth/register/", register, name="register"),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Profile
    path("api/profile/me/", my_profile, name="my-profile"),
    path("api/profile/update/", update_profile, name="update-profile"),
    path("api/profile/<str:username>/", public_profile, name="public-profile"),

    # dj-rest-auth
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),

    # Google login (your function-based view)
    path("auth/google/", google_login, name="google-login"),
]
