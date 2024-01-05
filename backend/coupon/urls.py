from django.urls import path
from rest_framework.routers import SimpleRouter
from coupon.views.coupons import CouponsViewSet
from coupon.views.scenes import CouponScenesViewSet
from coupon.views.exchanges import CouponExchangesViewSet
from coupon.views.exchange_codes import CouponExchangeCodesViewSet

router = SimpleRouter()
router.register("api/coupon/coupons", CouponsViewSet)
router.register("api/coupon/scenes", CouponScenesViewSet)
router.register("api/coupon/exchanges", CouponExchangesViewSet)
router.register("api/coupon/exchange_codes", CouponExchangeCodesViewSet)

urlpatterns = [
]
urlpatterns += router.urls