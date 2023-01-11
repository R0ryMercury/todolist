from django.contrib.auth import login
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from core.models import User
from core.serializers import CreateUserSerializer


class SignUpView(CreateAPIView):
    model = User
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)
        login(
            self.request,
            user=serializer.user,
            backend="django.contrib.auth.backends.ModelBackend",
        )
