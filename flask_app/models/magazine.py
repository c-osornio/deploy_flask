from flask_app.config.mysqlconnection import connectToMySQL, MySQLConnection
from flask_app import app
from flask import flash, session
from flask_app.models import user


class Magazine:
    db = "belt_exam"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        self.user_ids_who_subscribed= []
        self.users_who_subscribed = []

# Create
    @classmethod
    def save(cls, data):
        if not cls.validate_magazine_data(data):
            return False
        query = """
        INSERT INTO magazines(title, description, user_id)
        VALUES (%(title)s, %(description)s, %(user_id)s)
        ; """
        magazine_id = connectToMySQL(cls.db).query_db(query, data)
        return magazine_id

# Read
    @classmethod 
    def get_all_magazines(cls):
        query = """
        SELECT *
        FROM magazines
        JOIN users
        ON magazines.user_id = users.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_magazines = []
        if not results:
            return results
        for row in results:
            magazine = cls(row)
            creator_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'birthday': row['birthday'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            creator = user.User(creator_data)
            magazine.creator = creator
            all_magazines.append(magazine)
        return all_magazines

    @classmethod
    def get_magazine_by_id(cls, id):
        data = {
            'id': id,
        }
        query = """
        SELECT *
        FROM magazines
        JOIN users
        ON magazines.user_id = users.id
        WHERE magazines.id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        magazine= cls(results[0])
        for row in results:
            creator_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'birthday': row['birthday'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            creator = user.User(creator_data)
            magazine.creator = creator
        return magazine

    @classmethod 
    def get_all(cls):
        query = """
        SELECT *
        FROM magazines
        JOIN users AS creators
        ON magazines.user_id = creators.id
        LEFT JOIN subscribers
        ON subscribers.magazine_id = magazines.id
        LEFT JOIN users AS users_who_subscribed
        ON subscribers.user_id = users_who_subscribed.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        magazines = []
        if not results:
            return results
        for row in results:
            new_magazine = True
            user_who_subscribed_data = {
                'id': row['users_who_subscribed.id'],
                'first_name': row['users_who_subscribed.first_name'],
                'last_name': row['users_who_subscribed.last_name'],
                'email': row['users_who_subscribed.email'],
                'password': row['users_who_subscribed.password'],
                'birthday': row['users_who_subscribed.birthday'],
                'created_at': row['users_who_subscribed.created_at'],
                'updated_at': row['users_who_subscribed.updated_at'],
            }
            number_of_magazines = len(magazines)
            if number_of_magazines > 0:
                last_magazine = magazines[number_of_magazines- 1]
                if last_magazine.id == row['id']:
                    last_magazine.user_ids_who_subscribed.append(row['users_who_subscribed.id'])
                    last_magazine.users_who_subscribed.append(user.User(user_who_subscribed_data))
                    new_magazine = False
            if new_magazine:
                magazine = cls(row)
                user_data = {
                    'id': row['creators.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'birthday': row['birthday'],
                    'created_at': row['creators.created_at'],
                    'updated_at': row['creators.updated_at'],
                }
                creator= user.User(user_data)
                magazine.creator = creator
                if row['users_who_subscribed.id']:
                    magazine.user_ids_who_subscribed.append(row['users_who_subscribed.id'])
                    magazine.users_who_subscribed.append(user.User(user_who_subscribed_data))
                magazines.append(magazine)
        return magazines

    @classmethod
    def getOne(cls, id):
        data = {
            'id': id,
        }
        query='''
        SELECT * 
        FROM magazines
        JOIN users AS creators 
        ON magazines.user_id=creators.id
        LEFT JOIN subscribers
        ON subscribers.magazine_id=magazines.id
        LEFT JOIN users AS users_who_subscribed
        ON subscribers.user_id = users_who_subscribed.id
        WHERE magazines.id = %(id)s
        ;'''
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        new_magazine = True
        for row in results:
            if new_magazine:
                magazine = cls(row)
                user_data = {
                    'id': row['creators.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'birthday': row['birthday'],
                    'created_at': row['creators.created_at'],
                    'updated_at': row['creators.updated_at'],
                }
                creator = user.User(user_data)
                magazine.creator = creator
                new_magazine = False
            if row['users_who_subscribed.id']:
                user_who_subscribed_data = {
                    'id': row['users_who_subscribed.id'],
                    'first_name': row['users_who_subscribed.first_name'],
                    'last_name': row['users_who_subscribed.last_name'],
                    'email': row['users_who_subscribed.email'],
                    'password': row['users_who_subscribed.password'],
                    'birthday': row['users_who_subscribed.birthday'],
                    'created_at': row['users_who_subscribed.created_at'],
                    'updated_at': row['users_who_subscribed.updated_at'],
                }
                user_who_subscribed = user.User(user_who_subscribed_data)
                magazine.users_who_subscribed.append(user_who_subscribed)
                magazine.user_ids_who_subscribed.append(row['users_who_subscribed.id'])
        return magazine

# Delete
    @classmethod
    def delete(cls, id):
        data = {
            'id': id,
        }
        query='''
        DELETE FROM magazines
        WHERE id= %(id)s
        ;'''
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def subscribe(cls, data):
        query='''
        INSERT INTO subscribers(user_id, magazine_id) 
        VALUES(%(user_id)s, %(id)s)
        ;'''
        return connectToMySQL(cls.db).query_db(query, data)

# Validate 
    @staticmethod
    def validate_magazine_data(data):
        is_valid = True
        if len(data['title']) < 2:
            flash("Your title must be at least two characters long.", "magazine")
            is_valid = False
        if len(data['description']) < 10:
            flash("Your description must be at least ten characters long.", "magazine")
            is_valid = False
        return is_valid