from coupon.models import CouponsModel, CouponScenesModel
from user_center.models import UserCoupon
from datetime import datetime, timedelta

class CouponService():
    def send(self, scene_id, user_id):
        scene = CouponScenesModel.objects.get(id = scene_id)
        if scene is None:
            return None
        coupon = CouponsModel.objects.get(id = scene.coupon_id)
        if coupon is None:
            return None
        now = datetime.now()
        if coupon.expire_type == "countdown":
            start = now
            end = start + timedelta(days=coupon.days)
        else:
            start = coupon.start_time
            end = coupon.end_time

        return UserCoupon.objects.create(
            user_id = user_id,
            coupon_id = scene.coupon_id,
            agent_id = scene.agent_id,
            claimed_time = now,
            name = coupon.name,
            goods_id = scene.goods_id,
            type = coupon.type,
            value = coupon.value,
            min_amount = coupon.min_amount,
            start_time = start,
            end_time = end
        )