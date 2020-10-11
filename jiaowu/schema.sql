drop table if exists student;
drop table if exists course;
drop table if exists admin;

create table student
(
    sno    varchar(10) primary key,
    spwd   varchar(128) not null,
    sname  varchar(32)  not null,
    ssex   char(2)      not null check (ssex in ('男', '女')),
    sid    char(18)     not null unique,
    sgrade varchar(10),
    sdept  varchar(32),
    stel   varchar(11),
    smail  varchar(32)
);

create table course
(
    cno     int auto_increment primary key,
    cname   varchar(32) not null,
    ctype   varchar(10),
    ccredit int         not null,
    cdept   varchar(32),
    ccap    int         not null,
    cselect int         not null default '0'
);

create table admin
(
    ano   varchar(10) primary key,
    apwd  varchar(128) not null,
    aname varchar(32)  not null,
    atel  varchar(11),
    amail varchar(32)
);
