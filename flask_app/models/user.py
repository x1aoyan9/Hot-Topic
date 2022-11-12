from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash


class User:
    db = "DATABASE NAME HERE"
    def __init__(self, data):
        self.id = data['id']
        self.f_name = data['f_name']
        self.l_name = data['l_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.posts = []


# CREATE
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (f_name, l_name, email, password) VALUES (%(f_name)s, %(l_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)


# GET ALL
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        dict = []
        for row in results:
            dict.append(cls(row))
        return dict


# GET ONE BY EMAIL
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) <= 0:
            return False
        return cls(results[0])


# GET ONE BY ID
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])


# @classmethod
# def get_user_posts(cls, data):
#    query = left join between users and posts where post_id = posts.id


# @classmethod => might want to add some kind of warning/catch to confirm user wants to delete account
# def destroy_user(cls, data):
#    query = "SELECT * FROM users WHERE id = %(id)s;"
#    results = connectToMySQL(cls.db).query_db(query, data)
#    return cls(results[0])


    @staticmethod
    def valid_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email")
            is_valid = False
        if len(user['f_name']) < 2:
            flash("First name must be at least 2 characters")
            is_valid = False
        if len(user['l_name']) < 2:
            flash("Last name must be at least 2 characters")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        if user["password"] != user['confirm_password']:
            flash("Passwords do not match")
            is_valid = False
        return is_valid