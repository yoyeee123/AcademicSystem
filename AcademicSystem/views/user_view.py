from flask import request, Blueprint, jsonify

from flask_cors import CORS
from config import cursor, conn


# 创建蓝图
user_bp = Blueprint('user', __name__)

cors = CORS(user_bp, resources={r"/*": {"origins": "*"}})


# 用户模块  --> 登录
@user_bp.route('/login', methods=['POST', 'GET'])
def login():  # put user_bplication's code here
    # 从前端获取数据
    data = request.get_json()
    sno = data['sno']
    password = data['password']

    # 查表
    sql = "SELECT * FROM student WHERE sno='{}' and password='{}'".format(sno, password)
    cursor.execute(sql)
    conn.commit()

    result = cursor.fetchall()
    print(result)

    response_data = {}
    data = {}
    if len(result) != 0:
        response_data = {'state': 'success', 'message': '登录成功'}
        data['sno'] = result[0][1]
        response_data['data'] = data
        return jsonify(response_data)
    else:
        response_data = {'state': 'fail', 'message': '学号或密码错误', 'data': None}
        return jsonify(response_data)


# 用户模块  --> 注册功能
"""
@user_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # 获取数据
        data = request.get_json()
        sno = data['sno']
        sname = data['sname']
        password = data['password'] # 密码
        dept = data['dept']  # 学院
        major = data['major']   # 专业
        grade = data['grade']   # 年级
        semester = '1'
        # 默认是计算机学院的学分
        locate = '南湖校区'
        core_credits = 60
        personal_development_credits = 25
        general_core_credits = 10
        general_required_credits = 20

        # 插入数据
        sql = ("INSERT INTO student(sno, sname, password, dept, major, grade"
               "semester, locate, core_credits,personal_development_credits,general_core_credits,general_required_credits) "
               "VALUES ('{}', '{}','{}', '{}','{}', '{}','{}', '{}','{}', '{}','{}', '{}')").format(
            sno, sname, password, dept, major, grade,
            semester, locate, core_credits, personal_development_credits, general_core_credits, general_required_credits)
        try:
            # 插入记录
            cursor.execute(sql)
            conn.commit()
            response_data = {'state': 'success', 'message': '注册成功'}
        except Exception as e:
            response_data = {'state': 'fail', 'message':  f'注册失败！ Error: {str(e)}'}
        return jsonify(response_data)
"""


# 用户模块  --> 获取用户信息
@user_bp.route('/userinfo/<sno>', methods=['GET'])
def get_userinfo(sno):
    # 查表
    sql = "SELECT * FROM student WHERE sno='{}'".format(sno)
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)

    # if result is None:
    #     return jsonify({'error': 'No user found for the given student number'})

    # 转化为json格式
    keys = ['id', 'sno', 'sname', 'password', 'dept', 'major', 'grade', 'semester', 'location']
    userInfo = dict(zip(keys, result))
    return jsonify(userInfo)


# 用户模块  --> 修改密码
@user_bp.route('/update/pwd', methods=['POST'])
def update_pwd():
    # 获取数据
    data = request.get_json()
    sno = data.get('sno')
    old_password = data.get('old_password')
    new_password = data['new_password']

    # 查表
    sql = "SELECT * FROM student WHERE sno='{}' and password='{}'".format(sno, old_password)
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchone()
    print(result)
    if result is None:  # 用户不存在
        response_data = {'state': 'fail', 'message': '旧密码输入错误'}
        return jsonify(response_data)
    else:
        password = result[3]
        # 修改密码
        sql = "UPDATE student SET password='{}' WHERE sno='{}'".format(new_password, sno)
        cursor.execute(sql)
        conn.commit()
        response_data = {'state': 'success', 'message': '密码修改成功'}
        return jsonify(response_data)
