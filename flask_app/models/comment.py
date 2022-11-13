from flask import session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.topic import Topic

class Comment:
    db = 'hot_topic'
    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.topic_id = data['topic_id']
        self.user_id = session['user_id']
        #Empty creator to pull information with get comments method
        self.creator = None
    
#Classic create method
    @classmethod
    def add_comment(cls, data):
        query = 'INSERT INTO comments (comment, topic_id, user_id, created_at, updated_at) VALUES (%(comment)s, %(topic_id)s, %(user_id)s, NOW(),NOW());'
        return connectToMySQL(cls.db).query_db(query, data)

#Gets all comments on a route, using data = {'id': topic_id} in controller route
    @classmethod
    def get_comments(cls, data):
        query = 'SELECT * FROM comments LEFT JOIN topics ON topics.id = comments.topic_id WHERE topics.id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_comment(comment):
        is_valid = True
        if len(comment['comment']) < 1:
            flash('Please enter a comment', 'comment_validation')
            is_valid = False
        return is_valid
