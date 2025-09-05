from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, ProfileSerializer
from .models import Profile
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests


@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({"id": user.id, "username": user.username, "email": user.email})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_profile(request):
    profile = request.user.profile
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    profile = request.user.profile
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
def public_profile(request, username):
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=404)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)


# ✅ NEW: Google Login / Signup
@api_view(["POST"])
def google_login(request):
    token = request.data.get("access_token")
    if not token:
        return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Verify token with Google
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request())
        email = idinfo["email"]
        name = idinfo.get("name", email.split("@")[0])
        avatar_url = idinfo.get("picture", None)

        # Get or create user
        user, created = User.objects.get_or_create(
            username=email,
            defaults={"email": email, "first_name": name},
        )

        # Ensure profile exists & update avatar if from Google
        profile, _ = Profile.objects.get_or_create(user=user)
        if avatar_url and (created or not profile.avatar):
            profile.avatar = avatar_url
            profile.save()

        # Generate JWT
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "email": email,
                "username": user.username,
            },
            status=status.HTTP_200_OK,
        )

    except ValueError:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    profile = request.user.profile
    serializer = ProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)
