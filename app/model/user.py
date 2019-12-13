# -*- coding: utf-8 -*-

from typing import Optional, AnyStr
from sqlalchemy import Column, ForeignKey, String, Sequence
from sqlalchemy import FLOAT, TEXT, INTEGER, DECIMAL, SMALLINT, Table
from app.utils import db
from .base import BaseModel


class User(db.Model, BaseModel):
    __tablename__ = 'bao_user'

    id = Column(INTEGER, Sequence('user_id_seq', start=1,
                                  increment=1), primary_key=True, comment='用户的id')
    sex = Column(SMALLINT, nullable=True, default=0, comment='0 未设置 1 男性 2 女性')
    identifier = Column(String(128), nullable=True,
                        comment='用户的标识符，在某些情况不适合用id，会用此字段')
    mobilephone = Column(String(11), nullable=True)
    email = Column(String(64), nullable=True, unique=True)
    password = Column(String(64), nullable=True)
    status = Column(SMALLINT, nullable=True, default=1,
                    comment='0 未激活 1 正常 2 异常 3 注销')

    def __init__(
            self,
            email: AnyStr,
            sex: int = 0,
            mobilephone: Optional[AnyStr] = None,
            password: Optional[AnyStr] = None,
            status: int = 1,
            identifier: Optional[AnyStr] = None
    ):

        self.email = email
        self.mobilephone = mobilephone
        self.password = password
        self.status = status
        self.sex = sex
        self.identifier = identifier


class LoginRecordModel(db.Model, BaseModel):
    __tablename__ = 'bao_login_record'

    record_id = Column(INTEGER, Sequence('login_record_id_seq', start=1,
                                         increment=1), primary_key=True, comment='用户的登录记录')
    user_id = Column(INTEGER, nullable=True)
    op_time = Column(String(20), nullable=True)
    op_ip = Column(String(20), nullable=True)

    def __init__(
            self,
            user_id: int,
            op_ip: Optional[AnyStr] = None,
            op_time: Optional[AnyStr] = None
    ):
        from app.utils import get_unix_time_tuple
        self.user_id = user_id
        self.op_time = op_time or get_unix_time_tuple()
        self.op_ip = op_ip
