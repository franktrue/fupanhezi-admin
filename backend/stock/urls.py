from django.urls import path
from rest_framework.routers import SimpleRouter
from stock.views.zt_history import StockZtHistoryViewSet
from stock.views.history import StockHistoryViewSet
from stock.views.trade_date import StockTradeDateViewSet
from stock.views.board_industry import StockBoardIndustryViewSet
from stock.views.board_concept import StockBoardConceptViewSet
from stock.views.board_map import StockBoardMapViewSet
from stock.views.board_history import StockBoardHistoryViewSet
from stock.views.lhb import StockLhbViewSet
from stock.views.lhb_item import StockLhbItemViewSet
from stock.views.board_sub import StockBoardSubViewSet
from stock.views.api.fenshi import StockFenshiAPI
from stock.views.api.info import StockInfoAPI
from stock.views.api.board import StockBoardAPI
from stock.views.api.board_cons import StockBoardConsAPI
from stock.views.gnn_subject import StockGnnSubjectViewSet
from stock.views.gnn_map import StockGnnMapViewSet
from stock.views.api.config import StockConfigAPI
from stock.views.seat import StockSeatViewSet
from stock.views.seat_office import StockSeatOfficeViewSet
from stock.views.news import StockNewsViewSet
from stock.views.news_tag import StockNewsTagViewSet


router = SimpleRouter()
router.register("api/stock/zt_history", StockZtHistoryViewSet)
router.register("api/stock/history", StockHistoryViewSet)
router.register("api/stock/trade_date", StockTradeDateViewSet)
router.register("api/stock/lhb", StockLhbViewSet)
router.register("api/stock/lhb_item", StockLhbItemViewSet)
router.register("api/stock/board/industry", StockBoardIndustryViewSet)
router.register("api/stock/board/concept", StockBoardConceptViewSet)
router.register("api/stock/board/sub", StockBoardSubViewSet)
router.register("api/stock/board/map", StockBoardMapViewSet)
router.register("api/stock/board/history", StockBoardHistoryViewSet)

router.register("api/stock/gnn_subject", StockGnnSubjectViewSet)
router.register("api/stock/gnn_map", StockGnnMapViewSet)

router.register("api/stock/seat", StockSeatViewSet)
router.register("api/stock/seat_office", StockSeatOfficeViewSet)

router.register("api/stock/news", StockNewsViewSet)
router.register("api/stock/news_tag", StockNewsTagViewSet)


urlpatterns = [
    path("spider/fenshi", StockFenshiAPI.as_view()),
    path("spider/info", StockInfoAPI.as_view()),
    path("spider/board/hot", StockBoardAPI.as_view()),
    path("spider/board/cons", StockBoardConsAPI.as_view()),
    path("spider/config", StockConfigAPI.as_view())
]
urlpatterns += router.urls