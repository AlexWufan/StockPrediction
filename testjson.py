from datetime import datetime
import json
import svm
import pandas as pd
import datetime
import calendar
from flask import jsonify

data = []
predicted_data = svm.svm_predict(30, 0, 'AAPL')
for x in predicted_data:
    data.append(round(x,3))
utc = []

today = datetime.date.today()
thirtyday = datetime.timedelta(days=29)

daterange = pd.date_range(today, today + thirtyday)
for single_date in daterange:
    utc.append(calendar.timegm(single_date.timetuple()))

json_data=[]

for x in range(1,31):
    json_data.append([utc[x-1],data[x-1]])
# print json.dumps(json_data, separators=(',',','))

b = '''(
[1461110400000,107.13],
[1461196800000,105.97],
[1461283200000,105.68],
[1461542400000,105.08],
[1461628800000,104.35],
[1461715200000,97.82]
]);'''

print json.dumps(b)