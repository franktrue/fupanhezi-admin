from stock.models import StockGnnSubject
from django.db import connections
import requests
import json

class StockGnnSubjectService():

    def fetch(self):
        url = 'http://weapp.upchina.com/weeduapi/hq/getBlockTsLevel'
        data = {
            "stReq": {
                "vBlockCode": []
            }
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            # 先清空
            with connections['default'].cursor() as cursor:
                cursor.execute('TRUNCATE TABLE {0}'.format(StockGnnSubject._meta.db_table))
            json_data = response.json()
            for item in json_data['data']:
                result = self.fetchBasic(item['scode'])
                parent_id = None
                if item['pid']!='-1':
                    parent_id = item['pid']
                model = StockGnnSubject(
                    id = item['id'],
                    parent_id = parent_id,
                    code = item['scode'],
                    name = item['sname'],
                    desc = result['desc'],
                    level = result['level']
                )
                model.save()
        else:
            print('POST请求失败')
        
    def fetchBasic(self, code):
        url = 'http://gateway.uptougu.com/json/hq_fupan_guniuniu/getBlockBasicData'
        data = {
            "stReq": {
                "vecBlk": [
                    {
                        "shtSetcode": 1,
                        "sCode": code
                    }
                ],
                "iCmd": 2
            }
        }
        response2 = requests.post(url, data=json.dumps(data))
        result = {
            "desc": None,
            "level": 1
        }
        if response2.status_code == 200:
            json_data2 = response2.json()
            basic = json_data2['stRsp']['vecDateData'][0]['vecData'][0]['stBlkBasic']
            result['desc'] = basic['sDriveEvent']
            result['level'] = basic['iBlkLevel']
        return result
            