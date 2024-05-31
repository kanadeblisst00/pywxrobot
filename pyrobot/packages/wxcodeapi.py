import json
import traceback
import requests


class WxCodeAPi:
    def __init__(self, host="127.0.0.1", port=23235):
        self.api = f'http://{host}:{port}'
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def post(self, uri, data=None, retry=0):
        if retry > 2:
            return {}
        url = self.api + uri
        post_data = json.dumps(data) if data is not None else None
        try:
            resp = requests.post(url, data=post_data, headers=self.headers, timeout=60)
        except Exception:
            traceback.print_exc()
            return self.post(uri, data, retry+1)
        datas = resp.json()
        if str(datas.get('status')) == '200':
            return datas.get('datas') or datas.get('result')
        else:
            raise Exception(datas.get('err', str(datas)))
    
    def post_stream(self, uri, data, retry=0):
        if retry > 2:
            return {}
        url = self.api + uri
        try:
            resp = requests.post(url, data=json.dumps(data), headers=self.headers, stream=True)
        except Exception:
            traceback.print_exc()
            return self.post_stream(uri, data, retry+1)
        if resp.status_code == 200:
            for chunk in resp.iter_content(chunk_size=None, decode_unicode=True):
                yield chunk
        else:
            return []
       
    def getvideourl(self, objectid, nonceid):
        '''获取视频号信息'''
        uri = "/getvideourl"
        data = {
            "object_id": objectid,
            "nonce_id": nonceid
        }
        return self.post(uri, data)

    
    
    
    
    

    
    
    
    
    


    

    


    
