from flask import request, url_for, render_template
from app import app
from utils import get_db_connection
from models.editor_model import *
from math import isnan


@app.route('/editor', methods=['GET', 'POST'])
def editor():
    conn = get_db_connection()
    content = {}
    content_type = 'classes'
    content['classes'] = get_classes(conn)
    if request.method == 'POST':
        if 'new_class_name' in request.form.keys():
            add_class(conn, request.form['new_class_name'])
        elif 'classes' in request.form.keys():
            delete_classes(conn, request.form.getlist('classes'))
        content['classes'] = get_classes(conn)
    html = render_template('editor.html',
                           content=content,
                           content_type=content_type)
    return html


@app.route('/editor/property', methods=["GET", "POST"])
def property():
    conn = get_db_connection()
    content = {'types': get_property_types(conn), 'properties': get_properties(conn)}
    content_type = 'properties'
    if request.method == 'POST':
        if 'new_property_name' in request.form.keys():
            add_property(conn, request.form['new_property_name'], request.form['properties_types'])
        elif 'properties' in request.form.keys():
            delete_properties(conn, request.form.getlist('properties'))
        content['properties'] = get_properties(conn)

    html = render_template('editor.html',
                           content=content,
                           content_type=content_type)
    return html


@app.route('/editor/relevant', methods=['GET', 'POST'])
def relevant_values():
    conn = get_db_connection()
    content = {'properties': get_full_properties(conn)}
    content_type = 'relevant_values'
    if request.method == 'POST':
        if request.form['from'] == '' or request.form['to'] == '' or float(request.form['from']) > float(request.form['to']):
            print('Ошибка: какое-то из значений от/до не введено, или значение "от" больше, чем "до"')
        else:
            add_relevant_values(conn, request.form['properties_list'], request.form['from'], request.form['to'])
    html = render_template('editor.html',
                           content=content,
                           content_type=content_type)
    return html


@app.route('/editor/property-class', methods=['GET', 'POST'])
def property_class():
    conn = get_db_connection()
    content = {'classes': get_classes(conn), 'properties': get_full_properties(conn)}
    content_type = 'property_class'
    if request.method == "POST":
        edit_property_for_class(conn, request.form['classes'], request.form.getlist('properties'))

    html = render_template('editor.html',
                           content=content,
                           content_type=content_type)
    return html


@app.route('/editor/relevant-class', methods=['GET', 'POST'])
def relevant_class():
    conn = get_db_connection()
    content = {'classes': get_classes(conn), 'properties': get_full_properties(conn)}
    content_type = 'relevant-class'
    if request.method == 'POST':
        min_value, max_value = get_minmax_value(conn, request.form['properties'])
        if request.form['from'] == '' or request.form['to'] == '' or float(request.form['from']) > float(request.form['to']):
            print('Ошибка: какое-то из значений от/до не введено, или значение "от" больше, чем "до"')
        elif (min_value is not None and float(request.form['from']) < min_value) or (max_value is not None and float(request.form['to']) > max_value):
            print('Ошибка: какое-то из значений от/до меньше/больше, чем минимальное/максимальное допустимое значение для этого признака')
        else:
            add_relevant_values_for_class(conn, request.form['classes'], request.form['properties'], request.form['from'], request.form['to'])

    html = render_template('editor.html',
                           content=content,
                           content_type=content_type)
    return html


@app.route('/editor/completeness', methods=['GET'])
def completeness():
    conn = get_db_connection()
    data = get_classes_properties(conn)
    messages = []
    for index, item in data.iterrows():
        if isnan(item['min_value']):
            messages.append(f'Для класса {item['class_name']}, признака {item['property_name']} не указано минимальное значение.')
        if isnan(item['max_value']):
            messages.append(f'Для класса {item['class_name']}, признака {item['property_name']} не указано максимальное значение.')
    content = {'messages': messages}
    content_type = 'completeness'

    html = render_template('editor.html',
                           content=content,
                           content_type=content_type)
    return html
