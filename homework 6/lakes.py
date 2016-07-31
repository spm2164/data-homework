from flask import Flask, jsonify, request
import pg8000
conn=pg8000.connect(database='mondial', password='1234')

def lake_to_dict(lake_response):
    lake_list=[]
    for lake in lake_response:
        lake_info={}
        lake_info['name']=lake[0]
        if lake[1]:
            lake_info['elevation']=float(lake[1])
        else:
            lake_info['elevation']=None
        if lake[2]:
            lake_info['area']=float(lake[2])
        else:
            lake_info['area']=None
        lake_info['type']=str(lake[3])
        lake_list.append(lake_info)
    return lake_list

def cursor_get(query, specifier):
    cursor=conn.cursor()
    if specifier:
        cursor.execute(query, [specifier])
    else:
        cursor.execute(query)
    return cursor.fetchall()

app = Flask(__name__)
@app.route("/lakes")
def lake_lookup():
    output=[]
    get_type=request.args.get('type', 0)
    get_sort=request.args.get('sort', 0)
    if get_type:
        if get_sort=='elevation':
            query="select name, elevation, area, type from lake where type = %s order by elevation desc"
            output=lake_to_dict(cursor_get(query, get_type))
        elif get_sort=='area':
            query="select name, elevation, area, type from lake where type = %s order by area desc"
            output=lake_to_dict(cursor_get(query, get_type))
        elif get_sort:
            query="select name, elevation, area, type from lake where type = %s order by name asc"
            output=lake_to_dict(cursor_get(query, get_type))
        else:
            query="select name, elevation, area, type from lake where type = %s"
            output=lake_to_dict(cursor_get(query, get_type))
    else:
        if get_sort=='elevation':
            query="select name, elevation, area, type from lake order by elevation desc"
            output=lake_to_dict(cursor_get(query, get_type))
        elif get_sort=='area':
            query="select name, elevation, area, type from lake order by area desc"
            output=lake_to_dict(cursor_get(query, get_type))
        elif get_sort:
            query="select name, elevation, area, type from lake order by name asc"
            output=lake_to_dict(cursor_get(query, get_type))
        else:
            query="select name, elevation, area, type from lake"
            output=lake_to_dict(cursor_get(query, get_type))
    return jsonify(output)
app.run()
