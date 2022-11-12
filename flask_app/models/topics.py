from flask import session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Topic: 
    db = "hot_topic"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.question = data['question']
        self.choice1 = data['choice1']
        self.choice2 = data['choice2']
        self.choice3 = data['choice3']
        self.choice4 = data['choice4']
        self.choice5 = data['choice5']
        self.user_id = session['user_id']
        #blank creator to append and display with the get all class method
        self.creator = None

#CREATES NEW TOPIC
    @classmethod
    def create_topic(cls,data):
        query = 'INSERT INTO topics (title, question, choice1, choice2, choice3, choice4, choice5, created_at, updated_at, user_id) VALUES (%(title)s, %(question)s, %(choice1)s, %(choice2)s, %(choice3)s, %(choice4)s, %(choice5)s, NOW(), NOW(), %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

#Gets an array of all topics with an accessible creator for each to pull info from
    @classmethod
    def get_topics_with_creator(cls):
        query = 'SELECT * FROM topics JOIN users ON topics.user_id = users.id;'
        results = connectToMySQL(cls.db).query_db(query)
        all_topics = []
        for row in results:
            one_topic = cls(row)
            one_topic_creator_info = {
                'id' : row['users.id'],
                'f_name' : row['f_name'],
                'l_name' : row['l_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            one_topic.creator = User(one_topic_creator_info)
            all_topics.append(one_topic)
        return all_topics

#Gets all of the logged in user's topics
    @classmethod
    def get_topics_by_user(cls,data):
        query = 'SELECT * FROM topics LEFT JOIN users ON topics.user_id = users.id WHERE users.id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

#Gets one topic using data = {'id' : topic_id} in the controller route
    @classmethod
    def get_one_topic(cls,data):
        query = 'SELECT * FROM topics JOIN users ON topics.user_id = users.id WHERE topics.id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

#Delete method using data = {'id' : topic_id} in the controller route
    @classmethod
    def delete_topic(cls, data):
        query = 'DELETE FROM topics WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

#Update topic, uses form from updateForm.html
    @classmethod
    def update_topic(cls,data):
        query = 'UPDATE topics SET title=%(title)s, question=%(question)s, choice1=%(choice1)s, choice2=%(choice2)s, choice3=%(choice3)s, choice4=%(choice4)s, choice5=%(choice5)s WHERE id=%(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

#Simple front end validation
    @staticmethod
    def validate_topic(topic):
        is_valid = True
        if len(topic['title']) < 1:
            flash('Please enter a title', 'topic_validation')
            is_valid = False
        if len(topic['question']) < 1:
            flash('Please enter a proper question', 'topic_validation')
            is_valid = False
        if len(topic['choice1']) < 1 or len(topic['choice2']) < 1:
            flash('Must provide at least a first and second choice', 'topic_validation')
            is_valid = False
        return is_valid