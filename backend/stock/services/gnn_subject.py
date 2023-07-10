from stock.models import StockGnnSubject
import requests
import json

class StockGnnSubjectService():

    def fetch(self):
        url1 = 'http://weapp.upchina.com/weeduapi/hq/getBlockTsLevel'
        data1 = {
            "stReq": {
                "vBlockCode": []
            }
        }
        response1 = requests.post(url1, data=data1)
        if response1.status_code == 200:
            # 先清空
            StockGnnSubject.objects.all().delete()
            json_data1 = response1.json()
            for item in json_data1['data']:
                url2 = 'http://gateway.uptougu.com/json/hq_fupan_guniuniu/getBlockBasicData'
                data2 = {
                    "stReq": {
                        "vecBlk": [
                            {
                                "shtSetcode": 1,
                                "sCode": item['scode']
                            }
                        ],
                        "iCmd": 2
                    }
                }
                response2 = requests.post(url2, data=json.dumps(data2))
                desc = None
                level = 1
                if response2.status_code == 200:
                    json_data2 = response2.json()
                    basic = json_data2['stRsp']['vecDateData'][0]['vecData'][0]['stBlkBasic']
                    desc = basic['sDriveEvent']
                    level = basic['iBlkLevel']
                parent_id = None
                if item['pid']!='-1':
                    parent_id = item['pid']
                model = StockGnnSubject(
                    id = item['id'],
                    parent_id = parent_id,
                    code = item['scode'],
                    name = item['sname'],
                    desc = desc,
                    level = level
                )
                model.save()
        else:
            print('POST请求失败')