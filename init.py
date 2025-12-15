#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
from datetime import datetime, timedelta

import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)
# Lets Flask connect the CSS to the HTML 
app.static_folder = 'static'

#Configure MySQL. For mine port is 3306 and no password 
conn = pymysql.connect(host='localhost',
					   port = 3306,
                       user='root',
                       password='jiahaoma2000',
                       db='Airline_SystemV2',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route for home page
@app.route('/')
def home():
	return render_template('index.html')

#Define route for customer login
@app.route('/customer_login')
def customer_login():
	return render_template('customer_login.html')

#Define route for customer register
@app.route('/customer_register')
def customer_register():
	return render_template('customer_register.html')

#Define route for staff login
@app.route('/staff_login')
def staff_login():
	return render_template('staff_login.html')

#Define route for staff register
@app.route('/staff_register')
def staff_register():
	return render_template('staff_register.html')

#Authenticates the login for Customers 
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE email = %s and the_password = %s'
	cursor.execute(query, (email, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['email'] = email

		#ADD RESULT OF QUERY THAT RETURNS ALL PURCHASED FLIGHTS
		#-> done so already in /customer_home

		session['first_name'] = data['first_name'] 
		return redirect('/customer_home')
		#return render_template('customer)
	else:
		#returns an error message to the html page
		error = 'Invalid login information'
		return render_template('customer_login.html', error=error)

#Authenticates the registration for Customers
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	building_num = request.form['building_num']
	street = request.form['street']
	apt_num = request.form['apt_num']
	city = request.form['city']
	the_state = request.form['state']
	zip_code = request.form['zip-code']
	passport_num = request.form['pass_num']
	passport_expiration = request.form['pass_exp']
	pass_country = request.form['pass_country']
	dob = request.form['dob']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('customer_register.html', error = error)
	else:
		ins = 'INSERT INTO Customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (email, password, first_name, last_name, building_num, street, apt_num, city, the_state, zip_code, passport_num, passport_expiration, pass_country, dob))
		conn.commit()
		cursor.close()
		return render_template('index.html')
	
#Define route for customer home
@app.route('/customer_home')
def customer_home():
    if 'email' in session:
        email = session['email']
        first_name = session['first_name']  # Retrieve the first name from the session
        
        # Fetch customer's flights that they already bought 
        cursor = conn.cursor()
        query = '''
            SELECT t.ticket_id, f.airline_name, f.flight_number, f.depart_date, f.depart_time, f.depart_airport, f.arrival_airport
            FROM Ticket t
            JOIN Purchases p ON t.ticket_id = p.ticket_id
            JOIN Flight f ON t.airline_name = f.airline_name AND t.flight_number = f.flight_number AND t.depart_date = f.depart_date AND t.depart_time = f.depart_time
            WHERE p.email = %s AND (f.depart_date > CURDATE() OR (f.depart_date = CURDATE() AND f.depart_time > CURTIME()))
            ORDER BY f.depart_date ASC
        '''
        cursor.execute(query, (email))
        flights = cursor.fetchall()
        cursor.close()
        
        # Get error message from session if exists
        error = session.pop('error', None)
        
        return render_template('customer_home.html', first_name=first_name, flights=flights, error=error)
    else:
        return redirect('/customer_login')

#Authenticates the login for Staff
@app.route('/loginAuthStaff', methods=['GET', 'POST'])
def loginAuthStaff():
	#grabs information from the forms
	username = request.form.get('username')
	password = request.form.get('password')

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Airline_Staff WHERE username = %s and the_password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		# stores airline where staff works at 
		session['airline_name'] = data['airline_name']
		session['first_name'] = data['first_name'] 
		return render_template('staff_home.html', first_name=data['first_name'])
	else:
		#returns an error message to the html page
		error = 'Invalid login information'
		return render_template('staff_login.html', error=error)

#Authenticates the registration for Customers
@app.route('/registerAuthStaff', methods=['GET', 'POST'])
def registerAuthStaff():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	dob = request.form['dob']
	airline_name = request.form['airline_name']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('staff_register.html', error = error)
	else:
		ins = 'INSERT INTO airline_staff VALUES(%s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (username, password, first_name, last_name, dob, airline_name))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/flights', methods=['GET', 'POST'])
def flights():
	selected = request.form.get('flight_type')
	source = request.form['source']
	destination = request.form['destination']
	depart_date = request.form['departure_date']
	return_date = request.form.get('return_date')

	#convert from string to date type
	depart_dated = datetime.strptime(depart_date, '%Y-%m-%d').date()

	cursor = conn.cursor()

	leaving = '''SELECT *
				 FROM flight 
				 WHERE depart_date = %s AND (depart_date > CURDATE() OR (depart_date = CURDATE() AND depart_time > CURTIME())) AND 
				 depart_airport = %s AND arrival_airport = %s'''

	cursor.execute(leaving, (depart_dated, source, destination))
		
	#look for all future flights with specified time and airports
	leaving_data = cursor.fetchall()

	#one way trip chosen
	if selected == 'one-way':

		cursor.close()

		#if there are returned results
		if leaving_data:
			return render_template('flights.html', flights = leaving_data, trip = "one-way")
		
		#if there are no results
		else:
			none_found = "No Available Flights Found."
			return render_template('flights.html', nothing = none_found)
	
	#round trip chosen
	else:
		# Check if return_date is provided
		if not return_date:
			cursor.close()
			none_found = "Please provide a return date for round trip flights."
			return render_template('flights.html', nothing = none_found)
		
		return_dated = datetime.strptime(return_date, '%Y-%m-%d').date()

		#return flight is after departure flight - check for future flights only
		# Return flight should depart from destination and arrive at source (flipped)
		returning = '''SELECT *
					   FROM flight 
					   WHERE depart_date = %s 
					   AND (depart_date > CURDATE() OR (depart_date = CURDATE() AND depart_time > CURTIME()))
					   AND depart_airport = %s AND arrival_airport = %s'''

		#source and destination flipped for return flight
		cursor.execute(returning, (return_dated, destination, source))

		returning_data = cursor.fetchall()

		cursor.close()

		round_trips = []
		
		#compare each going flight with each return flight to check if compatible
		for i in leaving_data:
			for j in returning_data:
				#edge case: if same day round trip, but departure time of return flight is earlier than arrival time of going flight
				if (i['arrival_date'] == j['depart_date']) and (i['arrival_time'] >= j['depart_time']):
					pass
				#if same day round trip, but departure time of return flight is after arrival time of going flight
				elif (i['arrival_date'] == j['depart_date']) and (i['arrival_time'] < j['depart_time']):
					round_trips.append((i, j))
				#if return flight occurs after arrival of going flight
				elif i['arrival_date'] < j['depart_date']:
					round_trips.append((i, j))
				
		#since leaving_data only contains dates > CURDATE(), there will never be an instance where i[arrival_date] < j[departdate] if we choose departdate to be < CURDATE()
		if not round_trips:
			none_found = "No Available Flights Found!"
			return render_template('flights.html', nothing = none_found)
		
		return render_template('flights.html', flights = round_trips, trip = "round-trip")


@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
	# Check if user is logged in
	if 'email' not in session:
		return redirect('/customer_login')

	flight_type = request.args.get('flight_type')
	if not flight_type:
		return redirect('/customer_home')
		
	session['flight_type'] = flight_type

	if flight_type == 'one-way':
		airline_name = request.args.get('airline_name')
		airplane_name = request.args.get('airplane_name')
		flight_num = request.args.get('flight_number')
		airplane_id = request.args.get('airplane_id')
		depart_date = request.args.get('depart_date')
		depart_time = request.args.get('depart_time')

		#persistent data for multiple ticket purchases of a flight
		session['airline_name'] = airline_name
		session['flight_num'] = flight_num
		session['depart_date'] = depart_date
		session['depart_time'] = depart_time

	else:
		departing_airline_name = request.args.get('departing_airline_name')
		departing_airplane_name = request.args.get('departing_airplane_name')
		departing_flight_num = request.args.get('departing_flight_number')
		departing_airplane_id = request.args.get('departing_airplane_id')
		departing_depart_date = request.args.get('departing_depart_date')
		departing_depart_time = request.args.get('departing_depart_time')

		returning_airline_name = request.args.get('returning_airline_name')
		returning_airplane_name = request.args.get('returning_airplane_name')
		returning_flight_num = request.args.get('returning_flight_number')
		returning_airplane_id = request.args.get('returning_airplane_id')
		returning_depart_date = request.args.get('returning_depart_date')
		returning_depart_time = request.args.get('returning_depart_time')

		#persistent data for multiple ticket purchases of a flight
		session['departing_airline_name'] = departing_airline_name
		session['departing_flight_num'] = departing_flight_num
		session['departing_depart_date'] = departing_depart_date
		session['departing_depart_time'] = departing_depart_time
	
		session['returning_airline_name'] = returning_airline_name
		session['returning_flight_num'] = returning_flight_num
		session['returning_depart_date'] = returning_depart_date
		session['returning_depart_time'] = returning_depart_time

 
	cursor = conn.cursor()

	#find number of tickets reserved for a specific flight
	num_reserved = '''SELECT COUNT(ticket_id) as reserved
					 FROM ticket
					 WHERE ticket.flight_number = %s AND
					 ticket.depart_date = %s AND
					 ticket.depart_time = %s AND
					 ticket.airline_name = %s'''
	
	#find total seats for a specific flight
	num_seats ='''SELECT seats 
                  FROM airplane JOIN flight ON airplane.airline_name = flight.airline_name AND airplane.airplane_id = flight.airplane_id
                  WHERE airplane.airline_name = %s AND
                  airplane.airplane_id = %s AND
                  flight.flight_number = %s AND
                  flight.depart_date = %s AND
                  flight.depart_time = %s'''
	
	#obtain base price
	find_base = '''SELECT base_price
				   FROM flight
				   WHERE airline_name = %s AND
				   flight_number = %s AND
				   depart_date = %s AND
				   depart_time = %s'''
	
	#one way trip
	if flight_type == 'one-way':
		#find number of tickets reserved for a specific flight
		cursor.execute(num_reserved, (flight_num, depart_date, depart_time, airline_name))
		res = cursor.fetchone()
		reserved = res['reserved']
		#find total seats for a specific flight
		cursor.execute(num_seats, (airline_name, airplane_id, flight_num, depart_date, depart_time))
		seats = cursor.fetchall()
		flight_seats = seats[0]['seats']

		#flight percent capacity filled 
		if flight_seats == 0:
			cursor.close()
			session['error'] = "Flight has no available seats."
			return redirect('/customer_home')
		
		capacity_filled = reserved / flight_seats
		session['capacity_filled'] = capacity_filled

		#obtain base price
		cursor.execute(find_base, (airline_name, flight_num, depart_date, depart_time))
		price = cursor.fetchall()
		base_price = price[0]['base_price']

		# if capacity is greater than 80%, increase price by 25%
		if capacity_filled > 0.8:
			base_price *= 1.25

		session['ticket_price'] = base_price

	
	#round trip
	else:
		#DEPARTURE FLIGHT
		#find number of tickets reserved for a specific flight
		cursor.execute(num_reserved, (departing_flight_num, departing_depart_date, departing_depart_time, departing_airline_name))
		depart_res = cursor.fetchone()
		depart_reserved = depart_res['reserved']
		#print(f"reserved: {depart_reserved}")

		#find total seats for a specific flight
		cursor.execute(num_seats, (departing_airline_name, departing_airplane_id, departing_flight_num, departing_depart_date, departing_depart_time))
		depart_seats = cursor.fetchall()
		depart_flight_seats = depart_seats[0]['seats']
		#print(f"available seats: {depart_flight_seats}")

		#flight percent capacity filled 
		depart_capacity_filled = depart_reserved / depart_flight_seats
		#print(depart_capacity_filled)
  
		session['depart_capacity_filled'] = depart_capacity_filled

		#obtain base price
		cursor.execute(find_base, (departing_airline_name, departing_flight_num, departing_depart_date, departing_depart_time))
		depart_price = cursor.fetchall()
		depart_base_price = depart_price[0]['base_price']

		if depart_capacity_filled > 0.8:
			depart_base_price *= 1.25

		#RETURN FLIGHT
  		#find number of tickets reserved for a specific flight
		cursor.execute(num_reserved, (returning_flight_num, returning_depart_date, returning_depart_time, returning_airline_name))
		return_res = cursor.fetchone()
		return_reserved = return_res['reserved']
		#print(f"reserved: {return_reserved}")

		#find total seats for a specific flight
		cursor.execute(num_seats, (returning_airline_name, returning_airplane_id, returning_flight_num, returning_depart_date, returning_depart_time))
		return_seats = cursor.fetchall()
		return_flight_seats = return_seats[0]['seats']
		#print(f"available seats: {return_flight_seats}")

		#flight percent capacity filled 
		return_capacity_filled = return_reserved / return_flight_seats
		#print(return_capacity_filled)
  
		session['return_capacity_filled'] = return_capacity_filled

		#obtain base price
		cursor.execute(find_base, (returning_airline_name, returning_flight_num, returning_depart_date, returning_depart_time))
		return_price = cursor.fetchall()
		return_base_price = return_price[0]['base_price']

		if return_capacity_filled > 0.8:
			return_base_price *= 1.25

		total = depart_base_price + return_base_price
		#created for insertion into ticket table later
		session['depart_ticket_price'] = depart_base_price
		session['return_ticket_price'] = return_base_price
		session['total'] = total

	if request.method == 'GET':
		if flight_type == 'one-way':
			return render_template('purchase.html', flight_type = flight_type, ticket_price = base_price)
		else:
			return render_template('purchase.html', flight_type = flight_type, depart_ticket_price = depart_base_price, return_ticket_price = return_base_price, total = total)
	

@app.route('/purchaseAuth', methods = ['GET', 'POST'])
def purchaseAuth():
	# Check if user is logged in
	if 'email' not in session:
		return redirect('/customer_login')
	
	# Check if flight_type is in session
	if 'flight_type' not in session:
		session['error'] = "No flight selected. Please search for a flight first."
		return redirect('/customer_home')
	
	try:
		#user input
		email = request.form['email']
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		dob = request.form['dob']

		#card info
		card_type = request.form['card_type']
		card_name = request.form['card_name']
		card_num = request.form['card_num']
		exp_date = request.form['exp_date']

		
		#Ticket_id needs to be created for flight first:
		largest_ticket_id = '''SELECT MAX(ticket_id) as recent_id
					   		  FROM ticket'''
		
		cursor = conn.cursor()
		cursor.execute(largest_ticket_id)
		largest_id = cursor.fetchone()
		
		if largest_id['recent_id'] == None:
			new_ticket_id = "T1"
		else:
			#increments the num value next to 'T' by 1 to generate new id
			new_ticket_id = f"T{int(largest_id['recent_id'][1:len(largest_id['recent_id'])]) + 1}"

		# Define queries for capacity checking
		num_reserved = '''SELECT COUNT(ticket_id) as reserved
						 FROM ticket
						 WHERE ticket.flight_number = %s AND
						 ticket.depart_date = %s AND
						 ticket.depart_time = %s AND
						 ticket.airline_name = %s'''
		
		num_seats = '''SELECT seats 
					  FROM airplane JOIN flight ON airplane.airline_name = flight.airline_name AND airplane.airplane_id = flight.airplane_id
					  WHERE airplane.airline_name = %s AND
					  airplane.airplane_id = %s AND
					  flight.flight_number = %s AND
					  flight.depart_date = %s AND
					  flight.depart_time = %s'''
		
		add_ticket = '''INSERT INTO ticket (ticket_id, flight_number, airline_name, depart_date, depart_time, 
				   ticket_price, card_type, card_num, card_name, exp_date, pur_date, pur_time)
				   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )'''
		
		add_purchase = '''INSERT INTO purchases (email, ticket_id)
						  VALUES (%s, %s)'''

		#price info
		action = request.form['choice']

		current_day = datetime.today().date()
		current_time = datetime.now()  # Changed from .time() to full datetime since pur_time is datetime type

		error = None

		if session['flight_type'] == 'one-way':
			# Check if required session variables exist
			if 'flight_num' not in session or 'airline_name' not in session or 'depart_date' not in session or 'depart_time' not in session or 'ticket_price' not in session:
				cursor.close()
				session['error'] = "Missing flight information. Please try selecting the flight again."
				return redirect('/customer_home')

			#CHECK IF FLIGHT CAPACITY IS FULL (re-check at purchase time to prevent race conditions)
			# Re-calculate capacity to ensure accuracy
			cursor.execute(num_reserved, (session['flight_num'], session['depart_date'], session['depart_time'], session['airline_name']))
			res = cursor.fetchone()
			current_reserved = res['reserved']
			
			# Get airplane_id from flight table
			get_airplane_id = '''SELECT airplane_id FROM flight 
								WHERE flight_number = %s AND airline_name = %s 
								AND depart_date = %s AND depart_time = %s'''
			cursor.execute(get_airplane_id, (session['flight_num'], session['airline_name'], session['depart_date'], session['depart_time']))
			flight_data = cursor.fetchone()
			airplane_id = flight_data['airplane_id']
			
			cursor.execute(num_seats, (session['airline_name'], airplane_id, session['flight_num'], session['depart_date'], session['depart_time']))
			seats = cursor.fetchall()
			current_seats = seats[0]['seats']
			
			if current_seats == 0:
				cursor.close()
				session['error'] = "Flight has no available seats."
				return redirect('/customer_home')
			
			current_capacity = current_reserved / current_seats
			
			if current_capacity >= 1.0:
				cursor.close()
				session['error'] = "Selected Flight has no more available seats"
				return redirect('/customer_home')
			else:
				#add to ticket table (convert ticket_price to int since database expects int)
				cursor.execute(add_ticket, (new_ticket_id, session['flight_num'], session['airline_name'], session['depart_date'], session['depart_time'], int(round(session['ticket_price'])), card_type, card_num, card_name, exp_date, current_day, current_time))
				conn.commit()

				#add to purchase table
				cursor.execute(add_purchase, (email, new_ticket_id))
				conn.commit()

		else:
			# Check if required session variables exist for round trip
			if 'departing_flight_num' not in session or 'departing_airline_name' not in session or 'departing_depart_date' not in session or 'departing_depart_time' not in session or 'depart_ticket_price' not in session:
				cursor.close()
				session['error'] = "Missing departure flight information. Please try selecting the flight again."
				return redirect('/customer_home')
			if 'returning_flight_num' not in session or 'returning_airline_name' not in session or 'returning_depart_date' not in session or 'returning_depart_time' not in session or 'return_ticket_price' not in session:
				cursor.close()
				session['error'] = "Missing return flight information. Please try selecting the flight again."
				return redirect('/customer_home')

			#CHECK IF FLIGHT CAPACITY IS FULL (re-check at purchase time to prevent race conditions)
			# Re-calculate capacity for departure flight
			cursor.execute(num_reserved, (session['departing_flight_num'], session['departing_depart_date'], session['departing_depart_time'], session['departing_airline_name']))
			depart_res = cursor.fetchone()
			depart_current_reserved = depart_res['reserved']
			
			get_depart_airplane_id = '''SELECT airplane_id FROM flight 
										WHERE flight_number = %s AND airline_name = %s 
										AND depart_date = %s AND depart_time = %s'''
			cursor.execute(get_depart_airplane_id, (session['departing_flight_num'], session['departing_airline_name'], session['departing_depart_date'], session['departing_depart_time']))
			depart_flight_data = cursor.fetchone()
			depart_airplane_id = depart_flight_data['airplane_id']
			
			cursor.execute(num_seats, (session['departing_airline_name'], depart_airplane_id, session['departing_flight_num'], session['departing_depart_date'], session['departing_depart_time']))
			depart_seats = cursor.fetchall()
			depart_current_seats = depart_seats[0]['seats']
			
			if depart_current_seats == 0:
				cursor.close()
				session['error'] = "Departure flight has no available seats."
				return redirect('/customer_home')
			
			depart_current_capacity = depart_current_reserved / depart_current_seats
			
			# Re-calculate capacity for return flight
			cursor.execute(num_reserved, (session['returning_flight_num'], session['returning_depart_date'], session['returning_depart_time'], session['returning_airline_name']))
			return_res = cursor.fetchone()
			return_current_reserved = return_res['reserved']
			
			get_return_airplane_id = '''SELECT airplane_id FROM flight 
										 WHERE flight_number = %s AND airline_name = %s 
										 AND depart_date = %s AND depart_time = %s'''
			cursor.execute(get_return_airplane_id, (session['returning_flight_num'], session['returning_airline_name'], session['returning_depart_date'], session['returning_depart_time']))
			return_flight_data = cursor.fetchone()
			return_airplane_id = return_flight_data['airplane_id']
			
			cursor.execute(num_seats, (session['returning_airline_name'], return_airplane_id, session['returning_flight_num'], session['returning_depart_date'], session['returning_depart_time']))
			return_seats = cursor.fetchall()
			return_current_seats = return_seats[0]['seats']
			
			if return_current_seats == 0:
				cursor.close()
				session['error'] = "Return flight has no available seats."
				return redirect('/customer_home')
			
			return_current_capacity = return_current_reserved / return_current_seats
			
			if depart_current_capacity >= 1.0 or return_current_capacity >= 1.0:
				cursor.close()
				session['error'] = "One or Both of Selected Flights has no more available seats"
				return redirect('/customer_home')
			else:
				#add to ticket table (convert ticket_price to int since database expects int)
				cursor.execute(add_ticket, (new_ticket_id, session['departing_flight_num'], session['departing_airline_name'], session['departing_depart_date'], session['departing_depart_time'], int(round(session['depart_ticket_price'])), card_type, card_num, card_name, exp_date, current_day, current_time))
				conn.commit()

				#add to purchase table
				cursor.execute(add_purchase, (email, new_ticket_id))
				conn.commit()
				
				#return flight needs separate ticket id since both flights in a round trip need to have unique ticket_ids (increment id of departure flight by 1 to generate new id for return flight)
				return_new_ticket_id = f"T{int(new_ticket_id[1:len(new_ticket_id)]) + 1}"
				
				cursor.execute(add_ticket, (return_new_ticket_id, session['returning_flight_num'], session['returning_airline_name'], session['returning_depart_date'], session['returning_depart_time'], int(round(session['return_ticket_price'])), card_type, card_num, card_name, exp_date, current_day, current_time))
				conn.commit()
				
				#add to purchase table for return flight
				cursor.execute(add_purchase, (email, return_new_ticket_id))
				conn.commit()
		
		cursor.close()

		# Purchase complete, redirect to customer home
		return redirect('/customer_home')
			
	except Exception as e:
		if 'cursor' in locals():
			cursor.close()
		# Print error for debugging
		print(f"Purchase error: {str(e)}")
		print(f"Exception type: {type(e).__name__}")
		import traceback
		traceback.print_exc()
		session['error'] = f"An error occurred while processing your purchase: {str(e)}"
		return redirect('/customer_home')
	

@app.route('/cancel_trip', methods=['GET', 'POST'])
def cancel_trip():
	# Check if user is logged in
	if 'email' not in session:
		return redirect('/customer_login')
	
	ticket_id = request.args.get('ticket_id')
	email = session['email']

	cursor = conn.cursor()
	
	# First verify the ticket belongs to the customer and is in the future
	verify_query = '''SELECT t.ticket_id 
					  FROM ticket t
					  JOIN purchases p ON t.ticket_id = p.ticket_id
					  WHERE t.ticket_id = %s 
					  AND p.email = %s
					  AND (t.depart_date > CURDATE() OR (t.depart_date = CURDATE() AND t.depart_time > CURTIME()))'''
	
	cursor.execute(verify_query, (ticket_id, email))
	valid_ticket = cursor.fetchone()
	
	if not valid_ticket:
		cursor.close()
		session['error'] = "Ticket not found or cannot be cancelled."
		return redirect('/customer_home')
	
	# Delete from purchases first (due to foreign key constraint)
	query = '''DELETE FROM purchases 
                WHERE ticket_id = %s AND email = %s'''
	cursor.execute(query, (ticket_id, email))
	conn.commit()
	
	# Then delete the ticket
	query = '''DELETE FROM ticket 
                WHERE ticket_id = %s'''
	cursor.execute(query, (ticket_id,))
	conn.commit()
	cursor.close()
	
	return redirect('/customer_home')


#Checks if flight created is valid
@app.route('/create_flightAuth', methods=['GET', 'POST'])
def create_flightAuth():
	if 'username' not in session:
		return redirect('/staff_login')

	username = session['username']

	if request.method == 'POST':
		flight_type = request.form.get('flight_type', 'one-way')
		flight_number = request.form['flight_number']
		airline_name = request.form['airline_name']
		depart_date = request.form['depart_date']
		depart_time = request.form['depart_time']
		airplane_name = request.form['airplane_name']
		airplane_id = request.form['airplane_id']
		arrival_time = request.form['arrival_time']
		arrival_date = request.form['arrival_date']
		base_price = request.form['base_price']
		flight_status = request.form['flight_status']
		depart_airport = request.form['depart_airport']
		arrival_airport = request.form['arrival_airport']	

		cursor = conn.cursor()

		# Helper function to check maintenance
		def check_maintenance(airplane_id, airline_name, depart_date, arrival_date):
			maintenance_check = '''
				SELECT maintenance_start, maintenance_end
				FROM Airplane
				WHERE airplane_id = %s AND airline_name = %s
				AND maintenance_start <= %s AND maintenance_end >= %s
			'''
			cursor.execute(maintenance_check, (airplane_id, airline_name, arrival_date, depart_date))
			return cursor.fetchone()

		# Check maintenance for outbound flight
		maintenance_result = check_maintenance(airplane_id, airline_name, depart_date, arrival_date)
		if maintenance_result:
			cursor.close()
			error = f"The outbound airplane is under maintenance from {maintenance_result['maintenance_start']} to {maintenance_result['maintenance_end']}, which overlaps with the flight period ({depart_date} to {arrival_date}). Please choose a different airplane or adjust the flight schedule."
			return render_template('create_flight.html', error=error)

		# Create outbound flight
		query = '''
            INSERT INTO Flight (flight_number, airline_name, depart_date, depart_time, airplane_name, airplane_id, arrival_time, arrival_date, base_price, flight_status, depart_airport, arrival_airport)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
		cursor.execute(query, (flight_number, airline_name, depart_date, depart_time, airplane_name, airplane_id, arrival_time, arrival_date, base_price, flight_status, depart_airport, arrival_airport))
		conn.commit()

		# If round trip, create return flight
		if flight_type == 'round-trip':
			return_flight_number = request.form.get('return_flight_number')
			return_airplane_name = request.form.get('return_airplane_name')
			return_airplane_id = request.form.get('return_airplane_id')
			return_depart_date = request.form.get('return_depart_date')
			return_depart_time = request.form.get('return_depart_time')
			return_arrival_time = request.form.get('return_arrival_time')
			return_arrival_date = request.form.get('return_arrival_date')
			return_base_price = request.form.get('return_base_price')
			return_flight_status = request.form.get('return_flight_status')

			# Validate return flight departs after outbound flight arrives
			# Compare dates first, then times if same date
			if return_depart_date < arrival_date:
				cursor.close()
				error = "Return flight must depart on or after the outbound flight arrival date. Please adjust the return flight schedule."
				return render_template('create_flight.html', error=error)
			elif return_depart_date == arrival_date:
				# Same day - check times
				if return_depart_time <= arrival_time:
					cursor.close()
					error = "Return flight must depart after the outbound flight arrives. Please adjust the return flight schedule."
					return render_template('create_flight.html', error=error)

			# Check maintenance for return flight
			return_maintenance = check_maintenance(return_airplane_id, airline_name, return_depart_date, return_arrival_date)
			if return_maintenance:
				cursor.close()
				error = f"The return airplane is under maintenance from {return_maintenance['maintenance_start']} to {return_maintenance['maintenance_end']}, which overlaps with the return flight period ({return_depart_date} to {return_arrival_date}). Please choose a different airplane or adjust the flight schedule."
				return render_template('create_flight.html', error=error)

			# Create return flight (airports are swapped)
			return_query = '''
				INSERT INTO Flight (flight_number, airline_name, depart_date, depart_time, airplane_name, airplane_id, arrival_time, arrival_date, base_price, flight_status, depart_airport, arrival_airport)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
			'''
			# Return flight: departure airport is the arrival airport of outbound, and vice versa
			cursor.execute(return_query, (return_flight_number, airline_name, return_depart_date, return_depart_time, return_airplane_name, return_airplane_id, return_arrival_time, return_arrival_date, return_base_price, return_flight_status, arrival_airport, depart_airport))
			conn.commit()

		cursor.close()
		return render_template('staff_home.html')
	return render_template('create_flight.html')

	
#Authorizes staff to change flight status 
@app.route('/change_flight_statusAuth', methods=['GET', 'POST'])
def change_flight_statusAuth():
	if request.method == 'POST':
		flight_number = request.form['flight_number']
		airline_name = request.form['airline_name']
		depart_date = request.form['depart_date']
		flight_status = request.form['flight_status']

		cursor = conn.cursor()
		# updates flight status 
		query = '''
            UPDATE Flight
            SET flight_status = %s
            WHERE flight_number = %s AND airline_name = %s AND depart_date = %s
        '''
		cursor.execute(query, (flight_status, flight_number, airline_name, depart_date))
		conn.commit()
		cursor.close()
		return render_template('staff_home.html')
	return render_template('change_flight_status.html')

#Authorizes staff to add new airplane
@app.route('/add_airplaneAuth', methods=['GET', 'POST'])
def add_airplaneAuth():
	if 'username' not in session:
		return redirect('/staff_login')
	
	if request.method == 'POST':
		airplane_id = request.form['airplane_id']
		airline_name = request.form['airline_name']
		seats = request.form['seats']
		company = request.form['company']
		model_num = request.form['model_num']
		manu_date = request.form['manu_date']
		age = request.form['age']
		maintenance_start = request.form['maintenance_start']
		maintenance_end = request.form['maintenance_end']

		cursor = conn.cursor()
		#Inserts new airplane into the database
		query = '''
            INSERT INTO Airplane (airplane_id, airline_name, seats, company, model_num, manu_date, age, maintenance_start, maintenance_end)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
		cursor.execute(query, (airplane_id, airline_name, seats, company, model_num, manu_date, age, maintenance_start, maintenance_end))
		conn.commit()
		cursor.close()
		return render_template("staff_home.html")
	return render_template("add_airplane.html")

#Authorizes staff to add new airport
@app.route('/add_airportAuth', methods=['GET', 'POST'])
def add_airportAuth():
	if 'username' not in session:
		return redirect('/staff_login')
	
	if request.method == 'POST':
		airport_code = request.form['airport_code']
		airport_name = request.form['airport_name']
		city = request.form['city']
		country = request.form['country']
		terminals = request.form['terminals']
		airport_type = request.form['airport_type']

		cursor = conn.cursor()
		#Inserts new airport info into the database 
		query = '''
            INSERT INTO Airport (airport_code, airport_name, city, country, terminals, airport_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''
		cursor.execute(query, (airport_code, airport_name, city, country, terminals, airport_type))
		conn.commit()
		cursor.close()
		return render_template("staff_home.html")
	return render_template("add_airport.html")

#Authorizes staff to schedule maintenance for planes
@app.route('/schedule_maintenanceAuth', methods=['GET', 'POST'])
def schedule_maintenanceAuth():
	if 'username' not in session:
		return redirect('/staff_login')
	
	if request.method == 'POST':
		airline_name = request.form['airline_name']
		airplane_id = request.form['airplane_id']
		maintenance_start = request.form['maintenance_start']
		maintenance_end = request.form['maintenance_end']

		cursor = conn.cursor()
		#Updates the scheduled maintenance
		query = '''
            UPDATE Airplane
            SET maintenance_start = %s, maintenance_end = %s
            WHERE airline_name = %s AND airplane_id = %s
        '''
		cursor.execute(query, (maintenance_start, maintenance_end, airline_name, airplane_id))
		conn.commit()
		cursor.close()
		return render_template("staff_home.html")
	return render_template("schedule_maintenance.html")

#Authorizes staff to view the flights operated by the airline they work at
@app.route('/view_flightsAuth', methods=['GET', 'POST'])
def view_flightsAuth():
	if 'username' not in session:
		return redirect('/staff_login')
	
	airline_name = session['airline_name']

	if request.method == 'POST':
		start_date = request.form['start_date']
		end_date = request.form['end_date']
		depart_airport = request.form['depart_airport']
		arrival_airport = request.form['arrival_airport']

		cursor = conn.cursor() 
		# Finds all flights during the specific flight period 
		query = '''
            SELECT f.flight_number, f.depart_date, f.depart_time, f.arrival_date, f.arrival_time
            FROM Flight f
            WHERE f.airline_name = %s
            AND f.depart_date BETWEEN %s AND %s
            AND depart_airport = %s AND arrival_airport = %s
        '''
		cursor.execute(query, (airline_name, start_date, end_date, depart_airport, arrival_airport))
		flights = cursor.fetchall()
		cursor.close()
		return render_template('view_flights.html', flights = flights)
	return render_template('view_flights.html')

# Authorizes staff to view customers in the flights
@app.route('/view_customers/<flight_number>')
def view_customers(flight_number):
	if 'username' not in session:
		return redirect('/staff_login')
	
	# Get staff's airline to ensure they only see customers from their airline
	airline_name = session.get('airline_name')
	if not airline_name:
		return redirect('/staff_login')
    
	cursor = conn.cursor()
	query = '''
        SELECT c.first_name, c.last_name
        FROM Customer c
        JOIN Purchases p ON c.email = p.email
        JOIN Ticket t ON p.ticket_id = t.ticket_id
        WHERE t.flight_number = %s AND t.airline_name = %s
    '''
	cursor.execute(query, (flight_number, airline_name))
	customers = cursor.fetchall()
	cursor.close()
	return render_template('view_customers.html', customers=customers)

#Authorizes staff to view the flights ratings operated by the airline they work at
@app.route('/view_flight_ratingsAuth', methods=['GET', 'POST'])
def view_flight_ratingsAuth():
    if 'username' not in session:
        return redirect('/staff_login')
    
    airline_name = session['airline_name']
        
    # Get list of flights for dropdown
    cursor = conn.cursor()
    query = 'SELECT DISTINCT flight_number FROM Flight WHERE airline_name = %s ORDER BY flight_number'
    cursor.execute(query, (airline_name,))
    flights = cursor.fetchall()
    
    if request.method == 'POST':
        flight_number = request.form.get('flight_number')
        
        if flight_number:
            # Get individual reviews for the selected flight
            query = '''
                SELECT r.rate, r.comment, c.first_name, c.last_name, r.depart_date, r.depart_time
                FROM Review r
                JOIN Customer c ON r.email = c.email
                WHERE r.flight_number = %s AND r.airline_name = %s
                ORDER BY r.depart_date DESC, r.depart_time DESC
            '''
            cursor.execute(query, (flight_number, airline_name))
            individual_ratings = cursor.fetchall()
            
            # Calculate average rating for the flight
            query = '''
                SELECT AVG(r.rate) AS average_rating, COUNT(*) AS total_reviews
                FROM Review r
                WHERE r.flight_number = %s AND r.airline_name = %s
            '''
            cursor.execute(query, (flight_number, airline_name))
            avg_result = cursor.fetchone()
            average_rating = round(avg_result['average_rating'], 1) if avg_result['average_rating'] else 0
            total_reviews = avg_result['total_reviews'] if avg_result else 0
            
            cursor.close()
            
            return render_template('view_flight_rating.html', 
                                 flights=flights,
                                 flight_number=flight_number,
                                 individual_ratings=individual_ratings,
                                 average_rating=average_rating,
                                 total_reviews=total_reviews)
        else:
            cursor.close()
            return render_template('view_flight_rating.html', flights=flights)
    
    cursor.close()
    return render_template('view_flight_rating.html', flights=flights)

# Helper function to get most frequent customer (all time)
def get_most_frequent_customer(airline_name):
    cursor = conn.cursor()
    query = '''
        SELECT c.first_name, c.last_name, COUNT(*) AS num_flights
        FROM Customer c
        JOIN Purchases p ON c.email = p.email
        JOIN Ticket t ON p.ticket_id = t.ticket_id
        JOIN Flight f ON t.flight_number = f.flight_number AND t.airline_name = f.airline_name
        WHERE f.airline_name = %s
        GROUP BY c.first_name, c.last_name
        ORDER BY num_flights DESC
        LIMIT 1
    '''
    cursor.execute(query, (airline_name,))
    most_frequent_customer = cursor.fetchone()
    cursor.close()
    return most_frequent_customer

#Authorizes staff to view the frequent customers of the airline
@app.route('/view_frequent_customersAuth', methods=['GET', 'POST'])
def view_frequent_customersAuth():
    if 'username' not in session:
        return render_template('staff_login.html')
    
    airline_name = session['airline_name']
    most_frequent_customer = get_most_frequent_customer(airline_name)
    return render_template('view_frequent_customer.html', most_frequent_customer=most_frequent_customer)

#Lets staff view customer flights 
@app.route('/view_customer_flights', methods=['POST'])
def view_customer_flights():
	if 'username' not in session:
		return redirect('/staff_login')
	
	airline_name = session['airline_name']
	customer_email = request.form['customer_email']

	cursor = conn.cursor()
	query = '''
        SELECT c.first_name, c.last_name, f.flight_number, f.depart_date, f.depart_time, f.arrival_date, f.arrival_time
        FROM Customer c
        JOIN Purchases p ON c.email = p.email
        JOIN Ticket t ON p.ticket_id = t.ticket_id
        JOIN Flight f ON t.flight_number = f.flight_number AND t.airline_name = f.airline_name
        WHERE f.airline_name = %s AND c.email = %s
    '''
	cursor.execute(query, (airline_name, customer_email))
	customer_flights = cursor.fetchall()
	cursor.close()
	
	# Also get most frequent customer so it doesn't disappear
	most_frequent_customer = get_most_frequent_customer(airline_name)
	return render_template('view_frequent_customer.html', customer_flights=customer_flights, most_frequent_customer=most_frequent_customer)

#Define route of customer logout
@app.route('/logout')
def logout():
	session.pop('email')
	session.clear()
	return redirect('/customer_login')

#Define route for staff logout 
@app.route('/logoutStaff')
def logoutStaff():
	session.pop('username')
	return redirect('/staff_login')

#Define route for view flight
@app.route('/view_flight')
def view_flight():
	return render_template('view_flights.html')

#Define route for create_flight	
@app.route('/create_flight')
def create_flight():
	return render_template('create_flight.html')

#Define route for staff home
@app.route('/staff_home')
def staff_home():
	if 'username' in session:
		first_name = session['first_name']
		return render_template('staff_home.html', first_name = first_name)
	else:
		return redirect('/staff_login')
	
#Define route for change flight status 
@app.route('/change_flight_status')
def change_flight_status():
	return render_template('change_flight_status.html')

#Define route for add airplane
@app.route('/add_airplane')
def add_airplane():
	return render_template('add_airplane.html')

#Define route for add airport
@app.route('/add_airport')
def add_airport():
	return render_template('add_airport.html')


#Define route for schedule maintenance
@app.route('/schedule_maintenance')
def schedule_maintenance():
	return render_template('schedule_maintenance.html')

#Define route for view flight rating
@app.route('/view_flight_rating')
def view_flight_ratings():
	if 'username' not in session:
		return redirect('/staff_login')
	
	airline_name = session['airline_name']
	cursor = conn.cursor()
	query = 'SELECT DISTINCT flight_number FROM Flight WHERE airline_name = %s ORDER BY flight_number'
	cursor.execute(query, (airline_name,))
	flights = cursor.fetchall()
	cursor.close()
	return render_template('view_flight_rating.html', flights=flights)

#Define route for view frequent customers
@app.route('/view_frequent_customer')
def view_frequent_customer():
	if 'username' not in session:
		return redirect('/staff_login')
	
	airline_name = session['airline_name']
	most_frequent_customer = get_most_frequent_customer(airline_name)
	return render_template('view_frequent_customer.html', most_frequent_customer=most_frequent_customer)

#Define route for view earned revenue
@app.route('/view_revenue')
def view_revenue():
	if 'username' not in session:
		return redirect('/staff_login')
	
	cursor = conn.cursor()

	#Get airline name for the staff
	airline_name = session['airline_name']

	# Calculate revenue for the last month, use COALESCE to handle NULL values
	query = '''
        SELECT COALESCE(SUM(t.ticket_price), 0) AS revenue
        FROM Ticket t
        JOIN Flight f ON t.flight_number = f.flight_number AND t.airline_name = f.airline_name AND t.depart_date = f.depart_date AND t.depart_time = f.depart_time
        WHERE f.airline_name = %s AND t.pur_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
    '''
	cursor.execute(query, (airline_name,))
	result = cursor.fetchone()
	revenue_last_month = result['revenue'] if result else 0

	# Calculate revenue for the last year
	query = '''
        SELECT COALESCE(SUM(t.ticket_price), 0) AS revenue
        FROM Ticket t
        JOIN Flight f ON t.flight_number = f.flight_number AND t.airline_name = f.airline_name AND t.depart_date = f.depart_date AND t.depart_time = f.depart_time
        WHERE f.airline_name = %s AND t.pur_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    '''
	cursor.execute(query, (airline_name,))
	result = cursor.fetchone()
	revenue_last_year = result['revenue'] if result else 0
	
	# Calculate total revenue (all time)
	query = '''
        SELECT COALESCE(SUM(t.ticket_price), 0) AS revenue
        FROM Ticket t
        JOIN Flight f ON t.flight_number = f.flight_number AND t.airline_name = f.airline_name AND t.depart_date = f.depart_date AND t.depart_time = f.depart_time
        WHERE f.airline_name = %s
    '''
	cursor.execute(query, (airline_name,))
	result = cursor.fetchone()
	total_revenue = result['revenue'] if result else 0
	
	cursor.close()
	return render_template('view_revenue.html', 
						 revenue_last_month=revenue_last_month, 
						 revenue_last_year=revenue_last_year,
						 total_revenue=total_revenue,
						 airline_name=airline_name)

#Define route for customer to give rating and comments 
@app.route('/give_ratings_comments')
def give_ratings_comments():
	return render_template('give_ratings_comments.html')


#Lets user to give ratings and comments for prev flights they being on
@app.route('/give_ratings_commentsAuth', methods=['GET', 'POST'])
def give_ratings_commentsAuth():
	# Clear editing session if canceling
	if request.method == 'GET':
		session.pop('editing_review', None)
		session.pop('edit_airline_name', None)
		session.pop('edit_flight_number', None)
		session.pop('edit_depart_date', None)
		session.pop('edit_depart_time', None)
	
	email = session['email']
	ticket_id = request.form.get('ticket_id')
	if ticket_id:
		session['ticket_id'] = ticket_id  # create session for ticket_id 
	
	cursor = conn.cursor()

	query = '''SELECT t.ticket_id 
				FROM flight f NATURAL JOIN ticket t
				WHERE ((f.arrival_date < CURDATE()) OR 
				(f.arrival_date = CURDATE() AND f.arrival_time < CURTIME())) AND 
				t.ticket_id IN( SELECT ticket_id 
                                    FROM ticket 
                                    WHERE ticket_id IN( SELECT ticket_id 
                                                        FROM purchases as P 
														WHERE P.email = %s))
				AND NOT EXISTS (
					SELECT 1 FROM Review r
					WHERE r.email = %s 
					AND r.airline_name = t.airline_name
					AND r.flight_number = t.flight_number
					AND r.depart_date = t.depart_date
					AND r.depart_time = t.depart_time
				)'''

	cursor.execute(query, (email, email))
	tickets = cursor.fetchall()
	
	# Get all existing reviews for this customer
	reviews_query = '''
		SELECT r.rate, r.comment, r.airline_name, r.flight_number, r.depart_date, r.depart_time,
			   f.depart_airport, f.arrival_airport
		FROM Review r
		JOIN Flight f ON r.airline_name = f.airline_name 
			AND r.flight_number = f.flight_number 
			AND r.depart_date = f.depart_date 
			AND r.depart_time = f.depart_time
		WHERE r.email = %s
		ORDER BY r.depart_date DESC, r.depart_time DESC
	'''
	cursor.execute(reviews_query, (email,))
	existing_reviews = cursor.fetchall()
	
	cursor.close()
	error = session.pop('error', None)
	return render_template('give_ratings_comments.html', previous_tickets=tickets, existing_reviews=existing_reviews, error=error)

		

@app.route('/post_ratings_comments', methods = ['GET', 'POST'])
def post_ratings_comments():
	email = session['email']
	rate = request.form['rating']
	comment = request.form['comment']
	
	cursor = conn.cursor()
	
	# Check if we're editing (from session) or creating new
	if session.get('editing_review'):
		# Update existing review using session data
		edit_airline = session.pop('edit_airline_name', None)
		edit_flight = session.pop('edit_flight_number', None)
		edit_date = session.pop('edit_depart_date', None)
		edit_time = session.pop('edit_depart_time', None)
		session.pop('editing_review', None)
		
		update_review = '''UPDATE Review 
						   SET rate = %s, comment = %s
						   WHERE email = %s AND airline_name = %s AND flight_number = %s 
						   AND depart_date = %s AND depart_time = %s'''
		cursor.execute(update_review, (rate, comment, email, edit_airline, edit_flight, edit_date, edit_time))
		conn.commit()
		cursor.close()
		return redirect('/give_ratings_commentsAuth')
	
	# Creating new review - need ticket_id
	ticket_id = session.get('ticket_id')
	if not ticket_id:
		cursor.close()
		session['error'] = "Please select a ticket first."
		return redirect('/give_ratings_commentsAuth')

	print("TICKET_ID IS: ")
	print(ticket_id)

	ticket_find = '''SELECT * 
			FROM ticket
			WHERE ticket_id = %s'''
	cursor.execute(ticket_find, (ticket_id,))
	ticket = cursor.fetchone()

	if not ticket:
		cursor.close()
		session['error'] = "Ticket not found."
		return redirect('/give_ratings_commentsAuth')

	print(ticket)
	
	airline_name = ticket['airline_name']
	flight_number = ticket['flight_number']
	depart_date = ticket['depart_date']
	depart_time = ticket['depart_time']

	# Check if review already exists (prevent duplicates for new reviews)
	check_review = '''SELECT * FROM Review 
					  WHERE email = %s AND airline_name = %s AND flight_number = %s 
					  AND depart_date = %s AND depart_time = %s'''
	cursor.execute(check_review, (email, airline_name, flight_number, depart_date, depart_time))
	existing_review = cursor.fetchone()
	
	if existing_review:
		cursor.close()
		session['error'] = "You have already submitted a review for this flight."
		return redirect('/give_ratings_commentsAuth')
	
	# Insert new review
	review_post = '''INSERT INTO Review(email, airline_name, flight_number, depart_date, depart_time, rate, comment)
	VALUES(%s, %s, %s, %s, %s, %s, %s)'''
	cursor.execute(review_post, (email, airline_name, flight_number, depart_date, depart_time, rate, comment))
	
	conn.commit()
	cursor.close()
	
	# Clear ticket_id from session after successful submission
	session.pop('ticket_id', None)
	
	return redirect('/give_ratings_commentsAuth')

#Route to edit a review - loads review data into form
@app.route('/edit_review', methods=['POST'])
def edit_review():
	if 'email' not in session:
		return redirect('/customer_login')
	
	email = session['email']
	airline_name = request.form['airline_name']
	flight_number = request.form['flight_number']
	depart_date = request.form['depart_date']
	depart_time = request.form['depart_time']
	
	cursor = conn.cursor()
	query = '''SELECT r.rate, r.comment, r.airline_name, r.flight_number, r.depart_date, r.depart_time,
	           f.depart_airport, f.arrival_airport
	           FROM Review r
	           JOIN Flight f ON r.airline_name = f.airline_name 
	               AND r.flight_number = f.flight_number 
	               AND r.depart_date = f.depart_date 
	               AND r.depart_time = f.depart_time
	           WHERE r.email = %s AND r.airline_name = %s AND r.flight_number = %s 
	           AND r.depart_date = %s AND r.depart_time = %s'''
	cursor.execute(query, (email, airline_name, flight_number, depart_date, depart_time))
	review = cursor.fetchone()
	
	# Get tickets for dropdown
	tickets_query = '''SELECT t.ticket_id 
	                FROM flight f NATURAL JOIN ticket t
	                WHERE ((f.arrival_date < CURDATE()) OR 
	                (f.arrival_date = CURDATE() AND f.arrival_time < CURTIME())) AND 
	                t.ticket_id IN( SELECT ticket_id 
	                                    FROM ticket 
	                                    WHERE ticket_id IN( SELECT ticket_id 
	                                                        FROM purchases as P 
	                                                        WHERE P.email = %s))
	                AND NOT EXISTS (
	                    SELECT 1 FROM Review r
	                    WHERE r.email = %s 
	                    AND r.airline_name = t.airline_name
	                    AND r.flight_number = t.flight_number
	                    AND r.depart_date = t.depart_date
	                    AND r.depart_time = t.depart_time
	                )'''
	cursor.execute(tickets_query, (email, email))
	tickets = cursor.fetchall()
	
	# Get all existing reviews
	reviews_query = '''
        SELECT r.rate, r.comment, r.airline_name, r.flight_number, r.depart_date, r.depart_time,
               f.depart_airport, f.arrival_airport
        FROM Review r
        JOIN Flight f ON r.airline_name = f.airline_name 
            AND r.flight_number = f.flight_number 
            AND r.depart_date = f.depart_date 
            AND r.depart_time = f.depart_time
        WHERE r.email = %s
        ORDER BY r.depart_date DESC, r.depart_time DESC
    '''
	cursor.execute(reviews_query, (email,))
	existing_reviews = cursor.fetchall()
	
	cursor.close()
	
	# Store review info in session for editing
	session['editing_review'] = True
	session['edit_airline_name'] = airline_name
	session['edit_flight_number'] = flight_number
	session['edit_depart_date'] = depart_date
	session['edit_depart_time'] = depart_time
	
	return render_template('give_ratings_comments.html', 
	                     previous_tickets=tickets, 
	                     existing_reviews=existing_reviews,
	                     editing_review=review)

#Route to delete a review
@app.route('/delete_review', methods=['POST'])
def delete_review():
	if 'email' not in session:
		return redirect('/customer_login')
	
	email = session['email']
	airline_name = request.form['airline_name']
	flight_number = request.form['flight_number']
	depart_date = request.form['depart_date']
	depart_time = request.form['depart_time']
	
	cursor = conn.cursor()
	delete_query = '''DELETE FROM Review 
	                  WHERE email = %s AND airline_name = %s AND flight_number = %s 
	                  AND depart_date = %s AND depart_time = %s'''
	cursor.execute(delete_query, (email, airline_name, flight_number, depart_date, depart_time))
	conn.commit()
	cursor.close()
	
	# Clear ticket_id from session so user can select a new ticket
	session.pop('ticket_id', None)
	
	return redirect('/give_ratings_commentsAuth')

#Define route for customer to track spending
@app.route('/track_spending')
def track_spending():
	if 'email' not in session:
		return redirect('/customer_login')
	
	email = session['email']
	cursor = conn.cursor()
	
	# Get all tickets purchased by the customer with flight details
	query = '''
		SELECT t.ticket_id, t.ticket_price, t.pur_date, t.pur_time,
			   f.airline_name, f.flight_number, f.depart_date, f.depart_time,
			   f.depart_airport, f.arrival_airport, f.arrival_date, f.arrival_time
		FROM Ticket t
		JOIN Purchases p ON t.ticket_id = p.ticket_id
		JOIN Flight f ON t.airline_name = f.airline_name 
			AND t.flight_number = f.flight_number 
			AND t.depart_date = f.depart_date 
			AND t.depart_time = f.depart_time
		WHERE p.email = %s
		ORDER BY t.pur_date DESC, t.pur_time DESC
	'''
	cursor.execute(query, (email,))
	all_tickets = cursor.fetchall()
	
	# Calculate total spending (all time)
	total_spending = sum(ticket['ticket_price'] for ticket in all_tickets)
	
	# Calculate spending by year
	yearly_spending = {}
	for ticket in all_tickets:
		pur_date = ticket['pur_date']
		if isinstance(pur_date, str):
			pur_date = datetime.strptime(pur_date, '%Y-%m-%d').date()
		year_key = pur_date.strftime('%Y')
		if year_key not in yearly_spending:
			yearly_spending[year_key] = 0
		yearly_spending[year_key] += ticket['ticket_price']
	
	cursor.close()
	
	return render_template('track_spending.html', 
						 all_tickets=all_tickets,
						 total_spending=total_spending,
						 yearly_spending=yearly_spending,
						 first_name=session.get('first_name', 'Customer'))

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5001 (changed from 5000 to avoid macOS AirPlay Receiver conflict)
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5001, debug = True)