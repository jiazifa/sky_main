from typing import Optional, AnyStr, Dict
from flask import request, current_app, g, Blueprint
from app.utils import UserError
from app.utils import response_error, response_succ
from app.utils import get_random_num, get_unix_time_tuple, getmd5
from app.utils import redisClient
from app.utils import session, text, parse_params, get_current_user
from app.utils import login_require
from app.model import User, LoginRecordModel
import app

api = Blueprint('user', __name__)
app.fetch_route(api, '/user')

@api.route('/register', methods=['POST'])
def register():
    params = parse_params(request)
    email: str = params.get("email")
    password: str = params.get("password")
    q = session.query(User).filter(User.email == email, User.password==password)
    exsist_user = session.query(q.exists())
    if exsist_user:
        return UserError.get_error(error_code=40200)
    user = User(email, password=password)
    session.add(user)
    payload: Dict[AnyStr, int] = {'user_id': user.id}
    return response_succ(body=payload)

@api.route('/login', methods=['POST'])
def login():
    params = parse_params(request)
    email: str = params.get("email")
    password: str = params.get("password")
    exsist_user: User = session.query(User).filter_by(email=email, password=password).first()
    if exsist_user:
        # update log time
        login_time: str = get_unix_time_tuple()
        log_ip: str = request.args.get("user_ip") or request.remote_addr
        record: LoginRecordModel = LoginRecordModel(exsist_user.id, log_ip)
        record.save()
        # update token
        token: AnyStr = getmd5("-".join([email, password, login_time, get_random_num()]))
        # 保存到redis中, 设置有效时间为7天
        redisClient.set(str(exsist_user.id), token, 60*60*24*7)
        return response_succ(body={'token': token})
    else:
        return UserError.get_error(40203)


@api.route('/logout', methods=['POST'])
def logout():
    """  登出
    设置redis时间为过期
    """
    pass

@api.route('/info', methods=['GET'])
@login_require
def user_info():
    params = parse_params(request)
    user: User = get_current_user()

