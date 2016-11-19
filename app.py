from flask import Flask, session, request, redirect, url_for, render_template, abort, jsonify
import sqlite3 as lite
from flask import make_response
import svm
import MLP
import bayes
import datetime
import json
import calendar
import pandas as pd
from dateutil.relativedelta import relativedelta

#####
import fetchdata
import numpy as np
from sklearn.svm import SVR

app = Flask(__name__)


# Check Configuration section for more details
# SESSION_TYPE = 'redis'
# app.config.from_object(__name__)
# Session(app)

@app.route('/', methods=['GET', 'POST'])
def route():
    if request.method == 'POST':
        #pdb.set_trace()
        # return '<h3>please log in firstly.</h3>'
        if request.form.values():
            # return redirect(url_for('search', par=str(request.form['stockid'])))
            return render_template('search.html', par = str(request.form['stockid']))
    return render_template('base.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #pdb.set_trace()
        #return '<h3>please log in firstly.</h3>'
        if request.form.values():
            # json = createjson(request.form['stockid'])
            # return '<h3>please log in firstly.</h3>'
            # pdb.set_trace()
            # return render_template('predict.html', par = str(request.form['stockid']))
            # return str(request.form['stockid'])
            # return redirect(url_for('predict'))
            return render_template('predict.html')

    return render_template('index.html')


@app.route('/realtime', methods=['GET', 'POST'])
def realtime(chartID = 'chart_ID', chart_type = 'line', chart_height = 350):
    if request.method == 'POST':
        result = bayes.bayes_predict(request.form['stockid'])
        listtime = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
        series = [{"name": 'The 11th price is the predicted data', "data": result}]
        # return '<h3>please log in firstly.</h3>'
        title = {"text": 'Real time predicted price'}
        xAxis = {"categories": listtime}
        yAxis = {"title": {"text": 'yAxis Label'}}
        return render_template('realtime.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                               yAxis=yAxis, text=result[-1])
    return render_template('realtime.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict(chartID = 'chart_ID', chart_type = 'line', chart_height = 350):
    if request.method == 'POST':
        listtime = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        liststock = svm.svm_predict(15, 0, str(request.form['stockid']))
        liststock1 = MLP.mlp_predict(15, 0, str(request.form['stockid']))
        chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
        series = [{"name": 'SVM', "data": liststock}, {"name": 'MLP', "data": liststock1}]
        # return '<h3>please log in firstly.</h3>'
        title = {"text": 'Price in future 15 days'}
        xAxis = {"categories": listtime}
        yAxis = {"title": {"text": 'yAxis Label'}}
        return render_template('predict.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                               yAxis=yAxis)
    return render_template('predict.html')



@app.route('/search')
def search():
    return render_template('search.html')

# @app.route('/predict')
# def predict():
#     return render_template('predict.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404




@app.route('/signin', methods=['POST'])
def signin():
    conn = lite.connect('StockHistory.db')
    cursor = conn.cursor()
    cursor.execute('select Pwd from Users where UserID=' + request.form['username'])
    array = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    if request.form['password'] == array[0][0]:
        session['user'] = request.form['username']
        return redirect(url_for('predict'))
        # return render_template('problem2.html', form=form)
    return '<h3>Bad username or password.</h3>'

def getquery(strquery):
    conn = lite.connect('StockHistory.db')
    cursor = conn.cursor()
    cursor.execute(strquery)
    array = cursor.fetchall()
    listPrice =[]
    # for i in array:
    #   listPrice.append(str(i[0]))
    conn.commit()
    cursor.close()
    conn.close()
    return array

lastdate = getquery("select Max(TadeTime) from HistoryValue")

def query1():
    return getquery("Select distinct Symbol, ClosePrice from HistoryValue group by  Symbol ")


def query2(stockname, Ddays=10):
    tenday = datetime.timedelta(days=Ddays)
    requiredate = datetime.datetime.strptime(str(lastdate[0][0]), '%Y-%m-%d') - tenday
    requiredate=str(requiredate)[:-9]
    return getquery("select Max(ClosePrice) from HistoryValue where Symbol = '" +stockname +"' and TadeTime between '" + requiredate +"'and '"+lastdate[0][0]+"'")

def query3(stockname, Ddays=365):
    tenday = datetime.timedelta(days=Ddays)
    requiredate = datetime.datetime.strptime(str(lastdate[0][0]), '%Y-%m-%d') - tenday
    requiredate=str(requiredate)[:-9]
    return getquery("select Avg(ClosePrice) from HistoryValue where Symbol = '" +stockname +"' and TadeTime between '" + requiredate +"'and '"+lastdate[0][0]+"'")

def query4(stockname, Yyears=1):
    requiredate = datetime.datetime.strptime(str(lastdate[0][0]), '%Y-%m-%d')  - relativedelta(years=Yyears)
    requiredate=str(requiredate)[:-9]
    return getquery("select Symbol, min(ClosePrice) from HistoryValue where TadeTime between '" + requiredate +"'and '"+lastdate[0][0]+"' group by Symbol"  )

def query5(stockname, Yyears=365):
    requiredate = datetime.datetime.strptime(str(lastdate[0][0]), '%Y-%m-%d')  - relativedelta(years=Yyears)
    requiredate=str(requiredate)[:-9]
    data = getquery("select Symbol, min(ClosePrice) from HistoryValue where Symbol ='GOOG' and TadeTime between '" + requiredate +"'and '"+lastdate[0][0]+"' group by Symbol"  )
    return getquery("select Symbol, Avg(ClosePrice) from HistoryValue where TadeTime between '" + requiredate +"'and '"+lastdate[0][0]+"' group by Symbol having Avg(ClosePrice) < '"+str(data[0][1])+"' "  )


#problem1
@app.route('/query/api/v1.0/get/task1', methods=['GET'])
def get_task1():
    return json.dumps(query1())
# problem2
@app.route('/query/api/v1.0/get/task2/<string:stock_name>/<int:tendays>', methods=['GET'])
def get_task2(stock_name,tendays):
    return json.dumps(query2(stock_name,tendays)[0])

#problem3
@app.route('/query/api/v1.0/get/task3/<string:stock_name>/<int:tendays>', methods=['GET'])
def get_task3(stock_name,tendays):
    return json.dumps(query3(stock_name,tendays)[0])

#problem3
@app.route('/query/api/v1.0/get/task4/<string:stock_name>/<int:Years>', methods=['GET'])
def get_task4(stock_name,Years):
    return json.dumps(query3(stock_name,Years)[0])

#problem3
@app.route('/query/api/v1.0/get/task5/<string:stock_name>/<int:Years>', methods=['GET'])
def get_task5(stock_name,Years):
    return json.dumps(query3(stock_name,Years)[0])

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# @app.route('/query/api/v1.0/post/tasks', methods=['POST'])
# def create_task():
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     tasks.append(task)
#     return jsonify({'task': task}), 201
##############################graph




def getdate():
    name = session['name']
    conn = lite.connect('StockHistory.db')
    cursor = conn.cursor()
    #where Symbol ='"+ name +"' and TadeTime between '"+session['begindate'] +"'and '"+session['enddate']+"'"
    cursor.execute("select distinct TadeTime from HistoryValue where TadeTime between '2016-01-01'and '2016-01-10'")
    array = cursor.fetchall()
    listPrice =[]
    for i in array:
      listPrice.append(str(i[0]))
    conn.commit()
    cursor.close()
    conn.close()
########################
if __name__ == '__main__':
    # app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
