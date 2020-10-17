from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from flask_login import current_user
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from .auth import check_permission

from jiaowu import validators

from jiaowu.db_base import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/', methods=('GET',))
@check_permission('Admin', False)
def index():
    return redirect(url_for('admin.info_stu'))


@bp.route('/info_stu', methods=('GET', 'POST'))
@check_permission('Admin', False)
def info_stu():
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
            return redirect(url_for('admin.info_stu'))
        sql = 'select sno, sname, ssex, sid, sgrade, sdept, stel, smail' \
              ' from student where {} order by sno'.format(str_select[:-4])
        cursor.execute(sql)
    else:
        cursor.execute(
            'select sno, sname, ssex, sid, sgrade, sdept, stel, smail'
            ' from student'
            ' order by sno'
        )
    students = cursor.fetchall()
    cursor.close()
    return render_template('admin/info_stu.html', students=students)


@bp.route('/create_stu', methods=('GET', 'POST'))
@check_permission('Admin', False)
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

            db = get_db()
            cursor = db.cursor()
            cursor.callproc('create_student',
                            (sno, generate_password_hash(spwd), sname, ssex, sid, sgrade, sdept, stel, smail))
            db.commit()
            cursor.close()
            flash('创建成功！')
        except validators.ValidateException as e:
            flash(e.info)

        return redirect(url_for('admin.create_stu'))

    return render_template('admin/create_stu.html')


@bp.route('/update_stu/<sno>', methods=('GET', 'POST'))
@check_permission('Admin', False)
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

            cursor.callproc('update_student', (sno, sname, ssex, sid, sgrade, sdept, stel, smail))

            if len(spwd) > 0:
                cursor.callproc('update_student_pwd', (sno, generate_password_hash(spwd)))

            db.commit()
            cursor.close()
            flash('修改成功！')
        except validators.ValidateException as e:
            flash(e.info)

        return redirect(url_for('admin.update_stu', sno=sno))
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
        return render_template('admin/update_stu.html', student=student)


@bp.route('/delete_stu/<sno>', methods=('GET',))
@check_permission('Admin', False)
def delete_stu(sno):
    db = get_db()
    cursor = db.cursor()
    cursor.callproc('delete_student', (sno,))
    db.commit()
    cursor.close()
    flash('删除成功！')
    return redirect(url_for('admin.info_stu'))


@bp.route('/info_course', methods=('GET', 'POST'))
@check_permission('Admin', False)
def info_course():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        str_select = ''
        for key in request.form.keys():
            value = request.form[key]
            if key == 'cno':
                if len(value) > 0:
                    if not str.isdigit(value):
                        flash('课程号只能为数字！')
                        return redirect(url_for('admin.info_course'))
                    str_select += key + '=' + value + ' and '
            else:
                if type(value) == str:
                    if len(value) > 0:
                        str_select += key + ' LIKE \'%' + value + '%\' and '
                else:
                    abort(500)
        if len(str_select) == 0:
            return redirect(url_for('admin.info_course'))
        sql = 'select *' \
              ' from course where {} order by cno'.format(str_select[:-4])
        cursor.execute(sql)
    else:
        cursor.execute(
            'select *'
            ' from course'
            ' order by cno'
        )
    courses = cursor.fetchall()
    cursor.close()
    return render_template('admin/info_course.html', courses=courses)


@bp.route('/create_course', methods=('GET', 'POST'))
@check_permission('Admin', False)
def create_course():
    if request.method == 'POST':
        cname = request.form['cname']
        ctype = request.form['ctype']
        ccredit = request.form['ccredit']
        cdept = request.form['cdept']
        ccap = request.form['ccap']

        try:
            validators.Course.cname(cname)
            validators.Course.ctype(ctype)
            validators.Course.ccredit(ccredit)
            validators.Course.cdept(cdept)
            validators.Course.ccap(ccap)

            db = get_db()
            cursor = db.cursor()
            cursor.callproc('create_course', (cname, ctype, ccredit, cdept, ccap))
            db.commit()
            cursor.close()
            flash('创建成功！')

        except validators.ValidateException as e:
            flash(e.info)

        return redirect(url_for('admin.create_course'))

    return render_template('admin/create_course.html')


@bp.route('/update_course/<int:cno>', methods=('GET', 'POST'))
@check_permission('Admin', False)
def update_course(cno):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        cname = request.form['cname']
        ctype = request.form['ctype']
        ccredit = request.form['ccredit']
        cdept = request.form['cdept']
        ccap = request.form['ccap']

        try:
            validators.Course.cname(cname)
            validators.Course.ctype(ctype)
            validators.Course.ccredit(ccredit)
            validators.Course.cdept(cdept)
            validators.Course.ccap(ccap)

            cursor.callproc('update_course', (cno, cname, ctype, ccredit, cdept, ccap))
            db.commit()
            cursor.close()
            flash('修改成功！')

        except validators.ValidateException as e:
            flash(e.info)

        return redirect(url_for('admin.update_course', cno=cno))
    else:
        cursor.execute(
            'select *'
            ' from course'
            ' where cno = %s',
            (cno,)
        )
        course = cursor.fetchone()
        cursor.close()
        if course is None:
            abort(404)
        return render_template('admin/update_course.html', course=course)


@bp.route('/delete_course/<int:cno>', methods=('GET',))
@check_permission('Admin', False)
def delete_course(cno):
    db = get_db()
    cursor = db.cursor()
    cursor.callproc('delete_course', (cno,))
    db.commit()
    cursor.close()
    flash('删除成功！')
    return redirect(url_for('admin.info_course'))


@bp.route('/info_admin', methods=('GET', 'POST'))
@check_permission('Admin', False)
def info_admin():
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
            return redirect(url_for('admin.info_admin'))
        sql = 'select ano, aname, atel, amail' \
              ' from admin where {} order by ano'.format(str_select[:-4])
        cursor.execute(sql)
    else:
        cursor.execute(
            'select ano, aname, atel, amail'
            ' from admin'
            ' order by ano'
        )
    admins = cursor.fetchall()
    cursor.close()
    return render_template('admin/info_admin.html', admins=admins)


@bp.route('/create_admin', methods=('GET', 'POST'))
@check_permission('Admin', False)
def create_admin():
    if request.method == 'POST':
        ano = request.form['ano']
        apwd = request.form['apwd']
        aname = request.form['aname']
        atel = request.form['atel']
        amail = request.form['amail']

        try:
            validators.Admin.ano(ano)
            validators.Admin.apwd(apwd)
            validators.Admin.aname(aname)
            validators.Admin.atel(atel)
            validators.Admin.amail(amail)

            db = get_db()
            cursor = db.cursor()
            cursor.callproc('create_admin', (ano, generate_password_hash(apwd), aname, atel, amail))
            db.commit()
            cursor.close()
            flash('创建成功！')

        except validators.ValidateException as e:
            flash(e.info)

        return redirect(url_for('admin.create_admin'))

    return render_template('admin/create_admin.html')


@bp.route('/update_admin/<ano>', methods=('GET', 'POST'))
@check_permission('Admin', False)
def update_admin(ano):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        apwd = request.form['apwd']
        aname = request.form['aname']
        atel = request.form['atel']
        amail = request.form['amail']

        try:
            validators.Admin.aname(aname)
            validators.Admin.apwd(apwd, True)
            validators.Admin.atel(atel)
            validators.Admin.amail(amail)

            cursor.callproc('update_admin', (ano, aname, atel, amail))

            if len(apwd) > 0:
                cursor.callproc('update_admin_pwd', (ano, generate_password_hash(apwd)))

            db.commit()
            cursor.close()
            flash('修改成功！')

        except validators.ValidateException as e:
            flash(e.info)

        return redirect(url_for('admin.update_admin', ano=ano))

    else:
        cursor.execute(
            'select ano, aname, atel, amail'
            ' from admin'
            ' where ano = %s',
            (ano,)
        )
        admin = cursor.fetchone()
        cursor.close()
        if admin is None:
            abort(404)
        return render_template('admin/update_admin.html', admin=admin)


@bp.route('/delete_admin/<ano>', methods=('GET',))
@check_permission('Admin', False)
def delete_admin(ano):
    if current_user.no == ano:
        flash('不能删除当前用户！')
        return redirect(url_for('admin.info_admin'))
    db = get_db()
    cursor = db.cursor()
    cursor.callproc('delete_admin', (ano,))
    db.commit()
    cursor.close()
    flash('删除成功！')
    return redirect(url_for('admin.info_admin'))
