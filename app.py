from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml
#import json, time
from datetime import date

app = Flask(__name__)
Bootstrap(app)

db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    current_date = str(date.today())
    ip_add = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    cur = mysql.connection.cursor()
    resultvalue = cur.execute('SELECT * FROM ip WHERE ip_address = %s', [ip_add])
    if resultvalue > 0:
        get_ip_add = cur.fetchone()
        address = get_ip_add['ip_address']
        count = get_ip_add['visit_count'] + 1
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO ip(ip_address, visit_count, date) VALUES (%s, %s, %s)", (address, count, current_date))
        mysql.connection.commit()
        cur.close()
        print('Date: ' + str(current_date) +
              'ip: ' + address +
              'count: ' + str(count))
    else:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO ip(ip_address, visit_count, date) VALUES (%s, %s)', (ip_add, 1, current_date))
        mysql.connection.commit()
        cur.close()
        print('Date: ' + str(current_date) +
              'ip: ' + ip_add +
              'count: ' + 1)

    return render_template('base.html')

#@app.route('/time/')
#def time():
#    data_set = {'Visiter ID': user_id, 'No of visits' : visit_count, 'Date' : time.time() }
#    json_dump = json.dumps(data_set)

#    return json_dump

if __name__ == '__main__':
    app.run(debug=True)



