from datetime import datetime

from flask import request, Blueprint, jsonify
from flask_cors import CORS

# from config import cors
from config import cursor, conn


# 创建蓝图
room_bp = Blueprint('room', __name__)

cors = CORS(room_bp, resources={r"/*": {"origins": "*"}})


# 教室模块 --> 空闲教室 --> 将查询时间转为为对应的课程节数
def get_course_time(start_time, end_time):
    course_times = []
    if start_time >= '18:00:00':
        course_times.append('9-10')
    elif start_time >= '16:00:00':
        if end_time > '18:00:00':
            course_times.append('7-8')
            course_times.append('9-10')
        else:
            course_times.append('7-8')
    elif start_time >= '14:00:00':
        if end_time > '18:00:00':
            course_times.append('5-6')
            course_times.append('7-8')
            course_times.append('9-10')
        elif end_time > '16:00:00':
            course_times.append('5-6')
            course_times.append('7-8')
        else:
            course_times.append('5-6')
    elif start_time >= '10:00:00':
        if end_time > '18:00:00':
            course_times.append('3-4')
            course_times.append('5-6')
            course_times.append('7-8')
            course_times.append('9-10')
        elif end_time > '16:00:00':
            course_times.append('3-4')
            course_times.append('5-6')
            course_times.append('7-8')
        elif end_time > '14:00:00':
            course_times.append('3-4')
            course_times.append('5-6')
        else:
            course_times.append('3-4')
    else:
        if end_time > '18:00:00':
            course_times.append('1-2')
            course_times.append('3-4')
            course_times.append('5-6')
            course_times.append('7-8')
            course_times.append('9-10')
        elif end_time > '16:00:00':
            course_times.append('1-2')
            course_times.append('3-4')
            course_times.append('5-6')
            course_times.append('7-8')
        elif end_time > '14:00:00':
            course_times.append('1-2')
            course_times.append('3-4')
            course_times.append('5-6')
        elif end_time > '10:00:00':
            course_times.append('1-2')
            course_times.append('3-4')
        else:
            course_times.append('1-2')

    return course_times


# 教室模块  --> 查空闲教室（按校区、时间、）
@room_bp.route('/search/freeroom/<page>', methods=['POST'])
def free_class(page):
    data = request.get_json()
    page = int(page)
    location = data['location']     # 校区
    start_time = data['start_time']     # 前端确保start_time < end_time
    end_time = data['end_time']
    type = data['type']

    # 将时间转化为course_time, 如7-8节
    course_time = get_course_time(start_time, end_time)
    course_time_str = ', '.join(["'{}'".format(time) for time in course_time])
    print(course_time_str)

    # 获取此时此刻的时间: 如 2023-2024学年  下学期  星期三
    current_year = datetime.now().year
    current_month = datetime.now().month
    current_weekday = datetime.today().weekday()
    current_weekday = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'][current_weekday]
    print(current_weekday)

    if current_month > 7:
        academic_year = str(current_year) + '-' + str(current_year + 1)
        semester = '1'
    else:
        academic_year = str(current_year - 1) + '-' + str(current_year)
        semester = '2'

    # select 教室名 in 教室表 not in （子查询）
    # 子查询：查询课程表里当前正在上课的课程的教室
    sql = ("SELECT * FROM room WHERE location = '{}' AND type = '{}'AND classroom NOT IN "
           "(SELECT classroom FROM sc WHERE academic_year='{}' AND semester='{}' AND course_weekday='{}' AND course_time IN ({}))").format(
        location, type, academic_year, semester, current_weekday, course_time_str)
    cursor.execute(sql)
    results = cursor.fetchall()
    results = results[(page - 1) * 10: page * 10]   # 分页

    response_data = {}
    data = {}
    if len(results) > 0:
        # 加key
        keys = ['id', 'classroom', 'location', 'floor', 'type', 'description']
        results = [dict(zip(keys, row)) for row in results]
        print(results)

        response_data['state'] = 'success'
        response_data['message'] = '查询成功'
        total_results = len(results)
        data['results'] = results
        data['total_results'] = total_results
        data['page'] = page
        response_data['data'] = data

        return jsonify(response_data)

    else:
        response_data['state'] = 'fail'
        response_data['message'] = '查询失败'
        data = None
        response_data['data'] = data
        return jsonify(response_data)

