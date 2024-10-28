from django.urls import path, include

from .views import PostViewSet, FeedAPIView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")


urlpatterns = [
    path("", include(router.urls)),
    path("feed/", FeedAPIView.as_view(), name="feed"),
]
