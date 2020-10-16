from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin

from werkzeug.security import check_password_hash

from jiaowu.db_base import get_db

from functools import wraps

bp = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = '您还未登录。'


class User(UserMixin):
    __char2identity = {'S': 'Student', 'A': 'Admin'}

    def __init__(self, identity, no):
        if identity in self.__char2identity:
            self.identity = self.__char2identity[identity]
        else:
            self.identity = None
        assert isinstance(no, str)
        self.no = no
        self.id = identity + no
        if self.identity == 'Student':
            str_no, str_name = 'sno', 'sname'
        elif self.identity == 'Admin':
            str_no, str_name = 'ano', 'aname'
        else:
            assert False
        sql = 'select {} from {} where {} = {}'.format(
            str_name, self.identity, str_no, '\'' + self.no + '\'')
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql)
        self.name = cursor.fetchone()[str_name]
        cursor.close()

    def validate_pwd(self, pwd):
        if self.identity == 'Student':
            str_no, str_pwd = 'sno', 'spwd'
        elif self.identity == 'Admin':
            str_no, str_pwd = 'ano', 'apwd'
        else:
            return False
        sql = 'select {} from {} where {} = {}'.format(
            str_pwd, self.identity, str_no, '\'' + self.no + '\'')
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(sql)
        pwd_dict = cursor.fetchone()
        cursor.close()
        if pwd_dict is None:
            return False
        return check_password_hash(pwd_dict[str_pwd], pwd)


def check_permission(identity, need_certain):
    def auth_decorator(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('您还未登录。')
                return redirect(url_for('index'))
            try:
                assert current_user.identity == identity
                if need_certain:
                    if identity == 'Student':
                        assert kwargs['sno'] == current_user.no
                    elif identity == 'Admin':
                        assert kwargs['ano'] == current_user.no
            except AssertionError:
                flash('您的权限不匹配。')
                return redirect(url_for('index'))
            return func(*args, **kwargs)

        return wrapped_func

    return auth_decorator


@login_manager.user_loader
def load_user(user_id):
    try:
        return User(user_id[0], user_id[1:])
    except:
        return None


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            flash('您已登录。')
            return redirect(url_for('index'))
        return render_template('auth/login.html')
    try:
        user = User(request.form['identity'], request.form['id'])
        assert user.validate_pwd(request.form['pwd'])
        login_user(user)
        return redirect(url_for('index'))
    except:
        flash('学工号或密码错误!')
        return redirect(url_for('auth.login'))


@bp.route('/logout', methods=('GET',))
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
