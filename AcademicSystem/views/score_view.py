from flask import request, Blueprint, jsonify
from flask_cors import CORS

# from config import cors
from config import cursor, conn


# 创建蓝图
score_bp = Blueprint('score', __name__)

cors = CORS(score_bp, resources={r"/*": {"origins": "*"}})


# 成绩模块  -->  查单科成绩（按输入的课程名）
@score_bp.route('/one/score', methods=['POST'])
def get_one_score():
    data = request.get_json()
    sno = data['sno']
    cname = data['cname']   # 是否为空由前端判断
    print("sno: ", sno)
    print("cname: ", cname)

    sql = ("SELECT * FROM sc WHERE sno='{}' AND cname='{}' ").format(sno, cname)
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)

    response_data = {}
    data = {}
    if results is None or len(results) == 0:
        response_data['state'] = 'fail'
        response_data['message'] = '不存在该门课'
        data['results'] = None
        response_data['data'] = data
        return jsonify(response_data)
    elif results[0][7] is None:
        response_data['state'] = 'fail'
        response_data['message'] = '本课程没有成绩'
        data['results'] = None
        response_data['data'] = data
        return jsonify(response_data)
    else:
        response_data['state'] = 'success'
        response_data['message'] = '查找成功'
        keys = ['id', 'sno', 'cno', 'tname', 'credit', 'academic_year', 'semester', 'score', 'type', 'cname',
                'course_weekday', 'course_time', 'classroom']
        results = [dict(zip(keys, row)) for row in results]
        data['results'] = results
        response_data['data'] = data
        return jsonify(response_data)


# 成绩模块 --> 查多科成绩（按学年）--> 计算学分绩
def compute_credits(results):
    print(results)
    total_credits = 0
    avarage_credits = 0
    for result in results:
        total_credits = total_credits + result['credit']
    for result in results:
        avarage_credits = avarage_credits + result['score'] * (result['credit']/total_credits)
    return avarage_credits


# 成绩模块  -->  查多科成绩（按学年）
@score_bp.route('/more/score/<page>', methods=['POST'])
def get_more_score(page):
    data = request.get_json()
    sno = data['sno']
    academic_year = data['academic_year']   # 学年
    print("sno: ", sno)
    print("academic_year: ", academic_year)
    page = int(page)

    sql = ("SELECT * FROM SC WHERE sno='{}' AND academic_year='{}' AND score is not null ").format(sno, academic_year)
    cursor.execute(sql)
    results = cursor.fetchall()
    total_results = len(results)
    results = results[(page - 1) * 10: page * 10]  # 分页
    print(results)

    response_data = {}
    data = {}
    if results is None or len(results) == 0:
        response_data['state'] = 'fail'
        response_data['message'] = '本学年没有选修课程'
        data['results'] = None    # 学分绩
        response_data['data'] = data
        return jsonify(response_data)
    else:
        keys = ['id', 'sno', 'cno', 'tname', 'credit', 'academic_year', 'semester', 'score', 'type', 'cname',
                'course_weekday', 'course_time', 'classroom']
        results = [dict(zip(keys, row)) for row in results]

        # 计算学分绩
        score = compute_credits(results)

        response_data['state'] = 'success'
        response_data['message'] = '查找成功'
        data['results'] = results
        data['total_result'] = total_results
        data['page'] = page
        data['credit_score'] = score
        response_data['data'] = data

        return jsonify(response_data)

