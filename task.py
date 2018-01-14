from flask import Flask , render_template ,request,g
import sqlite3
import jinja2
app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
con= sqlite3.connect("/home/centos/peering/netix.db")
con.row_factory = dict_factory
cur = con.cursor()
@app.route('/')
def index():
	s1 = 0
	twitch_ix = con.execute('select twitch_ix.NAME,twitch_ix.SPEED,twitch_ix.IP4,twitch_ix.IP6 from twitch_ix order by NAME ASC')
	member = con.execute('select * from merge_new order by IXNAME ASC ')
	speed = con.execute('select SPEED from twitch_ix')
	for i in speed:
		s1 += i['SPEED']
	s1 = s1/1000
	return render_template('new_index.htm',twitch_ix = twitch_ix,member=member,speed=s1)

app.config.from_object(__name__)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80,)
