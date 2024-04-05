from functools import wraps

from flask import g, redirect


# 登录的装饰器
def login_required(func):
    @wraps(func)    # 保留func的信息
    def inner(*args, **kwargs):
        if g.user:
            return func(*args,**kwargs)
        else:
            return redirect("/auth/login")
    return inner