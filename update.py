# This Script is for merge DB to get What AS under IX .


import sqlite3
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
con= sqlite3.connect("/home/centos/peering/netix.db")
con.row_factory = dict_factory
cur = con.cursor()
get = con.execute('select twitch_ix.NAME,twitch_ix.SPEED,twitch_ix.IP4,twitch_ix.IP6 from twitch_ix')
NETSETID = con.execute('select twitch_ix.NAME,ix_member.NETID ,merge.NETNAME,merge.ASN  from ix_member,merge,twitch_ix where merge.IXID = twitch_ix.IXID;')
test = con.execute('select NETSET.NAME ,ix_member.IXID from NETSET , ix_member where ix_member.NETID = NETSET.ID;')

new = con.execute('select NETSET.NAME ,ix_member.IXID,NETSET.ASN ,twitch_ix.NAME from NETSET , twitch_ix, ix_member where ix_member.NETID = NETSET.ID;')

#update merge DB

twitch_ix = con.execute('select DISTINCT twitch_ix.IXID from twitch_ix')
net_data = con.execute('select * from NETSET')
for i in twitch_ix:
	ik = (i['IXID'],)
	pi = con.execute('select NAME from twitch_ix where IXID =?',ik)
	for io in pi:
		pi = io	
	ix_net = con.execute('select ix_member.NETID from ix_member where ix_member.IXID = ?',ik)
	
	for u in ix_net:
		kb = (u['NETID'],)
		pp = con.execute('select NETSET.NAME ,NETSET.ASN from NETSET where NETSET.ID = ?',kb)
		for ll in pp:	
			con.execute('insert or replace into merge_new (IXNAME,NAME,ASN) VALUES(?,?,?);',(pi['NAME'],ll['NAME'],ll['ASN']))

con.commit()
con.close()
