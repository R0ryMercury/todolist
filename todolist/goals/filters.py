from django.db import models
from django_filters.rest_framework import FilterSet
from django_filters import IsoDateTimeFilter

from goals.models import Goal


class GoalDateFilter(FilterSet):
    class Meta:
        model = Goal
        fields = {
            "due_date": ("lte", "gte"),
            "category": ("exact", "in"),
            "status": ("exact", "in"),
            "priority": ("exact", "in"),
        }

    filter_overrides = {models.DateTimeField: {"filter_class": IsoDateTimeFilter}}
