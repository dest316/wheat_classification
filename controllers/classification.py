from app import app
from flask import request, url_for, render_template, redirect
from models.classification_model import get_properties, get_properties_by_class, get_classes, check_completeness
from utils import get_db_connection


@app.route('/classification', methods=["GET", "POST"])
def classification():
    conn = get_db_connection()
    if not check_completeness(conn):
        return redirect(url_for('completeness'))
    data = get_properties(conn)
    logs = None
    result = None
    if request.method == 'POST':
        gotten_data = {}
        for i in request.form.items():
            if 'input_' in i[0] and i[1] != '':
                gotten_data[i[0][6:]] = float(i[1])
        classes = get_classes(conn)
        result = []
        logs = []
        for index, item in classes.iterrows():
            flag = True
            for index1, it in get_properties_by_class(conn, item['class_id']).iterrows():
                if not it['property_name'] in gotten_data:
                    continue
                if gotten_data[it['property_name']] < it['min_value'] or gotten_data[it['property_name']] > it['max_value']:
                    flag = False
                    logs.append((item['class_name'], it['property_name'], it['min_value'], it['max_value']))
            if flag:
                result.append(item['class_name'])

    html = render_template('classification.html',
                           data=data,
                           logs=logs,
                           result=result,
                           root_route=request.url_root)
    return html
