from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from flask_login import current_user

from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from .auth import check_permission

from jiaowu import validators

from jiaowu.db_base import get_db

bp = Blueprint('student', __name__, url_prefix='/student')


@bp.route('/', methods=('GET',))
@check_permission('Student', False)
def index():
    return '还没做，莫着急。<br/>sno: {}'.format(current_user.no)
