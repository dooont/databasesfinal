from flask import Flask, redirect, render_template, request, session, url_for
from datetime import datetime, timedelta
from functools import wraps

import pymysql.cursors

staffAirline = ''
staffUsername = ''
customerLogged = False
staffLogged = False

#if they logout, they shouldn't be able to go back
#implement as much logic as possible in the backend

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


#Customer Pages + What they can do ==========================================================================================
@app.route('/customer-login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM customer WHERE emailAddress = %s AND password = %s", (username, password))
                customer = cursor.fetchone()
                customerLogged = True
                print(customerLogged)
        finally:
            connection.close()
        return render_template('customer_home.html', customer=customer)
    else:
        return render_template('customer_login.html')

# redirect to customer registration form
@app.route('/customer-register', methods=['GET', 'POST'])
def customer_register():
    if request.method == 'POST':
        username = request.form.get('emailAddress')
        password = request.form.get('password')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        building_number = request.form.get('buildingNumber')
        street_name = request.form.get('streetName')
        apartment_number = request.form.get('apartmentNumber')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')
        passport_number = request.form.get('passport_number')
        passport_expiration = request.form.get('passport_expiration')
        passport_country = request.form.get('passport_country')
        date_of_birth = request.form.get('date_of_birth')
        phone_number = request.form.get("phoneNumber")

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                #fix query to be correct
                sql = "INSERT INTO customer (emailAddress, firstName, lastName, password, buildingNumber, streetName, apartmentNumber, city, state, zipCode, passport_number, passport_expiration, passport_country, date_of_birth) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (username, first_name, last_name, password, building_number, street_name, apartment_number, city, state, zip_code, passport_number, passport_expiration, passport_country, date_of_birth))
                cursor.execute("INSERT INTO customer_contact_info (emailAddress, phoneNumber) VALUES (%s, %s)", (username, phone_number))
                connection.commit()
        finally:
            connection.close()
        return redirect('/')
    else:
        return render_template('customer_register.html')    

@app.route('/customer-home', methods=['GET', 'POST'])
def customer_home():
    if customerLogged:
        return render_template('customer_home.html')
    else:
        return redirect('/')

@app.route('/flights', methods=['GET'])
def flightsCustomer():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM flight")
            flight_records = cursor.fetchall()
    finally:
        connection.close()
        
    return render_template('view_flights_customer.html', flights=flight_records)

#filter flights
@app.route('/flights', methods=['POST'])
def filter_flightsCustomer():
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
        
    return render_template('view_flights_customer.html', flights=flight_records)

#redirect to review flights form
@app.route('/ratings', methods=['GET'])
def customer_rating():
    return render_template('customer_rating.html')

#review flights post
@app.route('/ratings', methods=['POST'])
def customer_rating_post():
    email = request.form.get('Email')
    ticketID = request.form.get('ticketID')
    rating = request.form.get('Rating')
    comment = request.form.get('Comment')
    flightDate = request.form.get('flightDate')
    flightDateStr = datetime.strptime(flightDate, '%Y-%m-%d').date()
    tdyDate = datetime.now().date()
    connection = get_db_connection()
    
    if(flightDateStr>tdyDate): #if flight is in future
        connection.close()
        return redirect('/')
    
    else:
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO review (emailAddress, ticketID, Rating, Comment) VALUES (%s, %s, %s, %s)", (email, ticketID, rating, comment))
                connection.commit()
        finally:
            connection.close()
        return redirect('/')

#tracking spending
@app.route('/spending', methods=['GET', 'POST'])
def track_spending():
    name = request.form.get('name')
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT SUM(ticketPrice) FROM ticket where flightDepDate >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND nameOfHolder = %s", (name))
            result = cursor.fetchone()
            if result:
                total_past_year = result[0]
            else:
                total_past_year = 0
            
            monthly_spending_query = """
            SELECT YEAR(flightDepDate), MONTH(flightDepDate), SUM(ticketPrice)
            FROM ticket
            WHERE flightDepDate >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            AND nameOfHolder = %s
            GROUP BY YEAR(flightDepDate), MONTH(flightDepDate)
            ORDER BY YEAR(flightDepDate), MONTH(flightDepDate)
            """

            cursor.execute(monthly_spending_query,(name))
            monthly_data = cursor.fetchall()
            
            if request.method == 'POST':
                start_date = request.form['start_date']
                end_date = request.form['end_date']
                cursor.execute("SELECT SUM(ticketPrice) FROM Ticket WHERE flightDepDate BETWEEN %s AND %s", (start_date, end_date))
                range_total = cursor.fetchone()[0] or 0
                monthly_range_query = """
                SELECT YEAR(flightDepDate), MONTH(flightDepDate), SUM(ticketPrice)
                FROM Ticket
                WHERE flightDepDate BETWEEN %s AND %s
                AND nameOfHolder = %s
                GROUP BY YEAR(flightDepDate), MONTH(flightDepDate)
                ORDER BY YEAR(flightDepDate), MONTH(flightDepDate)
                """
                cursor.execute(monthly_range_query, (start_date, end_date, name))
                range_monthly_data = cursor.fetchall()
                #connection.commit()
                return render_template('spending.html', total_past_year=total_past_year, monthly_data=monthly_data, range_total=range_total, range_monthly_data=range_monthly_data)
            
        
    finally:
        connection.close()
    
    return render_template('spending.html', total_past_year=total_past_year, monthly_data=monthly_data, range_total=None, range_monthly_data=None)

#Staff Pages + What they can do =========================================================================================

# redirect to staff login
@app.route('/staff-login', methods=['GET'])
def staff_login():
    return render_template('staff_login.html')

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
    staffLogged = True
    return render_template('staff_home.html', staff=staff)

# staff registration form
@app.route('/staff-register', methods=['GET'])
def staff_register():
    return render_template('staff_register.html')

# staff registration post
@app.route('/staff-register', methods=['POST'])
def customer_register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    date_of_birth = request.form.get('dob')
    airline_name = request.form.get('airline-name')
    emailAddress = request.form.get('email-address')
    phoneNumber = request.form.get('phone-number')

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            #fix query to be correct
            cursor.execute("INSERT INTO airlinestaff (Username, Password, first_name, last_name, DOB, Airline_Name) VALUES (%s, %s, %s, %s, %s, %s)", (username, password, first_name, last_name, date_of_birth, airline_name))
            cursor.execute("INSERT INTO airlinestaff_email(Username, emailAddress) VALUES (%s, %s)", (username, emailAddress))
            cursor.execute("INSERT INTO airlinestaff_phone(Username, Phone_number) VALUES (%s, %s)", (username, phoneNumber))
            connection.commit()
    finally:
        connection.close()
    return redirect('/')

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
@app.route('/flights-staff', methods=['GET'])
def flightsStaff():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM flight")
            flight_records = cursor.fetchall()
    finally:
        connection.close()
        
    return render_template('view_flights_staff.html', flights=flight_records)

#filter flights
@app.route('/flights', methods=['POST'])
def filter_flights():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    source = request.form.get('source')
    destination = request.form.get('arr_Airport')
    
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
        
    return render_template('view_flights.html', flights=flight_records)    # 

#staff-home app route
@app.route('/staff-home', methods=['GET', 'POST'])
def staff_home():
    if staffLogged:
        return render_template('staff_home.html')
    else:
        return redirect('/')

@app.route('/add-airplane', methods=['GET', 'POST'])
def addAirplane():
    if request.method == 'POST':
        airplane_id = request.form.get('airplane_id')
        manufacturing_company = request.form.get('manufacturing_company')
        manufacturing_date = request.form.get('manufacturing_date')
        NumberOfSeats = request.form.get('number_of_seats')
        model_number = request.form.get('model_number')
        AirlineName = request.form.get('airline_name')
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO airplanes (ID, ManufacturingCompany, ManufacturingDate, NumberOfSeats, ModelNumber, AirlineName) VALUES (%s, %s, %s, %s, %s, %s)", (airplane_id, manufacturing_company, manufacturing_date, NumberOfSeats, model_number, AirlineName))
                connection.commit()
        finally:
            connection.close()
        return redirect('/airplanes')
    else:
        return render_template('add_airplane.html')#view airports route
    
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

#add-airport route
@app.route('/add-airport', methods=['GET', 'POST'])
def addAirport():
    if request.method == 'POST':
        airport_id = request.form.get('airport_id')
        airport_name = request.form.get('airport_name')
        airport_type = request.form.get('airport_type')
        airport_city = request.form.get('airport_city')
        airport_country = request.form.get('airport_country')
        terminal = request.form.get('terminal')
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO airport (Code, Name, AirportType, City, Country, Terminals) VALUES (%s, %s, %s, %s, %s, %s)", (airport_id, airport_name, airport_type, airport_city, airport_country, terminal))
                connection.commit()
        finally:
            connection.close()
        return redirect('/airports')
    else:
        return render_template('add_airport.html')
    
@app.route('/airplanes', methods=['GET', 'POST'])
def airplanes():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM airplanes")
            airplane_records = cursor.fetchall()
    finally:
        connection.close()
        
    return render_template('view_airplanes.html', airplanes=airplane_records)

#change flight status
@app.route('/change-flight-status', methods=['GET', 'POST'])
def changeFlightStatus():
    if request.method == 'POST':
        flight_id = request.form.get('flight_id')
        status = request.form.get('new_status')


        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE flight SET status = %s WHERE flightNum = %s", (status, flight_id))
                connection.commit()
        finally:
            connection.close()
        return redirect('/flights')
    else:
        return render_template('change_status.html')

#create flight route
@app.route('/create-flight', methods=['GET', 'POST'])
def createFlight():
    if request.method == 'POST':
        airline = request.form.get('airline')
        flight_id = request.form.get('flight_number')
        airplane_id = request.form.get('aircraft_id')
        dep_airport = request.form.get('departure_airport')
        arr_airport = request.form.get('arrival_airport')
        dep_date = request.form.get('departure_date')
        dep_time = request.form.get('departure_time')
        arr_date = request.form.get('arrival_date')
        arr_time = request.form.get('arrival_time')
        price = request.form.get('price')
        status = "on-time"
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO flight (Name, flightNum, depAirport, arrAirport, depDate, depTime, arrDate, arrTime, ID, basePrice, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (airline, flight_id, dep_airport, arr_airport, dep_date, dep_time, arr_date, arr_time, airplane_id, price, status))
                connection.commit()
        finally:
            connection.close()
        return redirect('/flights')
    else:
        return render_template('create_flight.html')

#maintenance route
@app.route('/view-maintenance', methods=['GET', 'POST'])
def view_maintenance():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM maintenance")
            maintenance_records = cursor.fetchall()
    finally:
        connection.close()
        
    return render_template('view_maintenance.html', mains=maintenance_records)

#schedule maintenance route
@app.route('/schedule-maintenance', methods=['GET', 'POST'])
def scheduleMaintenance():
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        start_time = request.form.get('start_time')
        end_date = request.form.get('end_date')
        end_time = request.form.get('end_time')
        airplane_id = request.form.get('airplane_id')
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO maintenance (Start_Date, Start_Time, End_Date, End_Time, AirplaneID) VALUES (%s, %s, %s, %s, %s)", (start_date, start_time, end_date, end_time, airplane_id))
                connection.commit()
        finally:
            connection.close()
        return redirect('/view-maintenance')
    else:
        return render_template('schedule_maintenance.html')

#Both Staff and Customer =========================================================================================

#logout app route
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    customerLogged = False
    staffLogged = False
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)