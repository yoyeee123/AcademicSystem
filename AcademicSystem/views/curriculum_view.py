from flask import request, Blueprint, jsonify
from flask_cors import CORS

from config import cursor, conn

from datetime import datetime
# 创建蓝图
curriculum_bp = Blueprint('curriculum', __name__)

cors = CORS(curriculum_bp, resources={r"/*": {"origins": "*"}})


# 课表模块  --> 查看课表
@curriculum_bp.route('/my_curriculum/<sno>', methods=["POST"])
def my_curriculum(sno):
    sql = ("SELECT * FROM SC WHERE sno='{}' AND score is NULL ORDER BY course_weekday and course_time").format(sno)
    cursor.execute(sql)
    results = cursor.fetchall()
    # print(results)

    response_data = {}
    data = {}
    if len(results) > 0:
        # 加key
        keys = ['id', 'sno', 'cno', 'tname', 'credit', 'academic_year', 'semester', 'score', 'type', 'cname', 'course_weekday', 'course_time', 'classroom']
        results = [dict(zip(keys, row)) for row in results]

        response_data['state'] = 'success'
        response_data['message'] = '查找成功'
        rows = []
        for row in results:
            # print("row:  ", row)
            result = {}

            # 字典的键为变量key
            if row['course_weekday'] == '星期一':
                key = 'mon'
            elif row['course_weekday'] == '星期二':
                key = 'tue'
            elif row['course_weekday'] == '星期三':
                key = 'wes'
            elif row['course_weekday'] == '星期四':
                key = 'thu'
            elif row['course_weekday'] == '星期五':
                key = 'fri'
            elif row['course_weekday'] == '星期六':
                key = 'sat'
            else:
                key = 'sun'
            # 字典的键为变量key
            result = {key: {"cname": row['cname'], 'tname': row['tname'], 'classroom': row['classroom']}}

            section = {"course_time": row['course_time']}
            result['section'] = section

            rows.append(result)

        data['results'] = rows
        response_data['data'] = data
        return jsonify(response_data)
    else:
        response_data['state'] = 'fail'
        response_data['message'] = '课表为空'
        data['results'] = None
        response_data['data'] = data
        return jsonify(response_data)
