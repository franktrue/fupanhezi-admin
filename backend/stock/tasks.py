# -*- coding: utf-8 -*-

"""
@author: franktrue
@contact: QQ:807615827
@Created on: 2023/5/21 15:30
@Remark:
"""
from application.celery import app
from stock.services.zt_history import StockZtHistoryService
from stock.services.history import StockHistoryService
from stock.services.lhb import StockLhbService
from celery import shared_task
import datetime

# 工作日15:05收盘后运行
@app.task
def task__history():
    # 更新行情
    service = StockHistoryService()
    service.update_latest()

# 工作日15:10收盘后运行
@app.task
def task__zt_history():
    # 更新涨停板
    today = datetime.date.today()
    service = StockZtHistoryService()
    service.fetch(today)

# 工作日18:05收盘后运行
@app.task
def task__lhb():
    # 更新涨停板
    today = datetime.date.today()
    service = StockLhbService()
    service.fetch(today)

@shared_task
def update_auction(date):
    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S').date()
    service = StockHistoryService()
    service.update_auction_by_date(date)