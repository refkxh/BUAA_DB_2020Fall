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
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        tpwd = request.form['tpwd']
        tname = request.form['tname']
        tsex = request.form['tsex']
        ttitle = request.form['ttitle']
        tdept = request.form['tdept']
        ttel = request.form['ttel']
        tmail = request.form['tmail']

        try:
            validators.Teacher.tpwd(tpwd, True)
            validators.Teacher.tname(tname)
            validators.Teacher.tsex(tsex)
            validators.Teacher.ttitle(ttitle)
            validators.Teacher.tdept(tdept)
            validators.Teacher.ttel(ttel)
            validators.Teacher.tmail(tmail)

            cursor.callproc('update_teacher', (current_user.no, tname, tsex, ttitle, tdept, ttel, tmail))

            if len(tpwd) > 0:
                cursor.callproc('update_teacher_pwd', (current_user.no, generate_password_hash(tpwd)))

            db.commit()
            cursor.close()
            flash('修改成功！')
        except validators.ValidateException as e:
            flash(e.info)

        return redirect(url_for('teacher.update_teacher', tno=current_user.no))
    else:
        cursor.execute(
            'select tno, tname, tsex, ttitle, tdept, ttel, tmail'
            ' from teacher'
            ' where tno = %s',
            (current_user.no,)
        )
        teacher = cursor.fetchone()
        cursor.close()
        if teacher is None:
            abort(404)
        return render_template('teacher/update_teacher.html', teacher=teacher)


@bp.route('/info_textbook', methods=('GET', 'POST'))
@check_permission('Teacher', False)
def info_textbook():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        str_select = ''
        for key in request.form.keys():
            value = request.form[key]
            if type(value) == str:
                if len(value) > 0:
                    str_select += key + ' LIKE \'%' + value + '%\' and '
            else:
                abort(500)
        if len(str_select) == 0:
            return redirect(url_for('teacher.info_textbook'))
        sql = 'select *' \
              ' from textbook where {} order by bno'.format(str_select[:-4])
        cursor.execute(sql)
    else:
        cursor.execute(
            'select *'
            ' from textbook'
            ' order by bno'
        )
    textbooks = cursor.fetchall()
    cursor.close()
    return render_template('teacher/info_textbook.html', textbooks=textbooks)


@bp.route('/create_textbook', methods=('GET', 'POST'))
@check_permission('Teacher', False)
def create_textbook():
    if request.method == 'POST':
        bno = request.form['bno']
        bname = request.form['bname']
        bauthor = request.form['bauthor']
        bpress = request.form['bpress']

        try:
            validators.Textbook.bno(bno)
            validators.Textbook.bname(bname)
            validators.Textbook.bauthor(bauthor)
            validators.Textbook.bpress(bpress)

            db = get_db()
            cursor = db.cursor()
            cursor.callproc('create_textbook', (bno, bname, bauthor, bpress))
            db.commit()
            cursor.close()
            flash('创建成功！')

        except validators.ValidateException as e:
            flash(e.info)

        return redirect(url_for('teacher.create_textbook'))

    return render_template('teacher/create_textbook.html')


@bp.route('/update_textbook/<bno>', methods=('GET', 'POST'))
@check_permission('Teacher', False)
def update_textbook(bno):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        bname = request.form['bname']
        bauthor = request.form['bauthor']
        bpress = request.form['bpress']

        try:
            validators.Textbook.bname(bname)
            validators.Textbook.bauthor(bauthor)
            validators.Textbook.bpress(bpress)

            cursor.callproc('update_textbook', (bno, bname, bauthor, bpress))
            db.commit()
            cursor.close()
            flash('修改成功！')

        except validators.ValidateException as e:
            flash(e.info)

        return redirect(url_for('teacher.update_textbook', bno=bno))
    else:
        cursor.execute(
            'select *'
            ' from textbook'
            ' where bno = %s',
            (bno,)
        )
        textbook = cursor.fetchone()
        cursor.close()
        if textbook is None:
            abort(404)
        return render_template('teacher/update_textbook.html', textbook=textbook)


@bp.route('/delete_textbook/<bno>', methods=('GET',))
@check_permission('Teacher', False)
def delete_textbook(bno):
    db = get_db()
    cursor = db.cursor()
    cursor.callproc('delete_textbook', (bno,))
    db.commit()
    cursor.close()
    flash('删除成功！')
    return redirect(url_for('teacher.info_textbook'))


@bp.route('/list_untaught_courses', methods=('GET',))
@check_permission('Teacher', False)
def list_untaught_courses():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select * from course where cno not in '
                   '(select cno from teacher_course where tno = %s) '
                   'order by cno', (current_user.no,))
    courses = cursor.fetchall()
    cursor.close()
    return render_template('teacher/list_untaught_courses.html', courses=courses)


@bp.route('/teach_course/<int:cno>', methods=('GET',))
@check_permission('Teacher', False)
def teach_course(cno):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select * from teacher_course where tno = %s and cno = %s', (current_user.no, cno))
    if cursor.fetchone() is not None:
        flash('您已教授该课程！')
    else:
        cursor.callproc('teach_course', (current_user.no, cno))
        flash('授课成功！')
    db.commit()
    cursor.close()
    return redirect(url_for('teacher.list_untaught_courses'))


@bp.route('/list_taught_courses', methods=('GET',))
@check_permission('Teacher', False)
def list_taught_courses():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select * from course where cno in '
                   '(select cno from teacher_course where tno = %s) '
                   'order by cno', (current_user.no,))
    courses = cursor.fetchall()
    cursor.close()
    return render_template('teacher/list_taught_courses.html', courses=courses)


@bp.route('/unteach_course/<int:cno>', methods=('GET',))
@check_permission('Teacher', False)
def unteach_course(cno):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select * from teacher_course where tno = %s and cno = %s', (current_user.no, cno))
    item = cursor.fetchone()
    if item is None:
        flash('您并未教授该课程！')
    else:
        cursor.callproc('unteach_course', (current_user.no, cno))
        flash('取消教授课程成功！')
    db.commit()
    cursor.close()
    return redirect(url_for('teacher.list_taught_courses'))
