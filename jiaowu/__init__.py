import os

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    username = input('Please enter MySQL username: ')
    password = input('Please enter the password: ')
    db_name = input('Please enter the name of the MySQL database to be used: ')

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_USERNAME=username,
        DATABASE_PASSWORD=password,
        DATABASE_NAME=db_name,
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db_base
    db_base.init_app(app)

    from . import admin
    app.register_blueprint(admin.bp)

    # app.add_url_rule('/', endpoint='index')

    return app
