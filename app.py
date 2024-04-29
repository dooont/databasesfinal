from flask import Flask, redirect, render_template, request, session, url_for
import pymysql.cursors
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'whatever_you_want'

# Handles GET form submission at the root URL
@app.route('/', methods=['GET'])
def index():
    # date1 = request.args.get('date1')
    # date2 = request.args.get('date2')

    # Implement any actual logic you need here
    return render_template('index.html')


# Handles POST form submission
@app.route('/customer-login', methods=['POST'])
def customerLoginPost():
    # data1 = request.form.get('data1')
    # data2 = request.form.get('data2')
    # data = {
    #     'data1': data1,
    #     'data2': data2
    # }

    # Any actual logic that you want to implement

    return render_template('customer_login.html')


@app.route('/staff-login', methods=['POST'])
def staffLoginPost():
    # data1 = request.form.get('data1')
    # data2 = request.form.get('data2')
    # data = {
    #     'data1': data1,
    #     'data2': data2
    # }

    # Any actual logic that you want to implement

    return render_template('staff_login.html')

@app.route('/customer-register', methods=['GET'])
def customerRegister():
    # date1 = request.args.get('date1')
    # date2 = request.args.get('date2')

    # Any actual logic that you want to implement
    return render_template('customer-register.html')

@app.route('/staff-register', methods=['GET'])
def staffRegister():
    # date1 = request.args.get('date1')
    # date2 = request.args.get('date2')

    # Any actual logic that you want to implement

    return render_template('staff-register.html')

@app.route('/login', methods=['POST'])
def loginPost():
    # Verify username and password here
    session['logged_in'] = True
    return redirect(url_for('protected'))

# Basic protected route example
@app.route('/protected', methods=['GET'])
def protectedGet():
    if session.get('logged_in'):
        # let the user see the protected page
        return render_template('protected.html')
    else:
        # otherwise redirect to somewhere else
        return render_template('unauthorized.html')

 #search for future flights
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
    
#flights status
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


from functools import wraps


# # This is a decorator that will make the route only accessible to logged in users
# # Make sure to import functools
# def protected_route(route):
#     @wraps(route)
#     def wrapper(*args, **kwargs):
#         if session.get('logged_in'):
#             return route(*args, **kwargs) # Direct to the actual function implementation
#         else:
#             return render_template('unauthorized.html') # Redirect to unauthorized page or whatever of your choice
#     return wrapper

# # Works just like /protected, but using a decorator
# @app.route('/protected2', methods=['GET'])
# @protected_route
# def protected2():
#     return render_template('protected.html')
    
# Set the logged_in session variable to False
# The naming does not matter, whether it is logged_in or just username, it is just a key in the session dictionary
# Just make sure setting it to false or popping it from the session dictionary will let the current user not pass the protected route check anymore
# @app.route('/logout')
# def logout():
#     session['logged_in'] = False
#     return redirect(url_for('index'))

# @app.route('/')
# def index():
#     return render_template('api_demo.html')

if __name__ == '__main__':
    app.run(debug=True)

#customer queries/pages
#view my flights
@app.route('/change to correct page', methods=['GET', 'POST'])
def view_myflights():
	today = datetime.today().strftime('%Y-%m-%d')
	future_date = (datetime.today() + timedelta(days = 180)).strftime('%Y-%m-%d')

	start_date = request.form.get('start_date',today)
	end_date = request.form.get('end_date',future_date)

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
	depAirport = request.args.get('depAirport')
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
	flightNum = request.form['flightNum']
	price = request.form['price']
	customer_email = session['username']
	firstName = request.form['firstName']
	lastName = request.form['lastName']
	date_of_birth = request.form['date_of_birth']
	cardType = request.form['cardType']
	cardNum = request.form['cardNum']
	expirationDate = request.form['expirationDate']
	purchaseDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print((flightNum, customer_email, firstName, lastName, date_of_birth, cardType, cardNum, expirationDate, purchaseDate))
	
	cursor = conn.cursor()
	ins = '''INSERT INTO ticket (flight_id, customer_email, fname, lname, dob, price, card_type, card_num, exp_date, purchase_date) 
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

	cursor.execute(ins, (flightNum, customer_email, firstName, lastName, date_of_birth, price, cardType, cardNum, expirationDate, purchaseDate) )
	conn.commit()
	cursor.close()
	return render_template('checkout.html')

#define route for my flights
@app.route('/my_flights', methods=['GET', 'POST'])
def my_flights():
	return redirect(url_for('view_myflights')) 