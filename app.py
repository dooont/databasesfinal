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

# Basic protected route example
@app.route('/protected', methods=['GET'])
def protectedGet():
    if session.get('logged_in'):
        # let the user see the protected page
        return render_template('protected.html')
    else:
        # otherwise redirect to somewhere else
        return render_template('unauthorized.html')

# search for future flights
@app.route('/search', methods=['GET', 'POST'])
def search():
    depAirport = request.form.get('depAirport')
    arrAirport = request.form.get('arrAirport')
    depDate = request.form.get('depDate')
    arrDate = request.form.get('arrDate', None)
    
    try:
        cursor = conn.cursor()
        query1 = """
            SELECT AirlineName, flight.ID, depDate, depTime, arrDate, arrTime
            FROM flight, airplane 
            WHERE flight.ID = airplane.ID 
            AND depAirport = %s 
            AND arrAirport = %s 
            AND depDate = %s;"""
        cursor.execute(query1, (depAirport, arrAirport, depDate))
        data1 = cursor.fetchall()

        if arrDate:
            query2 = """
                SELECT flight.ID, depDate, depTime, arrDate, arrTime, AirlineName
                FROM flight, airplane 
                WHERE flight.ID = airplane.ID 
                AND depAirport = %s 
                AND arrAirport = %s 
                AND depDate = %s;"""
            cursor.execute(query2, (arrAirport, depAirport, arrDate))
            data2 = cursor.fetchall()
            cursor.close()
            return render_template('index.html', depAirport=depAirport, arrAirport=arrAirport, depDate=depDate, 
                                arrDate=arrDate, flights=data1, flights2=data2)
        else:
            cursor.close()
            return render_template('index.html', depAirport=depAirport, arrAirport=arrAirport, depDate=depDate, 
                                arrDate=arrDate, flights=data1)
    except Exception as e:
        print(e)  # or log to a file/appropriate logging mechanism
        cursor.close()
        return "An error occurred during the flight search"
    
# flights status
@app.route('/flight_status',methods=['GET','POST'])
def flight_status():
    # grabs information from the forms
    depAirport = request.form.get('depAirport',None)
    arrAirport = request.form.get('arrAirport',None)
    depDate = request.form.get('depDate',None)
    arrDate = request.form.get('arrDate',None)

    cursor = conn.cursor()
    query = '''
            SELECT AirlineName, flight.ID, depDate, depTime, arrDate,arrTime, status 
            FROM flight, airplanes 
            WHERE flight.ID = airplanes.ID 
            AND dep_airport = %s 
            AND arr_airport = %s 
            AND dep_date = %s;'''
            
    cursor.execute(query, (depAirport, arrAirport, depDate)) #
    data = cursor.fetchall() 
    cursor.close()
    return render_template('flight_status.html', flights=data)

#customer queries
#view my flights
@app.route('/change to correct page', methods=['GET', 'POST'])
@app.route('/change to correct page', methods=['GET', 'POST'])
def view_myflights():
    today = datetime.today().strftime('%Y-%m-%d')
    future_date = (datetime.today() + timedelta(days = 180)).strftime('%Y-%m-%d')

    start_date = request.form.get('start_date', today)
    end_date = request.form.get('end_date', future_date)

    cursor = conn.cursor()
    query = '''
    SELECT  ticketID, flight.ID, depDate, depTime, arrDate, arrTime, status
    FROM flight INNER JOIN ticket
    where customer_email = %s
    and ticket.flightID = flight.ID
    and depDate between %s and %s;

    '''
    #ticket.flightID and flight.ID both refer to the ID of the airplane
    #check line where customer_email=%s. Does not seem it will work. Check for a way around. Maybe use customer name
    cursor.execute(query, (session.get('username'),start_date, end_date))
    data = cursor.fetchall() 
    cursor.close()
    return render_template('myflight.html', username = session['username'], flights=data)

#book a flight
@app.route('/change to correct page', methods=['GET', 'POST'])
def get_flights():
    depAirport = request.args.get('depAirport') #args.get is to filter results
    arrAirport = request.args.get('arrAirport')
    depDate = request.args.get('depDate')
    arrDate = request.args.get('arrDate',None)
    print(arrDate)

    cursor = conn.cursor()
    query1 = '''
            SELECT  flightNum, depDate, depTime, arrDate,arrTime, AirlineName
            FROM flight, airplanes
            WHERE flight.ID = airplanes.ID 
            AND dep_airport = %s 
            AND arr_airport = %s 
            AND dep_date = %s;'''    
    cursor.execute(query1, (depAirport, arrAirport, depDate)) 
    data1 = cursor.fetchall()
    
    
    if arrDate and arrDate != '':
        query2 = '''
        SELECT  flightNum, depDate, depTime, arrDate, arrTime, AirlineName
        FROM flight, airplane 
        WHERE flight.ID = airplanes.ID 
        AND depAirport = %s 
        AND arrAirport = %s 
        AND depDate = %s;'''
        cursor.execute(query2, (arrAirport, depAirport , arrDate)) 
        data2 = cursor.fetchall()
        cursor.close()
        return render_template('book_ticket.html', depAirport=depAirport, arrAirport=arrAirport, depDate=depDate, 
                            arrDate=arrDate, flights=data1, flights2=data2, username=session['username'])

    else: 
        cursor.close()
        return render_template('book_ticket.html', depAirport=depAirport, arrAirport=arrAirport, depDate=depDate, 
                            arrDate=arrDate, flights=data1, username=session['username'])

#book button
@app.route('/change to correct page', methods=['GET', 'POST'])
def book_clicked():
    flightNum = request.args.get('flightNum')

    cursor = conn.cursor()
    query = '''SELECT 
                CASE
                    WHEN (COUNT(ticket.ticketID) / seats) >= 0.8 THEN 1.25 * basePrice
                    ELSE basePrice
                END AS price
            FROM flight
            INNER JOIN airplane ON flight.ID = airplanes.ID
            LEFT JOIN ticket ON flight.ID = ticket.flightID
            WHERE flight.ID = %s 
            GROUP BY flight.ID;'''
    cursor.execute(query, (flightNum))
    data = cursor.fetchall() 
    price = int(data[0].get('price', None))

    conn.commit()
    cursor.close()

    return render_template('checkout.html',flightNum = flightNum, price = price)

#after selecting ticket
@app.route('/change to correct page', methods=['GET', 'POST'])
def checkout():
    ticketID = request.form['ticketID']
    flightName = request.form['flightName']
    flightNum = request.form['flightNum']
    flightDepDate = request.form['flightDepDate']
    flightDepTime = request.form['flightDepTime']
    flightID= request.form['flightID']
    price = request.form['price']
    customerEmail = session['username']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    fullName = "{} {}".format(firstName, lastName)
    cardType = request.form['cardType']
    cardNum = request.form['cardNum']
    expirationDate = request.form['expirationDate']
    purchaseDate = datetime.now().strftime('%Y-%m-%d')
    purchaseTime = datetime.now().strftime('%H:%M:%S')
    #print((flightNum, customer_email, firstName, lastName, date_of_birth, cardType, cardNum, expirationDate, purchaseDate))
    
    cursor = conn.cursor()
    ins = '''INSERT INTO ticket (ticketID, flightName, flightNum, flightDepDate, flightDepTime, flightID, ticketPrice, cardNum, cardType, nameOfHolder, exp_date) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        INSERT INTO purchases(customerEmail,flightName, flightNum, flightDepDate, flightDepTime, flightID, PurchaseTime, PurchaseDate)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
    
    cursor.execute(ins, (ticketID, flightName, flightNum, flightDepDate, flightDepTime, flightID, price, cardNum, cardType, fullName, expirationDate, customerEmail, flightName, flightNum, flightDepDate, flightDepTime, flightID, purchaseTime, purchaseDate) )
    conn.commit()
    cursor.close()
    return render_template('checkout.html')

#define route for my flights
@app.route('/my_flights', methods=['GET', 'POST'])
def my_flights():
    return redirect(url_for('view_myflights'))

#staff queries and all
#view flights
@app.route('/change to correct name', methods=['GET', 'POST'])
def view_flights():
    today = datetime.today().strftime('%Y-%m-%d')
    future_date = (datetime.today() + timedelta(days=30)).strftime('%Y-%m-%d')

    depAirport = request.form.get('depAirport')
    arrAirport = request.form.get('arrAirport')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date') 

    if not start_date:
        start_date = today

    if not end_date:
        end_date = future_date

    cursor = conn.cursor()
    query = '''
        SELECT  flighID, depDate, depTime, arrDate, arrTime, status, AirlineName
        FROM flight
        INNER JOIN airplane ON flight.ID = airplanes.ID
        WHERE AirlineName IN (
            SELECT airline_Name 
            FROM airlinestaff
            WHERE username = %s and
            dep_date BETWEEN %s AND %s
        )
    '''
    params = (session.get('username'),start_date, end_date,)

    if depAirport and arrAirport :
        query += 'AND depAirport = %s AND arrAirport = %s;'
        params += (depAirport, arrAirport)
    else:
        query += ';'

    cursor.execute(query, params)

    data = cursor.fetchall() 
    cursor.close()
    return render_template('staff_dashboard.html', username = session['username'], airlineName = session['airlineName'], flights=data)

#view customers of a particular flight
@app.route('/change to correct name', methods=['GET', 'POST'])
def view_customers():
    flightNum = request.args.get('flightNum')

    cursor = conn.cursor()

    query = """SELECT nameOfHolder FROM ticket 
                WHERE flightNum = %s;"""
    
    cursor.execute(query, (flightNum))
    customers = cursor.fetchall()

    cursor.close()
    return render_template('view_customers.html', customers=customers)

#view airplanes
@app.route('/change to correct name', methods=['GET', 'POST'])
def view_airplanes():
    
    cursor = conn.cursor()
    query = '''
        SELECT ID, ManufacturingCompany, ManufacturingDate, NumberOfSeats, ModelNumber
        FROM airplane
        WHERE AirlineName IN (
            SELECT Airline_Name 
            FROM airlinestaff
            WHERE username = %s
        );
    '''
    cursor.execute(query, session['username'])

    data = cursor.fetchall() 
    cursor.close()
    return render_template('view_airplanes.html', username = session['username'], airplanes=data)

if __name__ == '__main__':
    app.run(debug=True)
