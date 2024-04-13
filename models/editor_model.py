import pandas as pd
from models.classification_model import get_properties, get_classes


def add_class(conn, class_name):
    cur = conn.cursor()
    if pd.read_sql(f'''SELECT * FROM classes WHERE class_name='{class_name}';''', conn).size == 0:
        cur.execute(f'''INSERT INTO classes (class_name)
        VALUES ('{class_name}')''')
        conn.commit()
    else:
        print(f'Ошибка: класс с именем "{class_name}" уже есть')


def delete_classes(conn, list_to_delete):
    cur = conn.cursor()
    cur.execute(f'''DELETE FROM classes_properties
    WHERE class_id IN ({','.join(list_to_delete)});
''')
    cur.execute(f'''DELETE FROM classes
        WHERE class_id IN ({','.join(list_to_delete)});
                ''')
    conn.commit()


def get_property_types(conn):
    return pd.read_sql(f'''
    SELECT * FROM property_types;
''', conn)


def add_property(conn, property_name, property_type_id):
    if pd.read_sql(f'''SELECT * FROM properties WHERE property_name='{property_name}';''', conn).size == 0:
        cur = conn.cursor()
        cur.execute(f'''INSERT INTO properties (property_name, property_type_id)
        VALUES ('{property_name}', {property_type_id})''')
        conn.commit()
    else:
        print(f'Ошибка: признак с именем "{property_name}" уже есть')


def delete_properties(conn, list_to_delete):
    cur = conn.cursor()
    cur.execute(f'''DELETE FROM classes_properties
        WHERE property_id IN ({','.join(list_to_delete)});
    ''')
    cur.execute(f'''DELETE FROM classes
            WHERE property_id IN ({','.join(list_to_delete)});
                    ''')
    conn.commit()


def get_full_properties(conn):
    df = pd.read_sql(f'''
SELECT * FROM properties JOIN property_types USING (property_type_id);''', conn)
    return df


def add_relevant_values(conn, id, from_data, to_data):
    cur = conn.cursor()
    cur.execute(f'''
UPDATE properties
SET min_value={from_data}, max_value={to_data}
WHERE property_id = {id}''')
    conn.commit()


def edit_property_for_class(conn, class_id, property_list):
    cur = conn.cursor()
    df = pd.read_sql(f'''
SELECT * FROM classes_properties WHERE class_id = {class_id}''', conn)['property_id']
    # Получить разность множеств property_list и df. Добавить элементы только property_list в бд, элементы только из df - удалить
    added_elems = list(set(property_list) - set(df.to_list()))
    deleted_elems = list(set(df.to_list()) - set(property_list))
    delete_property_class(cur, deleted_elems, class_id)
    add_property_class(cur, added_elems, class_id)
    conn.commit()


def add_property_class(cur, list_of_id, class_id):
    query = f'''INSERT INTO classes_properties (class_id, property_id) VALUES '''
    for record in list_of_id:
        query += f'({class_id}, {record}), '
    query = query.rstrip(', ') + ';'
    cur.execute(query)


def delete_property_class(cur, list_of_id, class_id):
    cur.execute(f'''DELETE FROM classes_properties
    WHERE class_id = {class_id} and property_id IN ({','.join(map(str, list_of_id))});''')


def add_relevant_values_for_class(conn, class_id, property_id, from_data, to_data):
    cur = conn.cursor()
    cur.execute(f'''UPDATE classes_properties
SET min_value = {from_data}, max_value = {to_data}
WHERE class_id={class_id} AND property_id={property_id}''')
    conn.commit()


def get_minmax_value(conn, property_id):
    df = pd.read_sql(f'''SELECT min_value, max_value
FROM properties WHERE property_id = {property_id};''', conn)
    for index, item in df.iterrows():
        min_value = None if item['min_value'] is None else float(item['min_value'])
        max_value = None if item['max_value'] is None else float(item['max_value'])
        return min_value, max_value


def get_classes_properties(conn):
    df = pd.read_sql(f'''SELECT class_name, property_name, classes_properties.min_value, classes_properties.max_value
    FROM classes_properties 
    JOIN properties USING (property_id) JOIN classes USING (class_id);''', conn)
    print(df)
    return df
