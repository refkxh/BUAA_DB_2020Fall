from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin

from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from jiaowu import validators

from jiaowu.db_base import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

