import os

from flask import Flask, redirect, render_template, url_for
from flask_login import current_user

from werkzeug.exceptions import abort


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    username = input('Please enter MySQL username: ')
    password = input('Please enter the password: ')
    db_name = 'jiaowu'

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

    @app.errorhandler(400)
    def bad_request(e):
        return render_template('error.html', code=400)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', code=404)

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', code=500)

    from . import auth
    auth.login_manager.init_app(app)
    app.register_blueprint(auth.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import student
    app.register_blueprint(student.bp)

    from . import teacher
    app.register_blueprint(teacher.bp)

    @app.route('/', methods=('GET',))
    def index():
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        elif current_user.identity == 'Admin':
            return redirect(url_for('admin.index'))
        elif current_user.identity == 'Student':
            return redirect(url_for('student.index'))
        elif current_user.identity == 'Teacher':
            return redirect(url_for('teacher.index'))
        else:
            abort(500)

    return app
