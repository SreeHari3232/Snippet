from rest_framework.routers import DefaultRouter
from .views import Snippets, Tags


router = DefaultRouter()
router.register('snippets', Snippets, basename='snippets')
router.register('tags', Tags, basename='tags')

urlpatterns = router.urls



