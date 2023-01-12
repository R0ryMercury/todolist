from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from goals.models import Goal, GoalCategory, GoalComment
from goals.serializers import (
    CommentCreateSerializer,
    CommentSerializer,
    GoalCategoryCreateSerializer,
    GoalCategorySerializer,
    GoalCreateSerializer,
    GoalSerializer,
)
from goals.permissions import CommentPermissions, GoalCategoryPermissions, GoalPermissions
from goals.filters import GoalDateFilter


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "date_created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated, GoalCategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated, GoalPermissions]

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save()
        return instance

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated, GoalPermissions]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = GoalDateFilter
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority"]
    ordering = ["priority", "due_date"]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class CommentCreateView(CreateAPIView):
    model = GoalComment
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, CommentPermissions]

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user)


class CommentListView(ListAPIView):
    model = GoalComment
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["goal"]
    ordering = "-id"

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user)
