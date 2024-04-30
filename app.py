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
                                db='final_database',
                                cursorclass=pymysql.cursors.DictCursor)
    return connection

# main page
@app.route('/', methods=['GET', 'POST'])
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

# customer registration post
@app.route('/customer-register', methods=['POST'])
def customer_register_post():
    username = request.form.get('email')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    building_number = request.form.get('building_number')
    street_name = request.form.get('street_name')
    apartment_number = request.form.get('apartment_number')
    city = request.form.get('city')
    state = request.form.get('state')
    zip_code = request.form.get('zip_code')
    passport_number = request.form.get('passport_number')
    passport_expiration = request.form.get('passport_expiration')
    passport_country = request.form.get('passport_country')
    date_of_birth = request.form.get('date_of_birth')

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            #fix query to be correct
            cursor.execute("INSERT INTO customer (username, password, first_name, last_name, building_number, street_name, apartment_number, city, state, zip_code, passport_number, passport_expiration, passport_country, date_of_birth) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, password, first_name, last_name, building_number, street_name, apartment_number, city, state, zip_code, passport_number, passport_expiration, passport_country, date_of_birth))
            connection.commit()
    finally:
        connection.close()
    return redirect('/')

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



#staff-home app route
@app.route('/staff-home', methods=['GET', 'POST'])
def staff_home():
    return render_template('staff_home.html')

#logout app route
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect('/')

#customer-home app route
@app.route('/customer-home', methods=['GET', 'POST'])
def customer_home():
    return render_template('customer_home.html')

#add-airplane route
@app.route('/add-airplane', methods=['GET', 'POST'])
def addAirplane():
    if request.method == 'POST':
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
    else:
        return render_template('add_airplane.html')

#add-airport route
@app.route('/add-airport', methods=['GET', 'POST'])
def addAirport():
    if request.method == 'POST':
        airport_id = request.form.get('airport_id')
        airport_name = request.form.get('airport_name')
        airport_city = request.form.get('airport_city')
        airport_country = request.form.get('airport_country')
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO airport (airport_id, airport_name, airport_city, airport_country) VALUES (%s, %s, %s, %s)", (airport_id, airport_name, airport_city, airport_country))
                connection.commit()
        finally:
            connection.close()
        return redirect('/airports')
    else:
        return render_template('add_airport.html')
    
#view airports route
@app.route('/airports', methods=['GET'])
def airports():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM airport")
            airport_records = cursor.fetchall()
    finally:
        connection.close()
        
    return render_template('view_airports.html', airports=airport_records)

if __name__ == '__main__':
    app.run(debug=True)
