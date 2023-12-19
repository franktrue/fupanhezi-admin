from django.urls import path
from rest_framework.routers import SimpleRouter
from user_center.views.user import UserViewSet
from user_center.views.user_datav import DataVViewSet
from user_center.views.user_auth import UserAuthViewSet
from user_center.views.user_withdraw_record import UserWithdrawRecordViewSet
from user_center.views.user_reward import UserRewardViewSet
from user_center.views.user_agent import UserAgentViewSet

router = SimpleRouter()
router.register("api/user_center/user", UserViewSet)
router.register("api/user_center/user_auth", UserAuthViewSet)
router.register("api/user_center/user_withdraw_record", UserWithdrawRecordViewSet)
router.register("api/user_center/user_reward", UserRewardViewSet)
router.register("api/user_center/user_agent", UserAgentViewSet)
router.register("api/user_center/datav", DataVViewSet)

urlpatterns = [
]
urlpatterns += router.urls