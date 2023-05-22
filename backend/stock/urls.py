from rest_framework.routers import SimpleRouter
from stock.views.zt_history import StockZtHistoryViewSet
from stock.views.history import StockHistoryViewSet
from stock.views.trade_date import StockTradeDateViewSet
from stock.views.board_industry import StockBoardIndustryViewSet
from stock.views.board_concept import StockBoardConceptViewSet
from stock.views.board_map import StockBoardMapViewSet
from stock.views.lhb import StockLhbViewSet


router = SimpleRouter()
router.register("api/stock/zt_history", StockZtHistoryViewSet)
router.register("api/stock/history", StockHistoryViewSet)
router.register("api/stock/trade_date", StockTradeDateViewSet)
router.register("api/stock/lhb", StockLhbViewSet)
router.register("api/stock/board/industry", StockBoardIndustryViewSet)
router.register("api/stock/board/concept", StockBoardConceptViewSet)
router.register("api/stock/board/map", StockBoardMapViewSet)

urlpatterns = [
]
urlpatterns += router.urls