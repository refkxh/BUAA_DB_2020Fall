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
    return redirect(url_for('student.update_stu', sno=current_user.no))


@bp.route('/update_stu/<sno>', methods=('GET', 'POST'))
@check_permission('Student', True)
def update_stu(sno):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        spwd = request.form['spwd']
        sname = request.form['sname']
        ssex = request.form['ssex']
        sid = request.form['sid']
        sgrade = request.form['sgrade']
        sdept = request.form['sdept']
        stel = request.form['stel']
        smail = request.form['smail']

        try:
            validators.Student.sname(sname)
            validators.Student.spwd(spwd, True)
            validators.Student.ssex(ssex)
            validators.Student.sid(sid, cur_sno=sno)
            validators.Student.sgrade(sgrade)
            validators.Student.sdept(sdept)
            validators.Student.stel(stel)
            validators.Student.smail(smail)

            cursor.execute(
                'update student set sname = %s, ssex = %s, sid = %s,'
                ' sgrade = %s, sdept = %s, stel = %s, smail = %s'
                ' where sno = %s',
                (sname, ssex, sid, sgrade, sdept, stel, smail, sno)
            )

            if len(spwd) > 0:
                cursor.execute(
                    'update student set spwd = %s'
                    ' where sno = %s',
                    (generate_password_hash(spwd), sno)
                )

            db.commit()
            cursor.close()
            flash('修改成功！')
        except validators.ValidateException as e:
            flash(e.info)

        return redirect(url_for('student.update_stu', sno=sno))
    else:
        cursor.execute(
            'select sno, sname, ssex, sid, sgrade, sdept, stel, smail'
            ' from student'
            ' where sno = %s',
            (sno,)
        )
        student = cursor.fetchone()
        cursor.close()
        if student is None:
            abort(404)
        return render_template('student/update_stu.html', student=student)
