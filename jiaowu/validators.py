import re

from jiaowu.db_base import get_db


class ValidateException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self.info = info

    def __str__(self):
        return self.info


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
            'SELECT sno'
            ' FROM student'
            ' WHERE sno = %s',
            (input_str,)
        )
        student = cursor.fetchone()
        cursor.close()
        if student is not None:
            raise ValidateException("学号不能重复！")

    @staticmethod
    def spwd(input_str):
        if len(input_str) == 0:
            raise ValidateException("密码不能为空！")

        if len(input_str) > 128:
            raise ValidateException("密码过长！")

    @staticmethod
    def sname(input_str):
        if len(input_str) == 0:
            raise ValidateException("姓名不能为空！")

        if len(input_str) > 32:
            raise ValidateException("姓名过长！")

    @staticmethod
    def ssex(input_str):
        if input_str != "男" and input_str != "女":
            raise ValidateException("性别取值必须为“男”或“女”！")

    @staticmethod
    def sid(input_str):
        if not str.isdigit(input_str) or len(input_str) != 18:
            raise ValidateException("身份证号不合法！")

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'SELECT sid'
            ' FROM student'
            ' WHERE sid = %s',
            (input_str,)
        )
        student = cursor.fetchone()
        cursor.close()
        if student is not None:
            raise ValidateException("身份证号不能重复！")

    @staticmethod
    def sgrade(input_str):
        if len(input_str) > 10:
            raise ValidateException("年级信息过长！")

    @staticmethod
    def sdept(input_str):
        if len(input_str) > 32:
            raise ValidateException("院系信息过长！")

    @staticmethod
    def stel(input_str):
        if len(input_str) == 0:
            return

        if not str.isdigit(input_str) or len(input_str) != 11:
            raise ValidateException("手机号码不合法！")

    @staticmethod
    def smail(input_str):
        if len(input_str) == 0:
            return

        if not re.match(r'^\w+@(\w+\.\w+)$', input_str):
            raise ValidateException("邮件地址不合法！")
