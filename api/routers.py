from rest_framework.routers import DefaultRouter
from .views import Snippets, Tags
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path

router = DefaultRouter()
router.register('snippets', Snippets, basename='snippets')
router.register('tags', Tags, basename='tags')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = router.urls



