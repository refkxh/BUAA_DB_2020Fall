import mysql.connector

import click
from flask import current_app, g
from flask.cli import with_appcontext
from .sql_utils import simple_sql_file_to_list, create_procedures, drop_procedures

from werkzeug.security import generate_password_hash


def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host='localhost',
                user=current_app.config['DATABASE_USERNAME'],
                password=current_app.config['DATABASE_PASSWORD'],
                database=current_app.config['DATABASE_NAME'],
                charset='utf8mb4'
            )
        except:
            raise Exception('Database connection failed.')

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    cursor = db.cursor()

    for sql in simple_sql_file_to_list('schema.sql'):
        cursor.execute(sql)

    for procedure in drop_procedures:
        cursor.execute(procedure)

    for procedure in create_procedures:
        cursor.execute(procedure)

    cursor.executemany(
        'insert into admin (ano, apwd, aname, atel, amail)'
        ' values (%s, %s, %s, %s, %s)',
        [('refkxh', generate_password_hash('admin123'), '孔祥浩', '12345678901', 'refkxh@outlook.com'),
         ('apartment', generate_password_hash('admin123'), '龚毓', '12345678902', 'g94837848@gmail.com'),
         ('lzy', generate_password_hash('admin123'), '刘紫阳', '12345678903', 'a@b.c')]
    )

    db.commit()
    cursor.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Database initialized.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
