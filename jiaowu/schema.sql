drop table if exists student;
drop table if exists course;

create table student
(
    sno    varchar(10) primary key,
    spwd   varchar(128) not null,
    sname  nvarchar(16) not null,
    ssex   nchar(1)     not null check (ssex in ('男', '女')),
    sid    char(18)     not null unique,
    sgrade nvarchar(10),
    sdept  nvarchar(32),
    stel   varchar(11),
    smail  varchar(32)
);

create table course
(
    cno     int auto_increment primary key,
    cname   nvarchar(16) not null,
    ctype   nvarchar(5),
    ccredit int          not null,
    cdept   nvarchar(16),
    ccap    int          not null,
    cselect int          not null default '0'
);
