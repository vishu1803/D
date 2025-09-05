from django.contrib import admin
from django.urls import path
from blog import views as blog_views
from users.views import register
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import register, my_profile, update_profile, public_profile
from blog.views import add_comment, toggle_like
from blog.views import list_comments
from blog.views import list_blogs
from django.urls import path, include
from .views import GoogleLoginView


urlpatterns = [
    path("admin/", admin.site.urls),

    # Blog
    path("api/blogs/", blog_views.list_blogs),
    path("api/blogs/create/", blog_views.create_blog),
    path("api/blogs/<int:pk>/summarize/", blog_views.summarize_blog),

    # Auth
    path("api/auth/register/", register),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

     # Profile endpoints
    path("api/profile/me/", my_profile),
    path("api/profile/update/", update_profile),
    path("api/profile/<str:username>/", public_profile),

    path("api/blogs/<int:blog_id>/comment/", add_comment),
    path("api/blogs/<int:blog_id>/like/", toggle_like),
    path("api/blogs/<int:blog_id>/comments/", list_comments),  # paginated
    path("api/blogs/", list_blogs),  # now paginated
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("auth/google/", include("allauth.socialaccount.providers.google.urls")),
    path("auth/google/", GoogleLoginView.as_view(), name="google-login"),


]
