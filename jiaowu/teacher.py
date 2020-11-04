from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from flask_login import current_user

from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from .auth import check_permission

from jiaowu import validators

from jiaowu.db_base import get_db

bp = Blueprint('teacher', __name__, url_prefix='/teacher')


@bp.route('/', methods=('GET',))
@check_permission('Teacher', False)
def index():
    return redirect(url_for('teacher.update_teacher'))


@bp.route('/update_teacher', methods=('GET', 'POST'))
@check_permission('Teacher', False)
def update_teacher():
    pass
