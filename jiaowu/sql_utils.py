import os

from flask import current_app


def simple_sql_file_to_list(filename):
    contents = ''
    with open(os.path.join(current_app.root_path, filename), mode='r', encoding='utf-8') as f:
        for line in f:
            contents += line.strip()

    sql_list = contents.split(';')[:-1]

    return sql_list


procedures = ['create procedure create_student(sno_in varchar(10),'
              'spwd_in varchar(128), '
              'sname_in varchar(32),'
              'ssex_in char(2),'
              'sid_in char(18),'
              'sgrade_in varchar(10),'
              'sdept_in varchar(32),'
              'stel_in varchar(11),'
              'smail_in varchar(32))'
              'begin '
              'insert into student '
              '(sno, spwd, sname, ssex, sid, sgrade, sdept, stel, smail)'
              'values (sno_in, spwd_in, sname_in, ssex_in, sid_in, sgrade_in,'
              'sdept_in, stel_in, smail_in);'
              'commit;'
              'end',

              'create procedure update_student(sno_in varchar(10),'
              'sname_in varchar(32),'
              'ssex_in char(2),'
              'sid_in char(18),'
              'sgrade_in varchar(10),'
              'sdept_in varchar(32),'
              'stel_in varchar(11),'
              'smail_in varchar(32))'
              'begin '
              'update student '
              'set sname  = sname_in,'
              'ssex   = ssex_in,'
              'sid    = sid_in,'
              'sgrade = sgrade_in,'
              'sdept  = sdept_in,'
              'stel   = stel_in,'
              'smail  = smail_in '
              'where sno = sno_in;'
              'commit;'
              'end',

              'create procedure update_student_pwd(sno_in varchar(10),'
              'spwd_in varchar(128))'
              'begin '
              'update student '
              'set spwd  = spwd_in '
              'where sno = sno_in;'
              'commit;'
              'end',

              'create procedure delete_student(sno_in varchar(10))'
              'begin '
              'delete from student_course '
              'where sno = sno_in;'
              'delete from student '
              'where sno = sno_in;'
              'commit;'
              'end',

              'create procedure create_course(cname_in varchar(32),'
              'ctype_in varchar(10),'
              'ccredit_in int,'
              'cdept_in varchar(32),'
              'ccap_in int)'
              'begin '
              'insert into course (cname, ctype, ccredit, cdept, ccap)'
              ' values (cname_in, ctype_in, ccredit_in, cdept_in, ccap_in);'
              'commit;'
              'end',

              'create procedure update_course(cno_in int,'
              'cname_in varchar(32),'
              'ctype_in varchar(10),'
              'ccredit_in int,'
              'cdept_in varchar(32),'
              'ccap_in int)'
              'begin '
              'update course set cname = cname_in, ctype = ctype_in, ccredit = ccredit_in,'
              ' cdept = cdept_in, ccap = ccap_in'
              ' where cno = cno_in;'
              'commit;'
              'end',

              'create procedure delete_course(cno_in int)'
              'begin '
              'delete from student_course '
              'where cno = cno_in;'
              'delete from course '
              'where cno = cno_in;'
              'commit;'
              'end',

              'create procedure create_admin(ano_in varchar(10),'
              'apwd_in varchar(128), '
              'aname_in varchar(32),'
              'atel_in varchar(11),'
              'amail_in varchar(32))'
              'begin '
              'insert into admin (ano, apwd, aname, atel, amail)'
              ' values (ano_in, apwd_in, aname_in, atel_in, amail_in);'
              'commit;'
              'end',

              'create procedure update_admin(ano_in varchar(10),'
              'aname_in varchar(32),'
              'atel_in varchar(11),'
              'amail_in varchar(32))'
              'begin '
              'update admin set aname = aname_in, atel = atel_in, amail = amail_in'
              ' where ano = ano_in;'
              'commit;'
              'end',

              'create procedure update_admin_pwd(ano_in varchar(10),'
              'apwd_in varchar(128))'
              'begin '
              'update admin '
              'set apwd  = apwd_in '
              'where ano = ano_in;'
              'commit;'
              'end',

              'create procedure delete_admin(ano_in varchar(10))'
              'begin '
              'delete from admin '
              'where ano = ano_in;'
              'commit;'
              'end',

              'create procedure select_course(sno_in varchar(10), cno_in int)'
              'begin '
              'insert into student_course (sno, cno) '
              'values (sno_in, cno_in);'
              'commit;'
              'end',

              'create procedure unselect_course(sno_in varchar(10), cno_in int)'
              'begin '
              'delete from student_course '
              'where sno = sno_in and cno = cno_in;'
              'commit;'
              'end',

              'create procedure update_score(sno_in varchar(10), cno_in int, score_in int)'
              'begin '
              'update student_course '
              'set score = score_in '
              'where sno = sno_in and cno = cno_in;'
              'commit;'
              'end'
              ]

triggers = ['create trigger increase_cselect '
            'after insert on student_course '
            'for each row '
            'update course set cselect = cselect + 1 where course.cno = NEW.cno',

            'create trigger decrease_cselect '
            'after delete on student_course '
            'for each row '
            'update course set cselect = cselect - 1 where course.cno = OLD.cno',
            ]
