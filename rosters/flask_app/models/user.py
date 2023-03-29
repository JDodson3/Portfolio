from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app import bcrypt
from flask_app.models import player

class User:
    db = "rosters"
    def __init__(self,db_data):
        self.id = db_data['id']
        self.team_name = db_data['team_name']
        self.first_name = db_data['first_name']
        self.last_name = db_data['last_name']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.players = []

    @classmethod
    def getOne(cls,data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def getEmail(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def save(cls,form_data):
        hashed_data = {
            'team_name': form_data['team_name'],
            'first_name': form_data['first_name'],
            'last_name': form_data['last_name'],
            'email': form_data['email'],
            'password': bcrypt.generate_password_hash(form_data['password']),
        }
        query = 'INSERT INTO users (team_name, first_name, last_name, email, password) VALUES (%(team_name)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL(cls.db).query_db(query,hashed_data)

    @classmethod
    def update(cls,data):
        query = 'UPDATE user SET team_name=%(team_name)s, first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = 'DELETE FROM users WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_reg(form_data):
        isValid = True
        if len(form_data['email']) < 1:
            isValid = False
            flash("Email cannot be empty.", "register")
        elif not EMAIL_REGEX.match(form_data['email']):
            isValid = False
            flash("Invalid email format", "register")
        elif User.getEmail(form_data):
            isValid = False
            flash("A user already exists for that email.", "register")
        if len(form_data['team_name']) < 2:
            isValid = False
            flash("Team Name must have at least 2 characters")
        if len(form_data['first_name']) < 2:
            isValid = False
            flash("First Name must have at least 2 characters")
        if len(form_data['last_name']) < 2:
            isValid = False
            flash("Last Name must have at least 2 characters")
        if len(form_data['password']) < 8:
            isValid = False
            flash("Password must have at least 8 characters")
        if form_data['password'] != form_data['confirm']:
            isValid = False
            flash("Passwords are not matching", "register")
        return isValid

    @staticmethod
    def validate_login(form_data):
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email/password.","login")
            return False

        user = User.getEmail(form_data)
        if not user:
            flash("Invalid email/password.","login")
            return False
        
        if not bcrypt.check_password_hash(user.password, form_data['password']):
            flash("Invalid email/password.","login")
            return False
        
        return user

    
    @classmethod
    def get_one_with_players(cls, data ):
        query = "SELECT * FROM users LEFT JOIN players on users.id = players.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL('rosters').query_db(query,data)
        print(results)
        user = cls(results[0])
        for row in results:
            n = {
                'id': row['team.id'],
        'team_name': row['team_name'],
        'first_name': row['first_name'],
        'last_name': row['last_name'],
        'height': row['height'],
        'weight': row['weight'],
        'grade': row['grade'],
        'points_game': row['points_game'],
        'rebounds_game': row['rebounds_game'],
        'assists_game': row['assists_game'],
        'blocks_game': row['blocks_game'],
        'steals_game': row['steals_game'],
        'bio': row['bio'],
        'created_at': row['team.created_at'],
        'updated_at': row['team.updated_at'],
        'user_id': row['user_id']
            }
            user.players.append( Player(n) )
        return user
