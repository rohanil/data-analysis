from flask import Flask, render_template,url_for, Markup, request, session, abort, redirect, flash
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import pymysql
from sqlalchemy import *
import time
from operator import itemgetter
from itertools import groupby

SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'adminpwd'
#def create_app(configfile=None):
app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)

if app.debug is not True:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.ERROR)
    app.logger.setLevel(logging.ERROR)
    app.logger.addHandler(file_handler)

@app.route('/stats')
def display():
    start_time = time.time()
    db = pymysql.connect("localhost",user= "root",db="dump_test")
    cur = db.cursor()
    
    #group by reseller name , date, accounts on that date
    cur.execute("""
        SELECT a.v3, b.c3, SUM(b.c4), b.c2 FROM t1 as a inner join t2 as b on a.v2=b.c2 GROUP BY a.v3, b.c3""")
    data_table = cur.fetchall()

    #graph of data 

    sorted_data_table = sorted(data_table, key=itemgetter(0,1))

    groups = groupby(sorted_data_table, key=itemgetter(0))
    graph_data =[]
    for k, v in groups:
        graph_data.append({'name':k, 'data':[[1000*time.mktime(x[1].timetuple()), int(x[2])] for x in v]})
    

    #gather dates for table
    cur.execute("select c3 from t2 group by c3")
    seq = cur.fetchall()
    seq = sorted(seq, key=itemgetter(0), reverse=True)
    today = seq[0][0]
    yesterday = seq[1][0]
    start = min(seq)[0]
    
    #get table data
    c_array=[]
    table_data=[]
    for row in data_table:
        temp=row[0]
        if temp not in c_array:
            c_array.append(temp)
            b =[item[2] for item in data_table if item[0] == temp and item[1] in [today, yesterday, start]]
            todays = b[2]
	    yesterdays = b[1]
	    
	    starts = b[0]
            x = percent_diff(todays,yesterdays)
            
            y= percent_diff(todays,starts)
            table_data.append({'name': temp, 'today':todays, 'yesterday': yesterdays, 'diff': round(x,2), 'initial': starts, 'diff2': round(y,2)})

    
    total_today= sum(item[2] for item in data_table if item[1] == today)
    total_yesterday= sum(item[2] for item in data_table if item[1] == yesterday)
    
    total_initial= sum(item[2] for item in data_table if item[1] == start)
    x = percent_diff(total_today,total_yesterday)
    
    y = percent_diff(total_today,total_initial)
    table_data.append({'name': 'Total', 'today':total_today, 'yesterday': total_yesterday, 'diff': round(x,2), 'initial': total_initial, 'diff2': round(y,2)})
    table_data_sorted = sorted(table_data, key=itemgetter('today'), reverse=True)

    
    return render_template('table.html', result=table_data_sorted, olddate=yesterday, initialdate=start, chartID2="chart2", graph_data=graph_data, total_today=total_today)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('display'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


def percent_diff(x,y):
    if int(y) == 0:
        return 0.0
    else:
        temp = float(y-x)*100/float(y)
        return temp


#    return app


if __name__ == '__main__':
    app.run()
