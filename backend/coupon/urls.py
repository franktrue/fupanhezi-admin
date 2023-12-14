from django.urls import path
from rest_framework.routers import SimpleRouter
from coupon.views.coupons import CouponsViewSet
from coupon.views.scenes import CouponScenesViewSet

router = SimpleRouter()
router.register("api/coupon/coupons", CouponsViewSet)
router.register("api/coupon/scenes", CouponScenesViewSet)

urlpatterns = [
]
urlpatterns += router.urls