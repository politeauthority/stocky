import requests
import json
import urllib

url = 'http://127.0.0.1/api/quotes'
headers = {'Content-Type': 'application/json'}

filters = [dict(name='company_id', op='eq', val=1293)]

params = dict(q=json.dumps(dict(filters=filters)))

# response = requests.get(url, params=params, headers=headers)
# print url
# print response.status_code
# print(response.json())


filters = [dict(name='company_id', op='eq', val=1293)]

params = dict(q=json.dumps(dict(filters=filters)))

xfilters = {
    'name': 'company_id',
    'op': 'eq',
    'val': 1293
}
print "%s?%s" % (url, urllib.urlencode(xfilters))
