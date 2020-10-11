from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from .auth import check_permission

from jiaowu import validators

from jiaowu.db_base import get_db

bp = Blueprint('student', __name__, url_prefix='/student')


@bp.route('/<sno>', methods=('GET',))
@check_permission('Student', True)
def index(sno):
    return '还没做，莫着急。\nsno: {}'.format(sno)
