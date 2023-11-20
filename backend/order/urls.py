from django.urls import path
from rest_framework.routers import SimpleRouter
from order.views.datav import DataVViewSet
from order.views.info import OrderInfoViewSet
from order.views.item import OrderItemViewSet
from order.views.goods import OrderGoodsViewSet
from order.views.api.pay import OrderPaymentAPI

router = SimpleRouter()
router.register("api/order/info", OrderInfoViewSet)
router.register("api/order/item", OrderItemViewSet)
router.register("api/order/goods", OrderGoodsViewSet)
router.register("api/order/datav", DataVViewSet)

urlpatterns = [
    path("spider/pay", OrderPaymentAPI.as_view()),
]
urlpatterns += router.urls