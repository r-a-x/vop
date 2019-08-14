from database import open_db_connection
import json


def is_user_present(username):
    with open_db_connection() as cursor:
        cursor.execute('select name from users where username like ?', username)
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True


def generate_query(query_type, table, fields, values):
    values = [str(x) for x in values]
    print(values)
    query = None
    if query_type == "insert":
        query = "insert into " + table + "(" + ",".join(fields) + ") values('" + "','".join(values) + "')"
    if query_type == "select":
        query = "select * from " + table + " where " + fields[0] + " like '" + values[0] + "'"
    print query
    return query


def login_user(user_json):
    with open_db_connection() as cursor:
        row = cursor.execute('select username, name from users where username like ? and password like ?', user_json["username"],
                             user_json["password"]).fetchone()
        if row is None:
            raise InvalidLoginDetailsException()
        else:
            return{
                "name": row[1],
                "username": row[0]
            }, 200


def signup_user(user_json):
    with open_db_connection(True) as cursor:
        query = "If EXISTS ( " + generate_query("select", "users", ["username"], [user_json["username"]]) +" )BEGIN " + generate_query("select", "users", ["username"], [user_json["username"]]) + " END ELSE BEGIN " + generate_query("insert", "users",["name", "username", "password"],[user_json["name"], user_json["username"], user_json["password"]]) + " END"
        print query
        row = cursor.execute(query)
        if row.rowcount == -1:
            raise UserAlreadyExistException()
        else:
            del user_json["password"]
            return user_json, 200


class InvalidLoginDetailsException(Exception):
    code = 401
    name = "InvalidLoginDetailsException"
    message = "Invalid username and password"


class UserAlreadyExistException(Exception):
    code = 422
    name = "UserAlreadyExistException"
    message = "User with the username already exists"


class UserNotFoundException(Exception):
    code = 403
    name = "UserNotFoundException"
    message = "Please signup before proceeding"
