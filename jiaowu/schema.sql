drop database if exists jiaowu;
create database jiaowu;
use jiaowu;

create table student
(
    sno    varchar(10) primary key,
    spwd   varchar(128) not null,
    sname  varchar(32)  not null,
    ssex   char(2)      not null check (ssex in ('男', '女')),
    sid    char(18)     not null unique,
    sgrade varchar(10)  not null,
    sdept  varchar(32)  not null,
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

create table teacher
(
    tno    varchar(10) primary key,
    tpwd   varchar(128) not null,
    tname  varchar(32)  not null,
    tsex   char(2)      not null check (tsex in ('男', '女')),
    ttitle varchar(16)  not null,
    tdept  varchar(32)  not null,
    ttel   varchar(11),
    tmail  varchar(32)
);

create table admin
(
    ano   varchar(10) primary key,
    apwd  varchar(128) not null,
    aname varchar(32)  not null,
    atel  varchar(11),
    amail varchar(32)
);

create table textbook
(
    bno     varchar(32) primary key,
    bname   varchar(64) not null,
    bauthor varchar(64),
    bpress  varchar(32)
);

create table room
(
    rno     int auto_increment primary key,
    rname   varchar(32) not null,
    rcap    int check (rcap >= 0)
);

create table student_course
(
    sno   varchar(10),
    cno   int,
    score int,
    primary key (sno, cno),
    foreign key (sno) references student (sno),
    foreign key (cno) references course (cno)
);
