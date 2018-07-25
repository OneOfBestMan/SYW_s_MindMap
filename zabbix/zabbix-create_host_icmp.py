#!/usr/bin/env python
# Version = 3.6.1
# __auth__ = 'warren'
import json
from urllib import request, parse

ZABBIX_URL = 'http://127.0.0.1/zabbix'
ZABBIX_USERNAME = "Admin"
ZABBIX_PASSWORD = "passwd"
#定义要添加自己的列表
hostlist=["192.168.3.90"]
for host in hostlist:
    url = "{}/api_jsonrpc.php".format(ZABBIX_URL)
    header = {"Content-Type": "application/json"}
    # auth user and password
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
                    "templateid": "10104"
                }
            ],
            "inventory_mode": 0,
            "inventory": {
                "macaddress_a": "01234",
                "macaddress_b": "56768"
            }
        },
        "auth": "9afc764edb5b6bbd09369f7028231b70",
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