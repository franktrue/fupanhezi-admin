# -*- coding: utf-8 -*-

"""
@author: franktrue
@contact: QQ:807615827
@Created on: 2023/5/21 15:30
@Remark:
"""
from application.celery import app
from stock.models import StockBoardConcept
from stock.services.zt_history import StockZtHistoryService
from stock.services.history import StockHistoryService
from stock.services.trade_date import StockTradeDateService
from stock.services.lhb import StockLhbService
from stock.services.board import StockBoardService
from stock.services.fenshi import StockFenshiService
from celery import shared_task
import akshare as ak
import datetime

# 工作日15:00收盘后运行
@app.task
def task__stock():
    # 更新涨停板
    today = datetime.date.today()
    service1 = StockZtHistoryService()
    service1.fetch(today)
    # 更新行情
    service2 = StockHistoryService()
    service2.update_latest()
    # 清空表格缓存
    service3 = StockTradeDateService()
    service3.clearCache()
    # 更新概念指数数据
    service4 = StockBoardService()
    service4.fetch_history(trade_date=today)
    
# 工作日18:05收盘后运行
@app.task
def task__lhb():
    # 更新涨停板
    today = datetime.date.today()
    service = StockLhbService()
    service.fetch(today)

# 每日凌晨更新概念及成分股
@app.task 
def task__board():
    i = 0
    df1 = ak.stock_board_concept_name_ths()
    df1.columns = ['release_date', 'name', 'include_number', 'show_url', 'code']
    for row in df1.itertuples():
        board = StockBoardConcept.objects.filter(code=row.code).first()
        if board is None:
            board = StockBoardConcept(
                name = row.name,
                code = row.code,
                release_date = row.release_date,
                include_number = row.include_number,
                show_url = row.show_url
            )
        elif board.include_number != row.include_number or board.name != row.name:
            board.include_number = row.include_number
            board.release_date = row.release_date
            board.name = row.name
        else:
            continue
        board.save()
        update_board_cons.apply_async((row.code, row.name, 'concept'), countdown = 4*i)
        i = i+1
    df2 = ak.stock_board_industry_name_ths()
    for row in df2.itertuples():
        # 每隔任务间隔5s防止触发保护机制
        update_board_cons.apply_async((row.code, row.name, 'industry'), countdown = 4*i)
        i = i+1
    return "操作成功"

# 每日收盘后更新
@app.task
def task__update_fenshi():
    stock_history = ak.stock_zh_a_spot_em()
    stock_history = stock_history[['代码', '名称', '今开', '最新价', '最高', '最低']]
    stock_history.columns = ['stock_code', 'stock_name', 'open', 'close', 'high', 'low']
    stock_history = stock_history.dropna(subset=['open', 'high', 'low', 'close'])
    trade_date = datetime.date.today().strftime("%Y-%m-%d")
    for row in stock_history.itertuples():
        sync_stock_fenshi.delay(row.stock_code, trade_date)
        print(row.stock_code)
    return "SUCCESS"


@shared_task
def update_auction(date):
    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').date()
    service = StockHistoryService()
    service.update_auction_by_date(date)

@shared_task
def update_board_cons(symbol, name, type):
    service = StockBoardService()
    service.update_cons(symbol, name, type)

@shared_task
def update_board_history(trade_date):
    service = StockBoardService()
    service.fetch_history_by_task(trade_date)

@shared_task
def sync_stock_fenshi(stock_code, trade_date):
    service = StockFenshiService()
    service.sync(stock_code=stock_code, date=trade_date)
    