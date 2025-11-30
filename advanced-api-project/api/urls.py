from django.urls import path, include
from .views import BookViewSet, AuthorViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"books", BookViewSet, basename="book")
router.register(r"authors", AuthorViewSet, basename="author")

urlpatterns = [
    path("", include(router.urls)),
]
