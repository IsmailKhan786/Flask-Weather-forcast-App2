from flask import Flask, render_template, request
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'weather'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    
    return render_template('index.html')
@app.route('/add',methods=['GET', 'POST'])
def add():
    return render_template('add.html')

@app.route('/savedetails', methods=['GET', 'POST'])
def savedetails():
    if request.method == "POST":
        details = request.form
        city = details['city']
        humidity = details['humidity']
        maxtemp = details['maxtemp']
        mintemp = details['mintemp']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO weather(city, humidity, maxtemp, mintemp) VALUES (%s, %s, %s, %s)", (city, humidity, maxtemp, mintemp))
        mysql.connection.commit()
        cur.close()
        return 'success'
@app.route('/view',methods=['GET', 'POST'])
def view():  
    cur1 = mysql.connection.cursor()
    sql = "SELECT city,humidity,maxtemp,mintemp FROM weather"
    cur1.execute(sql)
    rows = cur1.fetchall()
    cur1.close()
    return render_template('view.html', rows = rows)
@app.route("/viewcity")  
def viewcity():
        return render_template('viewcity.html')
    
@app.route('/viewbycity',methods=['GET', 'POST'])    
def viewbycity():  
    cur2 = mysql.connection.cursor()
    city = request.form['city']
    sql = "SELECT * FROM weather where city like %s"
    cur2.execute(sql,(city,))
     
    rows = cur2.fetchall()
    cur2.close()
    return render_template('viewbycity.html', rows = rows)

if __name__ == '__main__':
    app.run()