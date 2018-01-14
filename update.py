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
con.execute('drop table merge_new')
con.commit()
#update merge DB

twitch_ix = con.execute('select DISTINCT twitch_ix.IXID from twitch_ix')

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
