from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register('titles', views.TitlesViewSet, basename='Titles')
router_v1.register('genres', views.GenresViewSet, basename='Genres')
router_v1.register(
    'categories', views.CategoriesViewSet, basename='Categories'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet, basename='Review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='Comment',
)

urlpatterns = [path('v1/', include(router_v1.urls))]
