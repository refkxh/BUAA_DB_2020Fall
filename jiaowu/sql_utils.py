import os

from flask import current_app


def simple_sql_file_to_list(filename):
    contents = ''
    with open(os.path.join(current_app.root_path, filename), mode='r', encoding='utf-8') as f:
        for line in f:
            contents += line.strip()

    sql_list = contents.split(';')[:-1]

    return sql_list


drop_procedures = ['drop procedure if exists create_student',
                   'drop procedure if exists update_student',
                   'drop procedure if exists update_student_pwd',
                   'drop procedure if exists delete_student'
                   ]

create_procedures = ['create procedure create_student(sno_in varchar(10),'
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
                     'delete from student '
                     'where sno = sno_in;'
                     'commit;'
                     'end'
                     ]
