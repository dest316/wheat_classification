import pandas as pd


def get_properties(conn):
    df = pd.read_sql(f'''
    SELECT property_name, property_type, property_id
     FROM properties JOIN property_types USING (property_type_id);
''', conn)
    return df


def get_classes(conn):
    df = pd.read_sql(f'''
    SELECT * FROM classes;''', conn)
    return df


def get_properties_by_class(conn, class_id):
    df = pd.read_sql(f'''
    SELECT property_name, property_id, class_id, classes_properties.min_value, classes_properties.max_value
    FROM classes_properties JOIN properties USING (property_id)
    WHERE class_id = {class_id};''', conn)
    return df


def check_completeness(conn):
    result = pd.read_sql(f'''
SELECT * FROM classes_properties''', conn).isnull().any().any()
    return not result
