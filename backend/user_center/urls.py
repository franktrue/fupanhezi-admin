from django.urls import path
from rest_framework.routers import SimpleRouter
from user_center.views.user import UserViewSet
from user_center.views.user_auth import UserAuthViewSet
from user_center.views.user_withdraw_record import UserWithdrawRecordViewSet

router = SimpleRouter()
router.register("api/user_center/user", UserViewSet)
router.register("api/user_center/user_auth", UserAuthViewSet)
router.register("api/user_center/user_withdraw_record", UserWithdrawRecordViewSet)

urlpatterns = [
]
urlpatterns += router.urls