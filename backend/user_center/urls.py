from django.urls import path
from rest_framework.routers import SimpleRouter
from user_center.views.user import UserViewSet
from user_center.views.user_auth import UserAuthViewSet

router = SimpleRouter()
router.register("api/user_center/user", UserViewSet)
router.register("api/user_center/user_auth", UserAuthViewSet)

urlpatterns = [
]
urlpatterns += router.urls