from rest_framework import viewsets
from rest_framework.exceptions import NotAcceptable

from djshop.apps.catalog.serializers.admin import (
    CreateCategoryNodeSerializer,
    CategoryTreeSerializer,
    CategoryNodeSerializer,
    CategoryModificationSerializer
)
from djshop.apps.catalog.models import Category


class CategoryViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        if self.action == "list":
            return Category.objects.filter(depth=1)
        else:
            return Category.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CategoryTreeSerializer
        elif self.action == 'create':
            return CreateCategoryNodeSerializer
        elif self.action == 'retrieve':
            return CategoryNodeSerializer
        elif self.action in ["update", "partial_update", "destroy"]:
            return CategoryModificationSerializer
        else:
            return NotAcceptable
