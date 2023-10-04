from flask_app.config.mysqlconnection import connectToMySQL

from flask_app import DATABASE, BCRYPT

import re

from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save_user(cls, form): #NEEDS TO BE FORM SINCE DATA= REQUEST.FORM = IMMUTABLE.
        hashed_pw = BCRYPT.generate_password_hash(form['password'])
        data ={
            **form,
            'password': hashed_pw
        }
        query = """INSERT INTO users(first_name, last_name, password, email)
        VALUES(%(first_name)s, %(last_name)s, %(password)s, %(email)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_email(cls,email):
        data = {
            'email': email
        }
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def validate_login(cls, form):
        is_valid = True
        found_user = cls.get_by_email(form['email'])
#THIS IS FOR WHEN THERE IS NO MATCH TO USER EMAIL IN DB; USER NOT FOUND. MADE FLASH MSG NOT SO OBVIOUS WHAT WAS WRONG FOR AN EXTRA LAYER OF PROTECTION.
        if not found_user:
            flash("Invalid Login!", "login")
            return False
#THIS IS WHAT COMPARES THE PASSWORD FROM FOUND USER WITH PASSWORD THAT IS SUPPLIED FROM THE FORM.
        else:
            if not BCRYPT.check_password_hash(found_user.password, form['password']):
                flash("Invalid Login!","login")
                return False
        return found_user

    @classmethod
    def get_by_id(cls, data):
        query = """SELECT * FROM users WHERE id = %(id)s"""
        results= connectToMySQL(DATABASE).query_db(query, data)
        return cls(results[0])

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = """SELECT * FROM users WHERE email = %(email)s;"""
        results= connectToMySQL(DATABASE).query_db(query, user)
        if len(results) >= 1:
            flash("Email is already taken, please use Login.", "register")
            is_valid= False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters", "register")
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters", "register")
            is_valid= False
        if not EMAIL_REGEX.match(user['email']):#THIS CHECKS THE EMAILS FORMATTING.
            flash("Invalid Email!!!")
            is_valid=False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid= False
        if user['password'] != user['confirm_password']: 
            flash("Passwords don't match", "register") 
            is_valid=False 
        return is_valid