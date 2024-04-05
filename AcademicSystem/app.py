
from flask import Flask


from views.course_view import course_bp
from views.curriculum_view import curriculum_bp
from views.room_view import room_bp
from views.score_view import score_bp
from views.user_view import user_bp
from views.forum_view import forum_bp

app = Flask(__name__)

app.register_blueprint(user_bp)
app.register_blueprint(course_bp)
app.register_blueprint(score_bp)
app.register_blueprint(room_bp)
app.register_blueprint(curriculum_bp)
app.register_blueprint(forum_bp)


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='10.130.191.161')

