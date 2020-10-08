from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin

from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from jiaowu import validators

from jiaowu.db_base import get_db

from functools import wraps

bp = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = '您还未登录。'


class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    pass
    # return User.get(user_id)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            flash('您已登录。')
            return redirect(url_for('index'))
        return render_template('auth/login.html')
    # try:
    #     user = User(request.form['utype'], request.form['uno'])
    #     assert user.validate_pwd(request.form['upwd'])
    #     login_user(user)
    #     flash('登录成功')
    #     return redirect(url_for('index'))
    # except:
    #     flash('登录失败')
    #     return redirect(url_for('login'))


@bp.route('/logout', methods=('GET',))
@login_required
def logout():
    logout_user()
    flash('登出成功！')
    return redirect(url_for('auth.login'))
