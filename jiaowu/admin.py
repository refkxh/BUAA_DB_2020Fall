from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from jiaowu import validators

from jiaowu.db_base import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/', methods=('GET',))
def index():
    return redirect(url_for('admin.info_stu'))


@bp.route('/info_stu', methods=('GET', 'POST'))
def info_stu():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        str_select = ''
        for key in request.form.keys():
            value = request.form[key]
            if type(value) == str:
                if len(value) > 0:
                    str_select += key + '=\'' + value + '\' and '
            else:
                return redirect(url_for('admin.info_stu'))
        if len(str_select) == 0:
            flash('查询条件不能为空！')
            return redirect(url_for('admin.info_stu'))
        sql = 'SELECT sno, sname, ssex, sid, sgrade, sdept, stel, smail'\
              ' FROM student WHERE {} ORDER BY sno'.format(str_select[:-4])
        cursor.execute(sql)
    else:
        cursor.execute(
            'SELECT sno, sname, ssex, sid, sgrade, sdept, stel, smail'
            ' FROM student'
            ' ORDER BY sno'
        )
    students = cursor.fetchall()
    cursor.close()
    return render_template('admin/info_stu.html', students=students)


@bp.route('/create_stu', methods=('GET', 'POST'))
def create_stu():
    if request.method == 'POST':
        sno = request.form['sno']
        spwd = request.form['spwd']
        sname = request.form['sname']
        ssex = request.form['ssex']
        sid = request.form['sid']
        sgrade = request.form['sgrade']
        sdept = request.form['sdept']
        stel = request.form['stel']
        smail = request.form['smail']

        valid = True

        try:
            validators.Student.sno(sno)
            validators.Student.spwd(spwd)
            validators.Student.sname(sname)
            validators.Student.ssex(ssex)
            validators.Student.sid(sid)
            validators.Student.sgrade(sgrade)
            validators.Student.sdept(sdept)
            validators.Student.stel(stel)
            validators.Student.smail(smail)
        except validators.ValidateException as e:
            valid = False
            flash(e.info)

        if valid:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO student (sno, spwd, sname, ssex, sid, sgrade, sdept, stel, smail)'
                ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (sno, generate_password_hash(spwd), sname, ssex, sid, sgrade, sdept, stel, smail)
            )
            db.commit()
            cursor.close()
            return redirect(url_for('admin.create_stu'))

    return render_template('admin/create_stu.html')


@bp.route('/update_stu/<int:sno>', methods=('GET', 'POST'))
def update_stu(sno):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        new_sno = request.form['sno']
        spwd = request.form['spwd']
        sname = request.form['sname']
        ssex = request.form['ssex']
        sid = request.form['sid']
        sgrade = request.form['sgrade']
        sdept = request.form['sdept']
        stel = request.form['stel']
        smail = request.form['smail']

        valid = True

        try:
            validators.Student.sno(new_sno)
            validators.Student.spwd(spwd)
            validators.Student.sname(sname)
            validators.Student.ssex(ssex)
            validators.Student.sid(sid)
            validators.Student.sgrade(sgrade)
            validators.Student.sdept(sdept)
            validators.Student.stel(stel)
            validators.Student.smail(smail)
        except validators.ValidateException as e:
            valid = False
            flash(e.info)

        if valid:
            cursor.execute(
                'UPDATE student SET sno = %s, spwd = %s, sname = %s, '
                ' ssex = %s, sid = %s, sgrade = %s, sdept = %s, stel = %s, smail = %s'
                ' WHERE sno = %s',
                (new_sno, generate_password_hash(spwd), sname, ssex, sid, sgrade, sdept, stel, smail, sno)
            )
            db.commit()
            cursor.close()
            return redirect(url_for('admin.update_stu', sno=sno))
    else:
        cursor.execute(
            'SELECT sno, sname, ssex, sid, sgrade, sdept, stel, smail'
            ' FROM student'
            ' WHERE sno = %s',
            (sno,)
        )
        student = cursor.fetchone()
        cursor.close()
        if student is None:
            abort(404)
        return render_template('admin/update_stu.html', student=student)


@bp.route('/delete_stu/<int:sno>', methods=('POST',))
def delete_stu(sno):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM student WHERE sno = %s', (sno,))
    db.commit()
    cursor.close()
    return redirect(url_for('admin.info_stu'))
