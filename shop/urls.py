from rest_framework.routers import DefaultRouter
from shop.views import TradePointViewSet


router = DefaultRouter()
router.register('', TradePointViewSet, basename='trade_point')


urlpatterns = [
    *router.urls
]
