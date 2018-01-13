import requests
import json
import sqlite3

#Open DB connect
db = sqlite3.connect("/home/centos/peering/netix.db")
c = db.cursor()

#Get AS46489's IX information
twitch_as = requests.get('https://peeringdb.com/api/net/1956?depth=1')
ix = json.loads(twitch_as.text)
twitch_netlan_obj = []
ixid = ix['data'][0]['netixlan_set']

for i in ixid:
        if i not in twitch_netlan_obj:
                twitch_netlan_obj.append(i)

netixlan_id = ','.join([str(x) for x in ixid])
netixlan_url = "https://peeringdb.com/api/netixlan?id__in=%s&depth=0" % netixlan_id
netixlan_data = requests.get(netixlan_url)
netixlan_data = json.loads(netixlan_data.text)
ixdataobj = {}

for i in netixlan_data['data']:
	ixdataobj[i['id']] = i['ix_id'],i['name'],i['speed'],i['ipaddr4'],i['ipaddr6']

#Insert IX information to table 
for key ,value in ixdataobj.items():
    c.execute('insert or replace into twitch_ix (ID,IXID,NAME,SPEED,IP4,IP6) VALUES(?,?,?,?,?,?);',(key,value[0],value[1],value[2],value[3],value[4]))


##Query NETID from IXID

db_netixid = c.execute('select distinct IXID from twitch_ix')
ix_netid = []
for i in db_netixid:
	ix_netid.append(i[0])	

ix_netid = ','.join([str(x) for x in ix_netid])

netdata_url = "https://peeringdb.com/api/ixlan?ix_id__in=%s&depth=1" % ix_netid
netdata_data = requests.get(netdata_url)
netdata_data = json.loads(netdata_data.text)
net_setid_value =[]
c.execute('drop table ix_member;')
c.execute('CREATE TABLE ix_member (IXID INT  ,NETID INT)')
db.commit()
for i in netdata_data['data']:
        for y in i['net_set']:
                net_setid = [i['ix_id'],y]
                c.execute('insert or replace into ix_member (IXID,NETID) VALUES (?,?);',(net_setid[0],net_setid[1]))
                if y not in net_setid_value:
                        #print (y)
                        #net_setid = [i['ix_id'],y]
                        #Insert IXID:NETID to table
                        #c.execute('insert or replace into ix_member (IXID,NETID) VALUES (?,?);',(net_setid[0],net_setid[1]))
                        net_setid_value.append(y)
db.commit()
split = round((len(net_setid_value)/3))
split2 = split*2

## Get NET(NAME ASN) from NETID

net_setid_value_1 = ','.join([str(x) for x in net_setid_value[:split]])			
net_setid_value_2 = ','.join([str(x) for x in net_setid_value[split:split2]])
net_setid_value_3 = ','.join([str(x) for x in net_setid_value[split2:]])
netset_data_url_1 = "https://peeringdb.com/api/net?id__in=%s&depth=0" % net_setid_value_1
netset_data_url_2 = "https://peeringdb.com/api/net?id__in=%s&depth=0" % net_setid_value_2
netset_data_url_3 = "https://peeringdb.com/api/net?id__in=%s&depth=0" % net_setid_value_3

netset_data1 = requests.get(netset_data_url_1)
netset_data2 = requests.get(netset_data_url_2)
netset_data3 = requests.get(netset_data_url_3)

netset_data1 = json.loads(netset_data1.text)
netset_data2 = json.loads(netset_data2.text)
netset_data3 = json.loads(netset_data3.text)

netset_obj1 = {}
for i in netset_data1['data']:
        netset_obj1[i['id']] = i['name'],i['asn']

netset_obj2 = {}
for i in netset_data2['data']:
        netset_obj2[i['id']] = i['name'],i['asn']

netset_obj3 = {}
for i in netset_data3['data']:
        netset_obj3[i['id']] = i['name'],i['asn']

#Insert NET information to table

for key ,value in netset_obj1.items():

	c.execute('insert or replace into NETSET (ID,NAME,ASN) VALUES (?,?,?);',(key,value[0],value[1]))

for key ,value in netset_obj2.items():

        c.execute('insert or replace into NETSET (ID,NAME,ASN) VALUES (?,?,?);',(key,value[0],value[1]))

for key ,value in netset_obj3.items():

        c.execute('insert or replace into NETSET (ID,NAME,ASN) VALUES (?,?,?);',(key,value[0],value[1]))



#for key ,value in net_setid.items():
#	print ("{0},{1}".format(key,value))
#	c.execute('insert or replace into ix_member (IXID,NETID) VALUES (?,?);',(key,value))


	


db.commit()
db.close()

