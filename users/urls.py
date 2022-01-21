from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router_v1 = DefaultRouter()
router_v1.register('users', views.UserViewSet, basename='User')

urlpatterns = [
    path('v1/', include([path('', include(router_v1.urls))])),
    path(
        'auth/token/',
        views.APIGetToken.as_view(),
        name='get-token'
    ),
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='get-refresh-token'
    ),
    path(
        'email/',
        views.APIGetConfirmationCodeByEmail.as_view(),
        name='get-confirmation-code'
    )
]
