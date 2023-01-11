from django.urls import path, include
from core.views import UserViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("profile", UserViewSet, basename="profile")

urlpatterns = [
    path("", include(router.urls)),
]
