import os

from flask import current_app


def sql_file_to_list(filename):
    contents = ''
    with open(os.path.join(current_app.root_path, filename), mode='r', encoding='utf-8') as f:
        for line in f:
            contents += line.strip()

    sql_list = contents.split(';')[:-1]
    for sql in sql_list:
        sql += ';'

    return sql_list
