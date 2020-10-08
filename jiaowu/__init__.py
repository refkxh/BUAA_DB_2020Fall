import os

from flask import Flask, render_template


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

    from . import auth
    app.register_blueprint(auth.bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', code=404)

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', code=500)

    app.add_url_rule('/', endpoint='admin.index')

    return app
