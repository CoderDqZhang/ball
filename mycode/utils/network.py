import requests
import json

HTTP_STATUS_CODE = {
    400:"",
    401:"",
    402:"",
    403:"",
    404:"",
    405:"",
    406:"",
    407:"",
    412:"",
    414:"",
    500:"",
    501:"",
    502:""
}

header = {"Content-type": "application/json", "Accept": "text/plain"}

def request_post(url,data):
    request_data = requests.post(url=url, json=data, timeout=30)
    if int(request_data.status_code) is 200 | int(request_data.status_code) is 201 :
        print("请求成功")
    else:
        print("请求失败")
    return json.loads(json.dumps(request_data.json()))
