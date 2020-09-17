# Import Flask modules

from flask import Flask, render_template, request
from flaskext.mysql import MySQL

# Create an object named app

app = Flask(__name__)

# Configure mysql database

app.config['MYSQL_DATABASE_HOST'] = 'call-mysql-db-server.cbanmzptkrzf.us-east-1.rds.amazonaws.com'
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Clarusway_1'
app.config['MYSQL_DATABASE_DB'] = 'clarusway'
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()

# Create users table within MySQL db and populate with sample data
# Execute the code below only once.
# Write sql code for initializing users table..

drop_table = 'DROP TABLE IF EXISTS users;'
users_table = """
CREATE TABLE users (
  username varchar(50) NOT NULL,
  email varchar(50),
  PRIMARY KEY (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""
data = """
INSERT INTO clarusway.users 
VALUES 
    ("ahmet", "john@clarusway.com" ),
    ("mehmet", "mike@clarusway.com"),
    ("ali", "tom@clarusway.com"),
    ("ayse", "tom@clarusway.com"),
	("zeynep", "tom@clarusway.com");
"""
cursor.execute(drop_table)
cursor.execute(users_table)
cursor.execute(data)
# cursor.close()
# connection.close()

# Write a function named `find_emails` which find emails using keyword from the user table in the db,
# and returns result as tuples `(name, email)`.

def find_emails(keyword):
    query = f"""
    SELECT * FROM users WHERE username like '%{keyword}%';
    """
    cursor.execute(query)
    result = cursor.fetchall()
    user_emails = [(row[0], row[1]) for row in result]
    # if there is no user with given name in the db, then give warning
    if not any(user_emails):
        user_emails = [('Not found.', 'Not Found.')]
    return user_emails

# Write a function named `emails` which finds email addresses by keyword using `GET` and `POST` methods,
# using template files named `emails.html` given under `templates` folder
# and assign to the static route of ('/')

@app.route('/', methods=['GET', 'POST'])
def emails():
    if request.method == 'POST':
        user_name = request.form['username']
        user_emails = find_emails(user_name)
        return render_template('emails.html', name_emails=user_emails, keyword=user_name, show_result=True)
    else:
        return render_template('emails.html', show_result=False)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)