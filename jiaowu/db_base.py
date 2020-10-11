import mysql.connector

import click
from flask import current_app, g
from flask.cli import with_appcontext
from .sql_utils import sql_file_to_list

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

    for sql in sql_file_to_list('schema.sql'):
        cursor.execute(sql)

    cursor.execute(
        'insert into admin (ano, apwd, aname, atel, amail)'
        ' values (%s, %s, %s, %s, %s)',
        ('refkxh', generate_password_hash('admin'), '孔祥浩', '12345678901', 'refkxh@outlook.com')
    )

    cursor.execute(
        'insert into admin (ano, apwd, aname, atel, amail)'
        ' values (%s, %s, %s, %s, %s)',
        ('apartment', generate_password_hash('admin'), '龚毓', '8888110', 'g94837848@gmail.com')
    )

    cursor.execute(
        'insert into admin (ano, apwd, aname, atel, amail)'
        ' values (%s, %s, %s, %s, %s)',
        ('lzy', generate_password_hash('admin'), '刘紫阳', '88885678', '')
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
