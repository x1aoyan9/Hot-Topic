from flask import session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_app.models.topic import Topic

class Response:
    db = "hot_topic"
    def __init__(self,data):
        self.id = data['id']
        self.choice = data['choice']
        self.user_id = session['user_id']
        self.topic_id = data['topic_id']

#Adds the voting choice to the responses table
    @classmethod
    def submit_choice(cls,data):
        query = 'INSERT INTO responses (choice, user_id, topic_id) VALUES (%(choice)s, %(user_id)s, %(topic_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_vote(topic):
        array = []
        results = Topic.get_all_responses(topic)
        is_valid = True
        for row in results:
            array.append(row)
        for i in array:
            if i['user_id'] == session['user_id']:
                is_valid = False
        print(array)
        return is_valid