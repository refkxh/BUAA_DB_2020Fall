from flask import current_app


def sql_file_to_list(filename):
    contents = ''
    with current_app.open_resource(filename, mode='r') as f:
        for line in f:
            contents += line.strip()

    sql_list = contents.split(';')[:-1]
    for sql in sql_list:
        sql += ';'

    return sql_list
