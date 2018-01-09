import requests
import json

twitch_as = requests.get('https://peeringdb.com/api/net/1956')

ix = json.loads(twitch_as.text)
obj = {}

for i in ix['data'][0]['netixlan_set']:
	if i['ix_id'] not in obj:
		obj[i['ix_id']] = i['name']
	    # print u"name: {0}, ix_id: {1}".format(i['name'], i['ix_id'])
obj1 = ','.join([str(x) for x in obj.keys()])


ixurl = "https://peeringdb.com/api/ixlan?id__%s&depth=2" % obj1

print ixurl
ix_as_net = requests.get(ixurl)

ix_as_net = json.loads(ix_as_net.text)

print ix_as_net

# ix_json = json.loads(ix_as_net.text) 

# ix_obj ={}
# for i in ix_json['data'][0]['net_set']:
# 	if i['name'] not in ix_obj:
# 		ix_obj[i['name']] = i['name']

# print ix_obj