drop table if exists student;
drop table if exists course;

create table student
(
    sno    varchar(10) primary key,
    spwd   varchar(128) not null,
    sname  varchar(32)  not null,
    ssex   varchar(4)   not null check (ssex in ('男', '女')),
    sid    varchar(18)  not null unique,
    sgrade varchar(10),
    sdept  varchar(32),
    stel   varchar(11),
    smail  varchar(30)
);

create table course
(
    cno     int auto_increment primary key,
    cname   varchar(32) not null,
    ctype   varchar(10) not null,
    ccredit int         not null,
    cdept   varchar(32),
    ccap    int         not null
);
