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
    df = ak.stock_board_concept_name_ths()
    df.columns = ['release_date', 'name', 'include_number', 'show_url', 'code']
    for row in df.itertuples():
        board = StockBoardConcept.objects.filter(code=row.code).first()
        if board is None:
            board = StockBoardConcept(
                name = row.name,
                code = row.code,
                release_date = row.release_date,
                include_number = row.include_number,
                show_url = row.show_url
            )
        elif board.include_number != row.include_number:
            board.include_number = row.include_number
        else:
            continue
        board.save()
        update_board_cons.delay(row.code, row.name, 'concept')
    return "操作成功"

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
def update_board_history(symbol):
    service = StockBoardService()
    service.fetch_history(symbol)
    