from flask import Flask, redirect, render_template, request, session, url_for
from datetime import datetime, timedelta
from functools import wraps

import pymysql.cursors


app = Flask(__name__, static_folder="static")
app.secret_key = 'whatever_you_want'

def get_db_connection():
    # Here, replace the placeholders with your actual database connection details
    connection = pymysql.connect(host='localhost',
                                port=3306,
                                user='root',
                                password='password',
                                db='database_final',
                                cursorclass=pymysql.cursors.DictCursor)
    return connection

# main page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# redirect to customer login form
@app.route('/customer-login', methods=['GET'])
def customer_login():
    return render_template('customer_login.html')

# redirect to customer registration form
@app.route('/customer-register', methods=['GET'])
def customer_register():
    return render_template('customer_register.html')

# redirect to staff login
@app.route('/staff-login', methods=['GET'])
def staff_login():
    return render_template('staff_login.html')

# staff registration form
@app.route('/staff-register', methods=['GET'])
def staff_register():
    return render_template('staff_register.html')

# view all customers
@app.route('/customers', methods=['GET'])
def customers():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customer")
            customer_records = cursor.fetchall()
    finally:
        connection.close()
        
    return render_template('view_customers.html', customers=customer_records)

#view all flights
@app.route('/flights', methods=['GET'])
def flights():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM flight")
            flight_records = cursor.fetchall()
    finally:
        connection.close()
        
    return render_template('view_flights.html', flights=flight_records)

#filter flights
@app.route('/flights', methods=['POST'])
def filter_flights():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    source = request.form.get('source')
    destination = request.form.get('destination')
    
    if not start_date:
        start_date = '2020-01-01'  
    if not end_date:
        end_date = '2100-12-31' 
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM flight WHERE depAirport = %s AND arrAirport = %s AND depDate >= %s AND arrDate <= %s", (source, destination, start_date, end_date))
            flight_records = cursor.fetchall()
    finally:
        connection.close()
        
    return render_template('view_flights.html', flights=flight_records)

#staff login post
@app.route('/staff-login', methods=['POST'])
def staffLoginPost():
    username = request.form.get('username')
    password = request.form.get('password')
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM airlinestaff WHERE username = %s AND password = %s", (username, password))
            staff = cursor.fetchone()
    finally:
        connection.close()
    return render_template('staff_home.html', staff=staff)

#check for valid customer login
@app.route('/customer_login', methods=['POST'])
def customerLoginPost():
    username = request.form.get('username')
    password = request.form.get('password')
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customer WHERE username = %s AND password = %s", (username, password))
            customer = cursor.fetchone()
    finally:
        connection.close()
    return render_template('customer_home.html', customer=customer)

#view all airplanes
@app.route('/airplanes', methods=['GET'])
def airplanes():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM airplanes")
            airplane_records = cursor.fetchall()
    finally:
        connection.close()
        
    return render_template('view_airplanes.html', airplanes=airplane_records)

#redirect to add_airplane.html
@app.route('/add-airplane', methods=['GET'])
def add_airplane():
    return render_template('add_airplane.html')

#adding an airplane
@app.route('/add-airplane', methods=['POST'])
def add_airplane_post():
    airplane_id = request.form.get('airplane_id')
    airplane_name = request.form.get('airplane_name')
    airplane_type = request.form.get('airplane_type')
    airplane_capacity = request.form.get('airplane_capacity')
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO airplanes (airplane_id, airplane_name, airplane_type, airplane_capacity) VALUES (%s, %s, %s, %s)", (airplane_id, airplane_name, airplane_type, airplane_capacity))
            connection.commit()
    finally:
        connection.close()
    return redirect('/airplanes')


if __name__ == '__main__':
    app.run(debug=True)
