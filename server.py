from flask import Flask, jsonify,request

from datascience import Table
from intervaltree import Interval, IntervalTree

prefixcode = ''

t = Table.read_table('CourseWhere.csv')
trees = {day:IntervalTree() for day in ['M','T','W','R','F','S']}
for row in t.rows:
    for day in row[5]:
        trees[day][row[6]:row[7]] = row

room_table = t.group('Building',collect=set).select(['Building','Facility set'])
room_list = {building.lower():rooms for building,rooms in zip(room_table['Building'],room_table['Facility set'])}


app = Flask(__name__)

def class_to_dict(clas):
    convert = lambda x: x if isinstance(x,str) else int(x)
    return {label:convert(v) for label,v in zip(t.column_labels,clas)}

@app.route(prefixcode+'/rooms/<building>/<room>')
def get_room(building,room):
    weekday = request.args.get('day', 'M')
    if weekday not in "MTWRFS":
        weekday = 'M'
    values = [class_to_dict(v) for v in t.where('Building',building).where('Room',room).rows]
    values = [v for v in values if weekday in v['Days']]
    values = sorted(values,key=lambda x:x['Start'])
    return jsonify(data=values)

def convert_if_possible(value,function,default):
    try:
        return function(value)
    except:
        return default

@app.route(prefixcode+'/buildings/<building>')
def get_building(building):
    if building not in room_list:
        building = 'evans'
    weekday = request.args.get('day', 'M')
    if weekday not in "MTWRFS":
        weekday = 'M'
    start = request.args.get('start', '1000')
    end = request.args.get('end', '1100')
    start = convert_if_possible(start, int, 1000)
    end = convert_if_possible(end, int, 1100)
    print(weekday, start, end, building)
    return jsonify(data=find_all(weekday, start, end, building))


@app.route(prefixcode+'/')
def index():
    return open('index.html').read()

@app.route('/get/buildings')
def get_buildings():
    weekday = request.args.get('day', 'M')
    if weekday not in "MTWRFS":
        weekday = 'M'
    start = request.args.get('start', '1000')
    start = convert_if_possible(start, int, 1000)
    all_buildings = [(room,next(iter(room_list[room])).rsplit(' ',1)[0],num_empty(room,weekday,start)) for room in room_list]
    all_buildings = sorted(all_buildings,key=lambda x: -1*len(room_list[x[0]]))
    return jsonify(data=all_buildings)

def num_empty(building,day,time):
    return len(room_list[building])-len([v for v in trees[day][time] if v.data[8]==building])

import time

def find_all(day,start,end,location='evans'):
    vals = trees[day][start:end]
    vals = [v for v in vals if v.data[8]==location]
    besttimes = list()
    for room in room_list[location]:
        possible = [v.data[6] for v in vals if v.data[4]==room]
        if len(possible) > 0:
            last = int(max(min(possible),start))
            besttimes.append([room,last,False,time_diff(start,last)])
        else:
            besttimes.append([room,end,True,time_diff(start,end)])
    return sorted(sorted(besttimes,key=lambda x: len(x[0])),key=lambda x: -1*x[1])

def time_diff(start,end):
    return (end//100-start//100)*60 + (end%100-start%100)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')