from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
Bootstrap(app)

db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

#User login count
@app.route('/', methods=['GET', 'POST'])
def index():
    ip_add = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    cur = mysql.connection.cursor()
    resultvalue = cur.execute('SELECT * FROM ip WHERE ip_address = %s', [ip_add])
    if resultvalue > 0:
        get_ip_add = cur.fetchone()
        address = get_ip_add['ip_address']
        count = get_ip_add['visit_count'] + 1
        cur = mysql.connection.cursor()
        cur.execute("UPDATE ip SET visit_count = %s WHERE ip_address = %s", (count, address))
        mysql.connection.commit()
        cur.close()
        print('You have visited ' + str(count) + ' times to this page')
    else:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO ip (ip_address, visit_count) VALUES (%s, %s)', (ip_add, 1))
        mysql.connection.commit()
        cur.close()
        print('You visited first time to this page')

    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)



