# -*- coding:utf-8 -*-

from db import Modal
from db import IntegerField, StringField


class User(Modal):
    # 表名
    # __tablename__ = "User1"

    id = IntegerField('id')
    username = StringField('username')
    email = StringField('email')
    password = StringField('password')


if __name__ == '__main__':
    u = User(id=1, username="xomas", email="zhouhaozt@126.com", password="123456")
    u.save()