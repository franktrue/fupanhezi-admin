from django.urls import path
from rest_framework.routers import SimpleRouter
from order.views.info import OrderInfoViewSet
from order.views.item import OrderItemViewSet
from order.views.goods import OrderGoodsViewSet

router = SimpleRouter()
router.register("api/order/info", OrderInfoViewSet)
router.register("api/order/item", OrderItemViewSet)
router.register("api/order/goods", OrderGoodsViewSet)

urlpatterns = []
urlpatterns += router.urls