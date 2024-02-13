from rest_framework.routers import DefaultRouter


from api.views import VideoViewSet
router = DefaultRouter()
router.register(r'file', VideoViewSet, basename='file')

api_urls = router.urls
