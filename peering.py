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


ixurl = "https://peeringdb.com/api/ixlan/%s?depth=1" % obj1[0]
ixname = requests.get(ixurl)
ixname = json.loads(ixname.text)
obj_list = list(obj.values())

print (obj_list[0])

netobj = []
for i in ixname['data'][0]['net_set'] :
    netid = i
    neturl = "https://peeringdb.com/api/net/%s?depth=0" % netid
    net_idn = requests.get(neturl)
    net_idn = json.loads(net_idn.text)
    print (net_idn['data'][0]['name'])


#print (ixname['data'][0]['net_set'])


# ix_json = json.loads(ix_as_net.text) 

# ix_obj ={}
# for i in ix_json['data'][0]['net_set']:
# 	if i['name'] not in ix_obj:
# 		ix_obj[i['name']] = i['name']

# print ix_obj
