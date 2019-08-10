import datetime

from database import open_db_connection
import json


# if EXISTS (select * from users where username like 'jindal') BEGIN  select * from users where  name like 'shivam' and username like 'goel' END ELSE BEGIN INSERT INTO USERS(name, username) values('shwetha', 'jindal') END

# def generate_user_insert_query(user_json):
#     return "insert into users(name, username, created_on, modified_on) values('" + user_json[] + "' )"

def generate_query(query_type, table, fields, values):
    if query_type == "insert":
        return "insert into " + table + "(" + ",".join(fields) + ") values('" + "','".join(values) + "')"
    if query_type == "select":
        return "select * from " + table + " where " + fields[0] + " like '" + values[0] + "'"


def login_user(user_json):
    with open_db_connection() as cursor:
        row = cursor.execute('select * from users where username like ? and password like ?', user_json["username"],
                             user_json["password"]).fetchone()
        if row is None:
            return json.dumps({
                "error": "Invalid username or password"
            }), 400
        else:
            return json.dumps({
                "name": row["name"],
                "username": row["username"]
            }), 200


def signup_user(user_json):
    with open_db_connection() as cursor:
        row = cursor.execute("If EXISTS (" + generate_query("select", "users", ["username"], [user_json["username"]]) +
                             ")BEGIN" + generate_query("select", "users", ["username"], [user_json["username"]]) +
                             "END ELSE BEGIN" + generate_query("insert", "users",
                                                               ["name", "username", "password", "created_on",
                                                                "modified_on"],
                                                               [user_json["name"], user_json["username"],
                                                                user_json["password"], datetime.datetime.now(),
                                                                datetime.datetime.now()]) + "END")
        # fetchone means the query that ran is of select which means the user exist
        if "fetchone" in row:
            return json.dumps({
                "error": "A user already exist with same username"
            }), 400
        else:
            del user_json["password"]
            return json.dumps(user_json), 200


def is_user_present(username):
    with open_db_connection() as cursor:
        cursor.execute('select name from users where username like ?', username)
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True
