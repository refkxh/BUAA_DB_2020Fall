from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from jiaowu.db_base import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/info_stu', methods=('GET', 'POST'))
def info_stu():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        pass
    else:
        cursor.execute(
            'SELECT sno, sname, ssex, sid, sgrade, sdept, stel, smail'
            ' FROM Student'
            ' ORDER BY sno'
        )
    students = cursor.fetchall()
    cursor.close()
    return render_template('admin/info_stu.html', students=students)


@bp.route('/create_stu', methods=('GET', 'POST'))
def create_stu():
    '''if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (%s, %s, %s)',
                (title, body, g.user[0])
            )
            db.commit()
            cursor.close()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')'''


@bp.route('/update_stu/<int:sno>', methods=('GET', 'POST'))
def update_stu(sno):
    '''post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'UPDATE post SET title = %s, body = %s'
                ' WHERE id = %s',
                (title, body, id)
            )
            db.commit()
            cursor.close()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)'''


@bp.route('/delete_stu/<int:sno>', methods=('POST',))
def delete(sno):
    '''get_post(id)
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM post WHERE id = %s', (id,))
    db.commit()
    cursor.close()
    return redirect(url_for('blog.index'))'''

