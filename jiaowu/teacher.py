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
        db.commit()
        flash('授课成功！')
    cursor.close()
    return redirect(url_for('teacher.list_untaught_courses'))


@bp.route('/list_taught_courses', methods=('GET',))
@check_permission('Teacher', False)
def list_taught_courses():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select course.cno cno, cname, ctype, ccredit, cdept, ccap, cselect '
                   'from course, teacher_course '
                   'where course.cno = teacher_course.cno and tno = %s '
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
    if cursor.fetchone() is None:
        flash('您并未教授该课程！')
    else:
        cursor.callproc('unteach_course', (current_user.no, cno))
        db.commit()
        flash('取消教授课程成功！')
    cursor.close()
    return redirect(url_for('teacher.list_taught_courses'))


@bp.route('/course_to_stu/<int:cno>', methods=('GET',))
@check_permission('Teacher', False)
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
    return render_template('teacher/course_to_stu.html', students=students, course=course)


@bp.route('/modify_score', methods=('POST',))
@check_permission('Teacher', False)
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


@bp.route('/course_to_textbook/<int:cno>', methods=('GET',))
@check_permission('Teacher', False)
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
    return render_template('teacher/course_to_textbook.html', textbooks=textbooks, course=course)


@bp.route('/assign_textbook', methods=('POST',))
@check_permission('Teacher', False)
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
@check_permission('Teacher', False)
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
@check_permission('Teacher', False)
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
    return render_template('teacher/course_to_course.html', courses=courses, course=course)


@bp.route('/assign_prev_course', methods=('POST',))
@check_permission('Teacher', False)
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
@check_permission('Teacher', False)
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


@bp.route('/timetable', methods=('GET',))
@check_permission('Teacher', False)
def timetable():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select course.cno cno, cname, rname, time '
                   'from course, room, room_course, teacher_course '
                   'where course.cno = room_course.cno and room.rno = room_course.rno '
                   'and room_course.cno = teacher_course.cno and tno = %s', (current_user.no,))
    course_rooms = cursor.fetchall()
    table = [[[] for j in range(4)] for i in range(5)]
    for course_room in course_rooms:
        time = course_room['time'].split('-')
        dim0 = int(time[0]) - 1
        dim1 = int(time[1]) - 1
        item = dict()
        item['cname'] = course_room['cname']
        item['rname'] = course_room['rname']
        cursor.execute('select tname from teacher where tno in '
                       '(select tno from teacher_course where cno = %s)', (course_room['cno'],))
        entries = cursor.fetchall()
        item['tname'] = [entry['tname'] for entry in entries]
        table[dim0][dim1].append(item)
    cursor.close()
    return render_template('teacher/timetable.html', table=table)


@bp.route('/list_ratings/<int:cno>', methods=('GET',))
@check_permission('Teacher', False)
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

    cursor.execute('select sname, score, tags, comment '
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
    return render_template('teacher/list_ratings.html', course=course, rating_info=rating_info, ratings=ratings)
