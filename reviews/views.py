from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .permissions import (
    IsAdmin,
    IsAuthenticated,
    IsAuthorOrReadOnlyOrAdminOrModerator,
    ReadOnly,
)
from .serializers import (
    CategoriesSerializer,
    CommentSerializer,
    GenresSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)

User = get_user_model()


class ListPostDelViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass


class TitlesViewSet(ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [ReadOnly | IsAuthenticated & IsAdmin]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleReadSerializer
        return TitleWriteSerializer


class GenresViewSet(ListPostDelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'name',
    ]
    permission_classes = [ReadOnly | IsAuthenticated & IsAdmin]
    lookup_field = 'slug'


class CategoriesViewSet(ListPostDelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'name',
    ]
    permission_classes = [ReadOnly | IsAuthenticated & IsAdmin]
    lookup_field = 'slug'


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnlyOrAdminOrModerator,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnlyOrAdminOrModerator,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
