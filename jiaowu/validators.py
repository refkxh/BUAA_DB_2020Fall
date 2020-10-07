class ValidateException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self.info = info

    def __str__(self):
        return self.info


class Student:
    @staticmethod
    def sno(input_str):
        return None

    @staticmethod
    def spwd(input_str):
        return None

    @staticmethod
    def sname(input_str):
        return None

    @staticmethod
    def ssex(input_str):
        return None

    @staticmethod
    def sid(input_str):
        return None

    @staticmethod
    def sgrade(input_str):
        return None

    @staticmethod
    def sdept(input_str):
        return None

    @staticmethod
    def stel(input_str):
        return None

    @staticmethod
    def smail(input_str):
        return None
