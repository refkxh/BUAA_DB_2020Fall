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
        cursor.execute('select * from course order by cno')
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
        cursor.execute('select * from course where cno = %s', (cno,))
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


@bp.route('/info_teacher', methods=('GET', 'POST'))
@check_permission('Admin', False)
def info_teacher():
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
            return redirect(url_for('admin.info_teacher'))
        sql = 'select tno, tname, tsex, ttitle, tdept, ttel, tmail' \
              ' from teacher where {} order by tno'.format(str_select[:-4])
        cursor.execute(sql)
    else:
        cursor.execute(
            'select tno, tname, tsex, ttitle, tdept, ttel, tmail'
            ' from teacher'
            ' order by tno'
        )
    teachers = cursor.fetchall()
    cursor.close()
    return render_template('admin/info_teacher.html', teachers=teachers)


@bp.route('/create_teacher', methods=('GET', 'POST'))
@check_permission('Admin', False)
def create_teacher():
    if request.method == 'POST':
        tno = request.form['tno']
        tpwd = request.form['tpwd']
        tname = request.form['tname']
        tsex = request.form['tsex']
        ttitle = request.form['ttitle']
        tdept = request.form['tdept']
        ttel = request.form['ttel']
        tmail = request.form['tmail']

        try:
            validators.Teacher.tno(tno)
            validators.Teacher.tpwd(tpwd, True)
            validators.Teacher.tname(tname)
            validators.Teacher.tsex(tsex)
            validators.Teacher.ttitle(ttitle)
            validators.Teacher.tdept(tdept)
            validators.Teacher.ttel(ttel)
            validators.Teacher.tmail(tmail)

            db = get_db()
            cursor = db.cursor()
            cursor.callproc('create_teacher',
                            (tno, generate_password_hash(tpwd), tname, tsex, ttitle, tdept, ttel, tmail))
            db.commit()
            cursor.close()
            flash('创建成功！')
        except validators.ValidateException as e:
            flash(e.info)

        return redirect(url_for('admin.create_teacher'))

    return render_template('admin/create_teacher.html')


@bp.route('/update_teacher/<tno>', methods=('GET', 'POST'))
@check_permission('Admin', False)
def update_teacher(tno):
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

            cursor.callproc('update_teacher', (tno, tname, tsex, ttitle, tdept, ttel, tmail))

            if len(tpwd) > 0:
                cursor.callproc('update_teacher_pwd', (tno, generate_password_hash(tpwd)))

            db.commit()
            cursor.close()
            flash('修改成功！')
        except validators.ValidateException as e:
            flash(e.info)

        return redirect(url_for('admin.update_teacher', tno=tno))
    else:
        cursor.execute(
            'select tno, tname, tsex, ttitle, tdept, ttel, tmail'
            ' from teacher'
            ' where tno = %s',
            (tno,)
        )
        teacher = cursor.fetchone()
        cursor.close()
        if teacher is None:
            abort(404)
        return render_template('admin/update_teacher.html', teacher=teacher)


@bp.route('/delete_teacher/<tno>', methods=('GET',))
@check_permission('Admin', False)
def delete_teacher(tno):
    db = get_db()
    cursor = db.cursor()
    cursor.callproc('delete_teacher', (tno,))
    db.commit()
    cursor.close()
    flash('删除成功！')
    return redirect(url_for('admin.info_teacher'))


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


@bp.route('/info_textbook', methods=('GET', 'POST'))
@check_permission('Admin', False)
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
            return redirect(url_for('admin.info_textbook'))
        sql = 'select *' \
              ' from textbook where {} order by bno'.format(str_select[:-4])
        cursor.execute(sql)
    else:
        cursor.execute('select * from textbook order by bno')
    textbooks = cursor.fetchall()
    cursor.close()
    return render_template('admin/info_textbook.html', textbooks=textbooks)


@bp.route('/create_textbook', methods=('GET', 'POST'))
@check_permission('Admin', False)
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

        return redirect(url_for('admin.create_textbook'))

    return render_template('admin/create_textbook.html')


@bp.route('/update_textbook/<bno>', methods=('GET', 'POST'))
@check_permission('Admin', False)
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

        return redirect(url_for('admin.update_textbook', bno=bno))
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
        return render_template('admin/update_textbook.html', textbook=textbook)


@bp.route('/delete_textbook/<bno>', methods=('GET',))
@check_permission('Admin', False)
def delete_textbook(bno):
    db = get_db()
    cursor = db.cursor()
    cursor.callproc('delete_textbook', (bno,))
    db.commit()
    cursor.close()
    flash('删除成功！')
    return redirect(url_for('admin.info_textbook'))


@bp.route('/info_room', methods=('GET', 'POST'))
@check_permission('Admin', False)
def info_room():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        str_select = ''
        for key in request.form.keys():
            value = request.form[key]
            if key == 'rno':
                if len(value) > 0:
                    if not str.isdigit(value):
                        flash('教室号只能为数字！')
                        return redirect(url_for('admin.info_room'))
                    str_select += key + '=' + value + ' and '
            else:
                if type(value) == str:
                    if len(value) > 0:
                        str_select += key + ' LIKE \'%' + value + '%\' and '
                else:
                    abort(500)
        if len(str_select) == 0:
            return redirect(url_for('admin.info_room'))
        sql = 'select *' \
              ' from room where {} order by rno'.format(str_select[:-4])
        cursor.execute(sql)
    else:
        cursor.execute('select * from room order by rno')
    rooms = cursor.fetchall()
    cursor.close()
    return render_template('admin/info_room.html', rooms=rooms)


@bp.route('/create_room', methods=('GET', 'POST'))
@check_permission('Admin', False)
def create_room():
    if request.method == 'POST':
        rname = request.form['rname']
        rcap = request.form['rcap']

        try:
            validators.Room.rname(rname)
            validators.Room.rcap(rcap)

            db = get_db()
            cursor = db.cursor()
            cursor.callproc('create_room', (rname, rcap))
            db.commit()
            cursor.close()
            flash('创建成功！')

        except validators.ValidateException as e:
            flash(e.info)

        return redirect(url_for('admin.create_room'))

    return render_template('admin/create_room.html')


@bp.route('/update_room/<int:rno>', methods=('GET', 'POST'))
@check_permission('Admin', False)
def update_room(rno):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        rname = request.form['rname']
        rcap = request.form['rcap']

        try:
            validators.Room.rname(rname)
            validators.Room.rcap(rcap)

            cursor.callproc('update_room', (rno, rname, rcap))
            db.commit()
            cursor.close()
            flash('修改成功！')

        except validators.ValidateException as e:
            flash(e.info)

        return redirect(url_for('admin.update_room', rno=rno))
    else:
        cursor.execute(
            'select *'
            ' from room'
            ' where rno = %s',
            (rno,)
        )
        room = cursor.fetchone()
        cursor.close()
        if room is None:
            abort(404)
        return render_template('admin/update_room.html', room=room)


@bp.route('/delete_room/<int:rno>', methods=('GET',))
@check_permission('Admin', False)
def delete_room(rno):
    db = get_db()
    cursor = db.cursor()
    cursor.callproc('delete_room', (rno,))
    db.commit()
    cursor.close()
    flash('删除成功！')
    return redirect(url_for('admin.info_room'))


@bp.route('/course_to_stu/<int:cno>', methods=('GET',))
@check_permission('Admin', False)
def course_to_stu(cno):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select student.sno sno, sname, ssex, sid, sgrade, sdept, stel, smail, score '
                   'from student, student_course '
                   'where student.sno = student_course.sno and cno = %s '
                   'order by sno', (cno,))
    students = cursor.fetchall()
    cursor.execute('select cno, cname from course where cno = %s', (cno,))
    course = cursor.fetchone()
    cursor.close()
    return render_template('admin/course_to_stu.html', students=students, course=course)


@bp.route('/stu_to_course/<sno>', methods=('GET',))
@check_permission('Admin', False)
def stu_to_course(sno):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select course.cno cno, cname, ctype, ccredit, cdept, ccap, cselect, score '
                   'from course, student_course '
                   'where course.cno = student_course.cno and sno = %s '
                   'order by cno', (sno,))
    courses = cursor.fetchall()
    cursor.execute('select sno, sname from student where sno = %s', (sno,))
    student = cursor.fetchone()
    cursor.close()
    return render_template('admin/stu_to_course.html', courses=courses, student=student)


@bp.route('/select_course', methods=('POST',))
@check_permission('Admin', False)
def select_course():
    sno = request.form['sno']
    cno = request.form['cno']
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select * from student_course where sno = %s and cno = %s', (sno, cno))
    if cursor.fetchone() is not None:
        flash('该学生已选修过该课程！')
    else:
        cursor.execute('select * from student where sno = %s', (sno,))
        if cursor.fetchone() is None:
            flash('不存在该学生！')
        else:
            cursor.execute('select ccap, cselect from course where cno = %s', (cno,))
            item = cursor.fetchone()
            if item is None:
                flash('不存在该课程！')
            elif item['cselect'] >= item['ccap']:
                flash('课程容量已满！')
            else:
                cursor.callproc('select_course', (sno, cno))
                db.commit()
                flash('选课成功！')
    cursor.close()
    return redirect(request.referrer or url_for('index'))


@bp.route('/unselect_course', methods=('POST',))
@check_permission('Admin', False)
def unselect_course():
    sno = request.form['sno']
    cno = request.form['cno']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('select * from student_course where sno = %s and cno = %s', (sno, cno))
    if cursor.fetchone() is None:
        flash('该学生并未选修过该课程！')
    else:
        cursor.callproc('unselect_course', (sno, cno))
        db.commit()
        flash('退课成功！')
    cursor.close()
    return redirect(request.referrer or url_for('index'))


@bp.route('/modify_score', methods=('POST',))
@check_permission('Admin', False)
def modify_score():
    sno = request.form['sno']
    cno = request.form['cno']
    score = request.form['score']
    if len(score) > 0 and (not str.isdigit(score) or not(0 <= int(score) <= 100)):
        flash('成绩非法！')
    else:
        if len(score) == 0:
            score = None
        db = get_db()
        cursor = db.cursor()
        cursor.execute('select * from student_course where sno = %s and cno = %s', (sno, cno))
        if cursor.fetchone() is None:
            flash('该学生并未选修过该课程！')
        else:
            cursor.callproc('update_score', (sno, cno, score))
            db.commit()
            flash('成绩修改成功！')
        cursor.close()
    return redirect(request.referrer or url_for('index'))


@bp.route('/course_to_teacher/<int:cno>', methods=('GET',))
@check_permission('Admin', False)
def course_to_teacher(cno):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select teacher.tno tno, tname, tsex, ttitle, tdept, ttel, tmail '
                   'from teacher, teacher_course '
                   'where teacher.tno = teacher_course.tno and cno = %s '
                   'order by tno', (cno,))
    teachers = cursor.fetchall()
    cursor.execute('select cno, cname from course where cno = %s', (cno,))
    course = cursor.fetchone()
    cursor.close()
    return render_template('admin/course_to_teacher.html', teachers=teachers, course=course)


@bp.route('/teacher_to_course/<tno>', methods=('GET',))
@check_permission('Admin', False)
def teacher_to_course(tno):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select course.cno cno, cname, ctype, ccredit, cdept, ccap, cselect '
                   'from course, teacher_course '
                   'where course.cno = teacher_course.cno and tno = %s '
                   'order by cno', (tno,))
    courses = cursor.fetchall()
    cursor.execute('select tno, tname from teacher where tno = %s', (tno,))
    teacher = cursor.fetchone()
    cursor.close()
    return render_template('admin/teacher_to_course.html', courses=courses, teacher=teacher)


@bp.route('/teach_course', methods=('POST',))
@check_permission('Admin', False)
def teach_course():
    tno = request.form['tno']
    cno = request.form['cno']
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select * from teacher_course where tno = %s and cno = %s', (tno, cno))
    if cursor.fetchone() is not None:
        flash('该老师已教授该课程！')
    else:
        cursor.execute('select * from teacher where tno = %s', (tno,))
        if cursor.fetchone() is None:
            flash('不存在该老师！')
        else:
            cursor.execute('select * from course where cno = %s', (cno,))
            if cursor.fetchone() is None:
                flash('不存在该课程！')
            else:
                cursor.callproc('teach_course', (tno, cno))
                db.commit()
                flash('授课关系设置成功！')
    cursor.close()
    return redirect(request.referrer or url_for('index'))


@bp.route('/unteach_course', methods=('POST',))
@check_permission('Admin', False)
def unteach_course():
    tno = request.form['tno']
    cno = request.form['cno']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('select * from teacher_course where tno = %s and cno = %s', (tno, cno))
    if cursor.fetchone() is None:
        flash('该老师并未教授该课程！')
    else:
        cursor.callproc('unteach_course', (tno, cno))
        db.commit()
        flash('取消教授课程成功！')
    cursor.close()
    return redirect(request.referrer or url_for('index'))


@bp.route('/course_to_textbook/<int:cno>', methods=('GET',))
@check_permission('Admin', False)
def course_to_textbook(cno):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select textbook.bno bno, bname, bauthor, bpress '
                   'from textbook, textbook_course '
                   'where textbook.bno = textbook_course.bno and cno = %s '
                   'order by bno', (cno,))
    textbooks = cursor.fetchall()
    cursor.execute('select cno, cname from course where cno = %s', (cno,))
    course = cursor.fetchone()
    cursor.close()
    return render_template('admin/course_to_textbook.html', textbooks=textbooks, course=course)


@bp.route('/textbook_to_course/<bno>', methods=('GET',))
@check_permission('Admin', False)
def textbook_to_course(bno):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select course.cno cno, cname, ctype, ccredit, cdept, ccap, cselect '
                   'from course, textbook_course '
                   'where course.cno = textbook_course.cno and bno = %s '
                   'order by cno', (bno,))
    courses = cursor.fetchall()
    cursor.execute('select bno, bname from textbook where bno = %s', (bno,))
    textbook = cursor.fetchone()
    cursor.close()
    return render_template('admin/textbook_to_course.html', courses=courses, textbook=textbook)


@bp.route('/assign_textbook', methods=('POST',))
@check_permission('Admin', False)
def assign_textbook():
    bno = request.form['bno']
    cno = request.form['cno']
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select * from textbook_course where bno = %s and cno = %s', (bno, cno))
    if cursor.fetchone() is not None:
        flash('该教材已被指定为该课程所用！')
    else:
        cursor.execute('select * from textbook where bno = %s', (bno,))
        if cursor.fetchone() is None:
            flash('不存在该教材！')
        else:
            cursor.execute('select * from course where cno = %s', (cno,))
            if cursor.fetchone() is None:
                flash('不存在该课程！')
            else:
                cursor.callproc('assign_textbook', (bno, cno))
                db.commit()
                flash('教材指定成功！')
    cursor.close()
    return redirect(request.referrer or url_for('index'))


@bp.route('/unassign_textbook', methods=('POST',))
@check_permission('Admin', False)
def unassign_textbook():
    bno = request.form['bno']
    cno = request.form['cno']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('select * from textbook_course where bno = %s and cno = %s', (bno, cno))
    if cursor.fetchone() is None:
        flash('该教材并未被该课程指定！')
    else:
        cursor.callproc('unassign_textbook', (bno, cno))
        db.commit()
        flash('取消指定教材成功！')
    cursor.close()
    return redirect(request.referrer or url_for('index'))


@bp.route('/course_to_course/<int:cno>', methods=('GET',))
@check_permission('Admin', False)
def course_to_course(cno):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select course.cno cno, cname, ctype, ccredit, cdept, ccap, cselect '
                   'from course, course_course '
                   'where course.cno = course_course.pcno and course_course.cno = %s '
                   'order by cno', (cno,))
    courses = cursor.fetchall()
    cursor.execute('select cno, cname from course where cno = %s', (cno,))
    course = cursor.fetchone()
    cursor.close()
    return render_template('admin/course_to_course.html', courses=courses, course=course)


@bp.route('/assign_prev_course', methods=('POST',))
@check_permission('Admin', False)
def assign_prev_course():
    pcno = request.form['pcno']
    cno = request.form['cno']
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select * from course_course where pcno = %s and cno = %s', (pcno, cno))
    if cursor.fetchone() is not None:
        flash('已存在该先修课程！')
    else:
        cursor.execute('select * from course where cno = %s', (cno,))
        if cursor.fetchone() is None:
            flash('不存在该课程！')
        else:
            cursor.execute('select * from course where cno = %s', (pcno,))
            if cursor.fetchone() is None:
                flash('不存在该课程！')
            else:
                cursor.callproc('assign_prev_course', (pcno, cno))
                db.commit()
                flash('先修课程指定成功！')
    cursor.close()
    return redirect(request.referrer or url_for('index'))


@bp.route('/unassign_prev_course', methods=('POST',))
@check_permission('Admin', False)
def unassign_prev_course():
    pcno = request.form['pcno']
    cno = request.form['cno']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('select * from course_course where pcno = %s and cno = %s', (pcno, cno))
    if cursor.fetchone() is None:
        flash('不存在该先修关系！')
    else:
        cursor.callproc('unassign_prev_course', (pcno, cno))
        db.commit()
        flash('取消先修关系成功！')
    cursor.close()
    return redirect(request.referrer or url_for('index'))


@bp.route('/room_to_course/<int:rno>', methods=('GET',))
@check_permission('Admin', False)
def room_to_course(rno):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select course.cno cno, cname, time '
                   'from course, room_course '
                   'where course.cno = room_course.cno '
                   'and room_course.rno = %s', (rno,))
    courses = cursor.fetchall()
    table = [[[] for j in range(4)] for i in range(5)]
    for course in courses:
        time = course['time'].split('-')
        dim0 = int(time[0]) - 1
        dim1 = int(time[1]) - 1
        item = dict()
        item['cno'] = course['cno']
        item['cname'] = course['cname']
        cursor.execute('select tname from teacher where tno in '
                       '(select tno from teacher_course where cno = %s)', (course['cno'],))
        entries = cursor.fetchall()
        item['tname'] = [entry['tname'] for entry in entries]
        table[dim0][dim1].append(item)
    cursor.execute('select rno, rname from room where rno = %s', (rno,))
    room = cursor.fetchone()
    cursor.close()
    return render_template('admin/room_to_course.html', table=table, room=room)


@bp.route('/course_to_room/<int:cno>', methods=('GET',))
@check_permission('Admin', False)
def course_to_room(cno):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select room.rno rno, rname, time '
                   'from room, room_course '
                   'where room.rno = room_course.rno '
                   'and room_course.cno = %s', (cno,))
    rooms = cursor.fetchall()
    table = [[[] for j in range(4)] for i in range(5)]
    for room in rooms:
        time = room['time'].split('-')
        dim0 = int(time[0]) - 1
        dim1 = int(time[1]) - 1
        item = dict()
        item['rno'] = room['rno']
        item['rname'] = room['rname']
        table[dim0][dim1].append(item)
    cursor.execute('select cno, cname from course where cno = %s', (cno,))
    course = cursor.fetchone()
    cursor.close()
    return render_template('admin/course_to_room.html', table=table, course=course)


@bp.route('/assign_course', methods=('POST',))
@check_permission('Admin', False)
def assign_course():
    rno = request.form['rno']
    cno = request.form['cno']
    time = request.form['time']
    if len(time) != 3 or time[1] != '-' or not time[0].isdigit() or not time[2].isdigit():
        flash('课程时间不合法！')
        return redirect(request.referrer or url_for('index'))
    if not (1 <= int(time[0]) <= 5 and 1 <= int(time[2]) <= 4):
        flash('课程时间不合法！')
        return redirect(request.referrer or url_for('index'))
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select * from room_course where cno = %s and time = %s', (cno, time))
    if cursor.fetchone() is not None:
        flash('该课程在该时间段已经排课！')
    else:
        cursor.execute('select * from room_course where rno = %s and time = %s', (rno, time))
        if cursor.fetchone() is not None:
            flash('该教室在该时间段已经排课！')
        else:
            cursor.execute('select ccap from course where cno = %s', (cno,))
            course = cursor.fetchone()
            if course is None:
                flash('不存在该课程！')
            else:
                cursor.execute('select rcap from room where rno = %s', (rno,))
                room = cursor.fetchone()
                if room is None:
                    flash('不存在该教室！')
                elif int(room['rcap']) < int(course['ccap']):
                    flash('该教室容量过小，不能满足课程需要！')
                else:
                    cursor.callproc('assign_course', (rno, cno, time))
                    db.commit()
                    flash('排课成功！')
    cursor.close()
    return redirect(request.referrer or url_for('index'))


@bp.route('/unassign_course', methods=('POST',))
@check_permission('Admin', False)
def unassign_course():
    rno = request.form['rno']
    cno = request.form['cno']
    time = request.form['time']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('select * from room_course where rno = %s and cno = %s and time = %s', (rno, cno, time))
    if cursor.fetchone() is None:
        flash('不存在该排课关系！')
    else:
        cursor.callproc('unassign_course', (rno, cno, time))
        db.commit()
        flash('取消排课成功！')
    cursor.close()
    return redirect(request.referrer or url_for('index'))


@bp.route('/list_ratings/<int:cno>', methods=('GET',))
@check_permission('Admin', False)
def list_ratings(cno):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute('select cno, cname from course where cno = %s', (cno,))
    course = cursor.fetchone()

    cursor.execute('select avg(score) avg_score, count(*) cnt '
                   'from rating, course '
                   'where rating.cno = course.cno '
                   'and rating.cno = %s', (cno,))
    rating_info = cursor.fetchone()

    cursor.execute('select student.sno sno, sname, score, tags, comment '
                   'from rating, student '
                   'where rating.sno = student.sno '
                   'and rating.cno = %s', (cno,))
    ratings = cursor.fetchall()
    for rating in ratings:
        tags = rating['tags']
        for i in range(1, 7):
            target = 'tag' + str(i)
            rating[target] = int(tags[i - 1])

    cursor.close()
    return render_template('admin/list_ratings.html', course=course, rating_info=rating_info, ratings=ratings)


@bp.route('/unrate_course', methods=('POST',))
@check_permission('Admin', False)
def unrate_course():
    sno = request.form['sno']
    cno = request.form['cno']
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select * from rating where sno = %s and cno = %s', (sno, cno))
    item = cursor.fetchone()
    if item is None:
        flash('该学生并未评价过该课程！')
    else:
        cursor.callproc('unrate_course', (sno, cno))
        db.commit()
        flash('删除评价成功！')
    cursor.close()
    return redirect(url_for('admin.list_ratings', cno=cno))
