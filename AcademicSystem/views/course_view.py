from flask import request, Blueprint, jsonify
from flask_cors import CORS

from config import cursor, conn

from datetime import datetime

# 创建蓝图
course_bp = Blueprint('course', __name__)

# 跨域请求
cors = CORS(course_bp, resources={r"/*": {"origins": "*"}})


# 选课模块 --> 查课 --> 构建查询条件
def get_conditions(data):
    # 构建查询条件
    conditions = []
    if 'cno' in data and data['cno']:   # 课程编号
        conditions.append("cno='{}'".format(data['cno']))
    if 'cname' in data and data['cname']:   # 课程名字
        conditions.append("cname='{}'".format(data['cname']))
    if 'credit' in data and data['credit']:     # 课程学分
        conditions.append("credit >= {}".format(data['credit']))
    if 'course_weekday' in data and data['course_weekday']:     # 上课时间  -- 星期几
        conditions.append("course_weekday='{}'".format(data['course_weekday']))
    if 'course_time' in data and data['course_time']:     # 上课时间  -- 第几节
        conditions.append("course_time='{}'".format(data['course_time']))
    if 'dept' in data and data['dept']:     # 开课学院
        conditions.append("dept='{}'".format(data['dept']))
    if 'type' in data and data['type']:     # 课程类别
        conditions.append("type='{}'".format(data['type']))
    if 'location' in data and data['location']:     # 上课校区
        conditions.append("location='{}'".format(data['location']))
    return conditions


# 选课模块--> 查课 --> 判断课程是否已选
def if_select(sno, results):
    for result in results:
        cno = result['cno']
        sql = "SELECT * FROM sc WHERE cno = '{}' AND sno = '{}'".format(cno, sno)
        cursor.execute(sql)
        course = cursor.fetchone()
        if course is not None:
            result['status'] = '已选'
        else:
            result['status'] = '未选'
    return results


# 选课模块 --> 查课 --> 分页功能
def paging(page, results, sno, total_result):
    response_data = {}
    # 加key
    # print(results)
    keys = ['id', 'cno', 'cname', 'credit', 'course_weekday', 'course_time', 'tname', 'dept', 'grade',
            'semester', 'type', 'classroom', 'location', 'floor', 'description', 'capacity', 'enrolled_student']
    results = [dict(zip(keys, row)) for row in results]
    # print(results)
    # 判断课程 '已选' or '未选'
    results = if_select(sno, results)
    response_data['state'] = 'success'
    response_data['message'] = '查找成功'

    # "data"字段
    data = {}
    data['page'] = page
    data['total_result'] = total_result
    data['results'] = results
    response_data['data'] = data
    return response_data


# 选课模块  --> 按筛选条件查课
@course_bp.route('/select/course/<page>', methods=['POST'])
def select_course(page):
    data = request.get_json()
    sno = data['sno']   # 学号
    page = int(page)

    # 构建查询条件
    conditions = []
    conditions = get_conditions(data)
    print("conditions:", conditions)

    response_data = {}
    if not conditions:
        response_data['state'] = 'fail'
        response_data['message'] = '请输入至少一个查询条件'
        response_data['data'] = None
        return jsonify(response_data)
    else:
        # 查表
        sql = "select * from course where " + " AND ".join(conditions)
        cursor.execute(sql,)
        conn.commit()
        results = cursor.fetchall()
        total_result = len(results)     # 满足条件的课程总数
        results = results[(page-1)*10: page*10]
        print(results)

        if len(results) > 0:
            response_data = paging(page, results, sno, total_result)
            print(response_data)
            return jsonify(response_data)   #

        else:
            response_data['state'] = 'fail'
            response_data['message'] = '未找到符合条件的课程'
            response_data['data'] = None
            return jsonify(response_data)


# 选课模块  -->  按搜索框查课
@course_bp.route('/search/course/<page>', methods=['POST'])
def search_cource(page):
    """
        搜索词信息:
        课程名cname、课程类型type、上课时间--星期几course_weekday、开课学院dept、教师姓名tname、上课校区location, 课程描述description
    """
    data = request.get_json()
    sno = data['sno']   # 学号
    page = int(page)    # 页码
    searchword = data['searchword']     # 搜索框是否为空由前端判断

    response_data = {}
    search_query = "SELECT * FROM course WHERE cname LIKE %s OR type LIKE %s OR course_weekday LIKE %s OR dept LIKE %s OR tname LIKE %s OR location LIKE %s OR description LIKE %s"
    wildcard_searchword = '%' + searchword + '%'
    cursor.execute(search_query,
                   (wildcard_searchword, wildcard_searchword, wildcard_searchword, wildcard_searchword, wildcard_searchword, wildcard_searchword, wildcard_searchword))
    results = cursor.fetchall()
    total_result = len(results)
    results = results[(page - 1) * 10: page * 10]

    if results is None or len(results) == 0:
        response_data['state'] = 'fail'
        response_data['message'] = '未找到符合条件的课程'
        response_data['data'] = None
        return jsonify(response_data)
    else:
        response_data = paging(page, results, sno, total_result)

        return jsonify(response_data)


# 选课模块  -->  选课
@course_bp.route('/add/course', methods=['POST'])
def add_course():
    # 获取信息
    data = request.get_json()
    sno = data['sno']
    cno = data['cno']
    cname = data['cname']
    tname = data['tname']
    credit = data['credit']
    type = data['type']
    course_weekday = data['course_weekday']
    course_time = data['course_time']
    classroom = data['classroom']

    # 判断是否已选
    response_data = {'state': 'success', 'message': ''}
    sql = "SELECT * FROM SC WHERE sno ='{}' AND cno ='{}'".format(sno, cno)
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) > 0:
        response_data['state'] = 'fail'
        response_data['message'] = '该门课已选'
        return jsonify(response_data)

    # 判断选修本门课的时间
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    if current_month > 8:
        academic_year = str(current_year) + '-' + str(current_year+1)
        semester = '1'
    else:
        academic_year = str(current_year-1) + '-' + str(current_year)
        semester = '2'

    # 插入数据
    sql = ("INSERT INTO sc (sno, cno, cname, tname, credit, academic_year, semester, type,course_weekday, course_time, classroom) "
           "VALUES ('{}', '{}','{}', '{}','{}', '{}','{}','{}','{}', '{}', '{}')").format(
        sno, cno, cname, tname, credit, academic_year, semester, type, course_weekday, course_time, classroom)
    try:
        # 插入记录
        cursor.execute(sql)
        conn.commit()
        response_data = {'state': 'success', 'message': '选课成功'}
    except Exception as e:
        response_data = {'state': 'fail', 'message': f'选课失败！ Error: {str(e)}'}
    return jsonify(response_data)


# 选课模块  -->  退课
@course_bp.route('/delete/course', methods=['POST'])
def delete_course():
    # 获取信息
    data = request.get_json()
    sno = data['sno']
    cno = data['cno']

    # 退课
    sql = ("DELETE FROM SC WHERE sno='{}' AND cno='{}' ").format(sno, cno)
    try:
        # 删除记录
        cursor.execute(sql)
        conn.commit()
        response_data = {'state': 'success', 'message': '退课成功'}
    except Exception as e:
        response_data = {'state': 'fail', 'message': f'退课失败！ Error: {str(e)}'}
    return jsonify(response_data)
