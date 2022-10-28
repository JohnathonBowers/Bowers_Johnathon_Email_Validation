from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, db_data):
        self.id = db_data.get('id')
        self.first_name = db_data.get('first_name')
        self.last_name = db_data.get('last_name')
        self.email = db_data.get('email')
        self.created_at = db_data.get('created_at')
        self.updated_at = db_data.get('updated_at')

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 1:
            flash('First name must include one or more characters', 'first_name')
            is_valid = False
        if len(user['last_name']) < 1:
            flash('Last name must include one or more characters', 'last_name')
            is_valid = False
        if len(user['email']) < 1:
            flash('Email address must include one or more characters', 'email')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash ('Invalid email address', 'email')
            is_valid = False
        return is_valid
        

    @classmethod
    def add_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s)'
        return connectToMySQL('user_val_schema').query_db(query, data)

    @classmethod
    def get_all_users(cls):
        query = 'SELECT * FROM users ORDER BY last_name ASC;'
        results = connectToMySQL('user_val_schema').query_db(query)
        user_objects = []
        for db_row in results:
            user_objects.append(cls(db_row))
        return user_objects
