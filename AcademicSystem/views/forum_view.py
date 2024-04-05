import json
from datetime import datetime

from flask import request, Blueprint, jsonify

from flask_cors import CORS
from config import cursor, conn


# 创建蓝图
forum_bp = Blueprint('forum', __name__)

cors = CORS(forum_bp, resources={r"/*": {"origins": "*"}})


# 判断是否点赞 帖子或评论
def iflike(sno, kind, results):
    for result in results:
        if kind == '帖子':
            target_id = result['qid']
        else:
            target_id = result['aid']

        sql = "SELECT * FROM `like` WHERE sno = %s AND kind = %s AND qidOrAid = %s"
        cursor.execute(sql, (sno, kind, target_id))
        liked_item = cursor.fetchone()
        if liked_item is not None:
            result['status'] = '已点赞'
        else:
            result['status'] = '未点赞'
    return results


# 论坛模块 --> 首页
@forum_bp.route("/forum/main/<page>", methods=['POST'])
def forum_main(page):
    page = int(page)
    data = request.get_json()
    sno = data.get('sno')

    sql = "SELECT * FROM question ORDER BY create_time DESC"
    cursor.execute(sql, )
    conn.commit()
    results = cursor.fetchall()
    total_result = len(results)  # 帖子数量
    results = results[(page - 1) * 10: page * 10]
    print(results)

    # return jsonify(results)

    response_data = {}
    if len(results) > 0:
        keys = ['qid', 'sno', 'sname', 'title', 'content', 'create_time', 'answer_count', 'like_count']
        results = [dict(zip(keys, row)) for row in results]

        # 判断帖子是否被sno点赞
        results = iflike(sno, '帖子', results)

        # 格式化create_time字段
        for result in results:
            if result['create_time'] is not None:
                result['create_time'] = result['create_time'].strftime('%Y-%m-%d %H:%M:%S')
            else:
                result['create_time'] = 'null'

        response_data['state'] = 'success'
        response_data['message'] = '查找成功'

        # "data"字段
        data = {}
        data['page'] = page
        data['total_result'] = total_result
        data['results'] = results
        response_data['data'] = data
        return response_data

    else:
        response_data['state'] = 'fail'
        response_data['message'] = '没有帖子'
        response_data['data'] = None
        return jsonify(response_data)


# 论坛模块 --> 搜索帖子
@forum_bp.route("/search/forum/<page>", methods=['POST'])
def search_forum(page):
    page = int(page)
    data = request.get_json()
    searchword = data['searchword']
    sno = data['sno']

    response_data = {}
    search_query = "SELECT * FROM question WHERE title LIKE %s OR content LIKE %s "
    wildcard_searchword = '%' + searchword + '%'
    cursor.execute(search_query,
                   (wildcard_searchword, wildcard_searchword))
    results = cursor.fetchall()
    total_result = len(results)
    results = results[(page - 1) * 10: page * 10]

    if results is None or len(results) == 0:
        response_data['state'] = 'fail'
        response_data['message'] = '未找到符合条件帖子'
        response_data['data'] = None
        return jsonify(response_data)
    else:
        keys = ['qid', 'sno', 'sname', 'title', 'content', 'create_time', 'answer_count', 'like_count']
        results = [dict(zip(keys, row)) for row in results]

        # 格式化create_time字段
        for result in results:
            if result['create_time'] is not None:
                result['create_time'] = result['create_time'].strftime('%Y-%m-%d %H:%M:%S')
            else:
                result['create_time'] = 'null'

        # 判断帖子是否被sno点赞
        results = iflike(sno, '帖子', results)

        response_data['state'] = 'success'
        response_data['message'] = '查找成功'

        # "data"字段
        data = {}
        data['page'] = page
        data['total_result'] = total_result
        data['results'] = results
        response_data['data'] = data
        return jsonify(response_data)


# 论坛模块 --> 发布帖子
@forum_bp.route("/question/add", methods=['POST'])
def add_question():
    data = request.get_json()
    sno = data.get('sno')
    title = data.get('title')
    content = data.get('content')
    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 查询发布用户的用户名
    sql_sname = "SELECT sname FROM student WHERE sno = %s"
    cursor.execute(sql_sname, (sno,))
    result = cursor.fetchone()
    if not result:
        return jsonify({'state': 'fail', 'message': '发布失败！未找到该用户'})

    sname = result[0]

    # 插入帖子信息
    sql_insert = "INSERT INTO question (sno, sname, title, content, create_time) VALUES (%s, %s, %s, %s, %s)"
    values = (sno, sname, title, content, create_time)

    try:
        cursor.execute(sql_insert, values)
        conn.commit()
        response_data = {'state': 'success', 'message': '帖子发布成功'}
    except Exception as e:
        conn.rollback()  # 回滚事务
        response_data = {'state': 'fail', 'message': f'帖子发布失败！ Error: {str(e)}'}

    return jsonify(response_data)


# 论坛模块 --> 发布评论
@forum_bp.route('/answer/add', methods=['POST'])
def add_answer():
    data = request.get_json()
    qid = data.get('qid')
    sno = data.get('sno')
    content = data.get('content')
    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 查询发布用户的用户名
    sql_sname = "SELECT sname FROM student WHERE sno = %s"
    cursor.execute(sql_sname, (sno,))
    result = cursor.fetchone()
    if not result:
        return jsonify({'state': 'fail', 'message': '评论发布失败！未找到该用户'})

    sname = result[0]

    # 插入评论信息
    sql_insert = "INSERT INTO answer (qid, sno, sname, content, create_time) VALUES (%s, %s, %s, %s, %s)"
    values = (qid, sno, sname, content, create_time)

    # 更新帖子的评论数量
    sql_update = "UPDATE question SET answer_count = answer_count + 1 WHERE qid = %s"
    qid_value = (qid,)

    try:
        cursor.execute(sql_insert, values)
        cursor.execute(sql_update, qid_value)
        conn.commit()
        response_data = {'state': 'success', 'message': '评论发布成功'}
    except Exception as e:
        conn.rollback()  # 回滚事务
        response_data = {'state': 'fail', 'message': f'评论发布失败！ Error: {str(e)}'}

    return jsonify(response_data)


# 论坛模块 --> 帖子详情
@forum_bp.route("/forum/detail", methods=['POST'])
def forum_detail():
    data = request.get_json()
    qid = data.get('qid')
    sno = data.get('sno')

    # 检查参数是否完整
    if not qid or not sno:
        return jsonify({'state': 'fail', 'message': '参数不完整'})

    # 查询帖子信息
    sql_question = "SELECT * FROM question WHERE qid = %s"
    cursor.execute(sql_question, (qid,))
    question = cursor.fetchone()
    if not question:
        return jsonify({'state': 'fail', 'message': '该帖子不存在'})

    data = {}
    # 将查询结果转换为字典形式，并格式化时间字段
    question_keys = ['qid', 'sno', 'sname', 'title', 'content', 'create_time', 'answer_count', 'like_count']
    question_dict = dict(zip(question_keys, question))
    question_dict['create_time'] = question_dict['create_time'].strftime('%Y-%m-%d %H:%M:%S')

    # 判断帖子是否被点赞
    sql_like = "SELECT * FROM `like` WHERE sno = %s AND kind = %s AND qidOrAid = %s"
    cursor.execute(sql_like, (sno, '帖子', qid))
    liked_item = cursor.fetchone()
    question_dict['status'] = '已点赞' if liked_item else '未点赞'
    data['question'] = question_dict

    # 查询帖子的评论信息
    sql_answers = "SELECT * FROM answer WHERE qid = %s"
    cursor.execute(sql_answers, (qid,))
    answers = cursor.fetchall()

    if answers:
        # 将查询结果转换为字典形式，并格式化时间字段
        answer_keys = ['aid', 'sno', 'sname', 'title', 'content', 'create_time', 'like_count']
        answers = [dict(zip(answer_keys, row)) for row in answers]
        for answer in answers:
            answer['create_time'] = answer['create_time'].strftime('%Y-%m-%d %H:%M:%S') if answer[
                'create_time'] else None

        # 判断评论是否被点赞
        answers = iflike(sno, '评论', answers)
        data['answer'] = answers

    response_data = {
        'state': 'success',
        'message': '查找成功',
        'data': data
    }

    return jsonify(response_data)


# 论坛模块 --> 点赞（帖子 or 评论）
@forum_bp.route('/forum/like', methods=['POST'])
def forum_like():
    data = request.get_json()
    sno = data['sno']
    kind = data['kind']  # '帖子' or '评论'
    qidOrAid = data['qidOrAid']  # 帖子或评论对应的id

    if kind not in ['帖子', '评论']:
        response_data = {'state': 'fail', 'message': 'kind 参数错误'}
        return jsonify(response_data)

    try:
        # 检查是否已经点赞过
        sql_check = "SELECT COUNT(*) FROM `like` WHERE sno = %s AND qidOrAid = %s AND kind = %s"
        cursor.execute(sql_check, (sno, qidOrAid, kind))
        result = cursor.fetchone()
        if result[0] > 0:
            response_data = {'state': 'fail', 'message': '请勿重复点赞'}
            return jsonify(response_data)

        if kind == '帖子':
            sql1 = "INSERT INTO `like` (sno, qidOrAid, kind) VALUES (%s, %s, %s)"
            sql2 = "UPDATE question SET like_count = like_count + 1 WHERE qid = %s"
        elif kind == '评论':
            sql1 = "INSERT INTO `like` (sno, qidOrAid, kind) VALUES (%s, %s, %s)"
            sql2 = "UPDATE answer SET like_count = like_count + 1 WHERE aid = %s"

        # 插入记录
        cursor.execute(sql1, (sno, qidOrAid, kind))
        conn.commit()

        # 更新点赞数
        cursor.execute(sql2, (qidOrAid,))
        conn.commit()

        response_data = {'state': 'success', 'message': '点赞成功'}
    except Exception as e:
        response_data = {'state': 'fail', 'message': f'点赞失败 Error: {str(e)}'}

    return jsonify(response_data)


# 论坛模块 --> 取消点赞
@forum_bp.route('/forum/dislike', methods=['POST'])
def forum_dislike():
    data = request.get_json()
    sno = data['sno']
    kind = data['kind']  # '帖子' or '评论'
    qidOrAid = data['qidOrAid']  # 帖子或评论对应的id

    if kind not in ['帖子', '评论']:
        response_data = {'state': 'fail', 'message': 'kind 参数错误'}
        return jsonify(response_data)

    try:
        sql1 = "DELETE FROM `like` WHERE sno = %s AND qidOrAid = %s AND kind = %s"
        cursor.execute(sql1, (sno, qidOrAid, kind))
        conn.commit()

        if kind == '帖子':
            sql2 = "UPDATE question SET like_count = like_count - 1 WHERE qid = %s"
        elif kind == '评论':
            sql2 = "UPDATE answer SET like_count = like_count - 1 WHERE aid = %s"

        cursor.execute(sql2, (qidOrAid,))
        conn.commit()

        response_data = {'state': 'success', 'message': '取消点赞成功'}
    except Exception as e:
        response_data = {'state': 'fail', 'message': f'取消点赞失败 Error: {str(e)}'}

    return jsonify(response_data)
