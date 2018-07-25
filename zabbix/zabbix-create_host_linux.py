#!/usr/bin/env python
# Version = 3.6.1
# __auth__ = 'syavingc'

import json
from urllib import request, parse

ZABBIX_URL = 'http://127.0.0.1/zabbix'
ZABBIX_USERNAME = "Admin"
ZABBIX_PASSWORD = "passwd"
#定义要添加自己的列表
hostlist=["172.30.88.19","172.30.101.253","172.30.101.208","172.30.100.80","172.30.66.145","172.30.103.5","172.30.103.204","172.30.102.105"]
#hostlist=[]
for host in hostlist:
    url = "{}/api_jsonrpc.php".format(ZABBIX_URL)
    header = {"Content-Type": "application/json"}
    data = {
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": host,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": host,
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": [
                {
                    "groupid": "2"
                }
            ],
            "templates": [
                {
                    "templateid": "10001"

                }
            ],
            "inventory_mode": 0,
            "inventory": {
                "macaddress_a": "01234",
                "macaddress_b": "56768"
            }
        },
        "auth": "66e14bdff60f8490a57108bc0704fce9",
        "id": 1
    }
    # 由于API接收的是json字符串，故需要转化一下
    value = json.dumps(data).encode('utf-8')

    # 对请求进行包装
    req = request.Request(url, headers=header, data=value)

    # 验证并获取Auth ID
    try:
        # 打开包装过的url
        result = request.urlopen(req)
    except Exception as e:
        print("Auth Failed, Please Check Your Name And Password:", e)
    else:
        response = result.read()
        # 上面获取的是bytes类型数据，故需要decode转化成字符串
        page = response.decode('utf-8')
        # 将此json字符串转化为python字典
        page = json.loads(page)
        result.close()
        print("Create host Successful. The host ID Is: {}".format(page.get('result')))