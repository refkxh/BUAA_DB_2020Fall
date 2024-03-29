import re

from jiaowu.db_base import get_db


class ValidateException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self.info = info

    def __str__(self):
        return self.info


def pwd(input_str, nullable=False):
    if not nullable and len(input_str) == 0:
        raise ValidateException("密码不能为空！")

    if not nullable and len(input_str) < 6:
        raise ValidateException("密码不能少于6位！")

    if len(input_str) > 128:
        raise ValidateException("密码过长！")


def name(input_str):
    if len(input_str) == 0:
        raise ValidateException("姓名不能为空！")

    if len(input_str) > 32:
        raise ValidateException("姓名过长！")


def sex(input_str):
    if input_str != "男" and input_str != "女":
        raise ValidateException("性别取值必须为“男”或“女”！")


def dept(input_str):
    if len(input_str) > 32:
        raise ValidateException("院系信息过长！")


def tel(input_str):
    if len(input_str) == 0:
        return

    if not str.isdigit(input_str) or len(input_str) != 11:
        raise ValidateException("手机号码不合法！")


def mail(input_str):
    if len(input_str) == 0:
        return

    if not re.match(r'^\w+@(\w+(\.\w+)+)$', input_str):
        raise ValidateException("邮件地址不合法！")


def grade(input_str):
    if len(input_str) > 10:
        raise ValidateException("年级信息过长！")


def cap(input_str):
    if len(input_str) == 0:
        raise ValidateException("容量不能为空！")
    if not str.isdigit(input_str):
        raise ValidateException("容量不合法！")
    if int(input_str) > 8192:
        raise ValidateException("容量过大！")


class Student:
    @staticmethod
    def sno(input_str):
        if len(input_str) == 0:
            raise ValidateException("学号不能为空！")

        if len(input_str) > 10:
            raise ValidateException("学号过长！")

        if not str.isalnum(input_str):
            raise ValidateException("学号只能由字母和数字组成！")

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'select sno'
            ' from student'
            ' where sno = %s',
            (input_str,)
        )
        student = cursor.fetchone()
        cursor.close()
        if student is not None:
            raise ValidateException("学号不能重复！")

    @staticmethod
    def spwd(input_str, nullable=False):
        pwd(input_str, nullable)

    @staticmethod
    def sname(input_str):
        name(input_str)

    @staticmethod
    def ssex(input_str):
        sex(input_str)

    @staticmethod
    def sid(input_str, cur_sno=None):
        if not str.isdigit(input_str) or len(input_str) != 18:
            raise ValidateException("身份证号不合法！")

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            'select *'
            ' from student'
            ' where sid = %s',
            (input_str,)
        )
        student = cursor.fetchone()
        cursor.close()
        if student is not None and student['sno'] != cur_sno:
            raise ValidateException("身份证号不能重复！")

    @staticmethod
    def sgrade(input_str):
        grade(input_str)

    @staticmethod
    def sdept(input_str):
        dept(input_str)

    @staticmethod
    def stel(input_str):
        tel(input_str)

    @staticmethod
    def smail(input_str):
        mail(input_str)


class Course:
    @staticmethod
    def cname(input_str):
        if len(input_str) == 0:
            raise ValidateException("课程名不能为空！")

        if len(input_str) > 32:
            raise ValidateException("课程名过长！")

    @staticmethod
    def ctype(input_str):
        if len(input_str) > 10:
            raise ValidateException("课程类型过长！")

    @staticmethod
    def ccredit(input_str):
        if len(input_str) == 0:
            raise ValidateException("学分不能为空！")
        if not str.isdigit(input_str):
            raise ValidateException("学分不合法！")
        if int(input_str) > 256:
            raise ValidateException("学分过大！")

    @staticmethod
    def cdept(input_str):
        dept(input_str)

    @staticmethod
    def ccap(input_str):
        cap(input_str)


class Teacher:
    @staticmethod
    def tno(input_str):
        if len(input_str) == 0:
            raise ValidateException("工号不能为空！")

        if len(input_str) > 10:
            raise ValidateException("工号过长！")

        if not str.isalnum(input_str):
            raise ValidateException("工号只能由字母和数字组成！")

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'select *'
            ' from teacher'
            ' where tno = %s',
            (input_str,)
        )
        teacher = cursor.fetchone()
        cursor.close()
        if teacher is not None:
            raise ValidateException("工号不能重复！")

    @staticmethod
    def tpwd(input_str, nullable=False):
        pwd(input_str, nullable)

    @staticmethod
    def tname(input_str):
        name(input_str)

    @staticmethod
    def tsex(input_str):
        sex(input_str)

    @staticmethod
    def ttitle(input_str):
        if len(input_str) > 16:
            raise ValidateException("职称信息过长！")

    @staticmethod
    def tdept(input_str):
        dept(input_str)

    @staticmethod
    def ttel(input_str):
        tel(input_str)

    @staticmethod
    def tmail(input_str):
        mail(input_str)


class Admin:
    @staticmethod
    def ano(input_str):
        if len(input_str) == 0:
            raise ValidateException("教务管理号不能为空！")

        if len(input_str) > 10:
            raise ValidateException("教务管理号过长！")

        if not str.isalnum(input_str):
            raise ValidateException("教务管理号只能由字母和数字组成！")

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'select *'
            ' from admin'
            ' where ano = %s',
            (input_str,)
        )
        admin = cursor.fetchone()
        cursor.close()
        if admin is not None:
            raise ValidateException("教务管理号不能重复！")

    @staticmethod
    def apwd(input_str, nullable=False):
        pwd(input_str, nullable)

    @staticmethod
    def aname(input_str):
        name(input_str)

    @staticmethod
    def atel(input_str):
        tel(input_str)

    @staticmethod
    def amail(input_str):
        mail(input_str)


class Textbook:
    @staticmethod
    def bno(input_str):
        if len(input_str) == 0:
            raise ValidateException("书号不能为空！")

        if len(input_str) > 32:
            raise ValidateException("书号过长！")

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'select *'
            ' from textbook'
            ' where bno = %s',
            (input_str,)
        )
        textbook = cursor.fetchone()
        cursor.close()
        if textbook is not None:
            raise ValidateException("书号不能重复！")

    @staticmethod
    def bname(input_str):
        if len(input_str) == 0:
            raise ValidateException("书名不能为空！")

        if len(input_str) > 64:
            raise ValidateException("书名过长！")

    @staticmethod
    def bauthor(input_str):
        if len(input_str) > 64:
            raise ValidateException("作者信息过长！")

    @staticmethod
    def bpress(input_str):
        if len(input_str) > 32:
            raise ValidateException("出版社信息过长！")


class Room:
    @staticmethod
    def rname(input_str):
        if len(input_str) == 0:
            raise ValidateException("教室名不能为空！")

        if len(input_str) > 32:
            raise ValidateException("教室名过长！")

    @staticmethod
    def rcap(input_str):
        cap(input_str)
