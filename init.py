#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
from datetime import datetime

import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)
# Lets Flask connect the CSS to the HTML 
app.static_folder = 'static'

#Configure MySQL. For mine port is 3306 and no password 
conn = pymysql.connect(host='localhost',
					   port = 3306,
                       user='root',
                       password='',
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
            WHERE p.email = %s AND (f.depart_date > CURDATE() OR (f.depart_date = CURDATE() AND f.depart_date > CURTIME()))
            ORDER BY f.depart_date ASC
        '''
        cursor.execute(query, (email))
        flights = cursor.fetchall()
        cursor.close()
        
        return render_template('customer_home.html', first_name=first_name, flights=flights)
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
		return_dated = datetime.strptime(return_date, '%Y-%m-%d').date()

		#return flight is after departure flight (same day return flight is tackled below)
		returning = '''SELECT *
					   FROM flight 
					   WHERE depart_date = %s AND depart_airport = %s AND arrival_airport = %s'''

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

	flight_type = request.args.get('flight_type')
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
                  FROM airplane JOIN flight
                  WHERE airplane.airline_name = %s AND
                  airplane.airplane_id = %s AND
                  flight.flight_number = %s AND
                  flight.depart_date = %s AND
                  flight.depart_time = %s AND
				  flight.airline_name = %s'''
	
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
		print(f"reserved: {reserved}")

		#find total seats for a specific flight
		cursor.execute(num_seats, (airplane_name, airplane_id, flight_num, depart_date, depart_time, airline_name))
		seats = cursor.fetchall()
		flight_seats = seats[0]['seats']
		print(f"available seats: {flight_seats}")

		#flight percent capacity filled 
		capacity_filled = reserved / flight_seats
		print(capacity_filled)

		session['capacity_filled'] = capacity_filled

		#obtain base price
		cursor.execute(find_base, (airline_name, flight_num, depart_date, depart_time))
		price = cursor.fetchall()
		base_price = price[0]['base_price']

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
		cursor.execute(num_seats, (departing_airplane_name, departing_airplane_id, departing_flight_num, departing_depart_date, departing_depart_time, departing_airline_name))
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
		cursor.execute(num_seats, (returning_airplane_name, returning_airplane_id, returning_flight_num, returning_depart_date, returning_depart_time, returning_airline_name))
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
	
	#user input
	email = request.form['email']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	dob = request.form['dob']
	print(email)

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

	print(f"NEW TICKET ID: {new_ticket_id}")

	
	add_ticket = '''INSERT INTO ticket (ticket_id, flight_number, airline_name, depart_date, depart_time, 
			   ticket_price, card_type, card_num, card_name, exp_date, pur_date, pur_time)
			   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )'''
	
	add_purchase = '''INSERT INTO purchases (email, ticket_id)
					  VALUES (%s, %s)'''

	#price info
	action = request.form['choice']

	current_day = datetime.today().date()
	current_time = datetime.now().time()

	print(current_day)
	print(current_time)

	error = None

	if session['flight_type'] == 'one-way':

		print("NOT SUPPOSED TO HAPPEN")

		#CHECK IF FLIGHT CAPACITY IS 80% OR FULL
		if session['capacity_filled'] == 1:
			print("MAX CAPACITY REACHED")
			
			error = "Selected Flight has no more available seats"
			return render_template('customer_home.html', error = error)
			
		else:
			
			#add to ticket table
			cursor.execute(add_ticket, (new_ticket_id, session['flight_num'], session['airline_name'], session['depart_date'], session['depart_time'], session['ticket_price'], card_type, card_num, card_name, exp_date, current_day, current_time))
			conn.commit()

			#add to purchase table
			cursor.execute(add_purchase, (email, new_ticket_id))
			conn.commit()
			

	else:
		#CHECK IF FLIGHT CAPACITY IS 80% OR FULL
		if session['depart_capacity_filled'] == 1 or session['return_capacity_filled'] == 1:
			error = "One or Both of Selected Flights has no more available seats"
			return render_template('customer_home.html', error = error)
		else:
			
			#add to ticket table
			cursor.execute(add_ticket, (new_ticket_id, session['departing_flight_num'], session['departing_airline_name'], session['departing_depart_date'], session['departing_depart_time'], session['depart_ticket_price'], card_type, card_num, card_name, exp_date, current_day, current_time))
			conn.commit()

			#add to purchase table
			cursor.execute(add_purchase, (email, new_ticket_id))
			conn.commit()
			
			#return flight needs separate ticket id since both flights in a round trip need to have unique ticket_ids (increment id of departure flight by 1 to generate new id for return flight)
			return_new_ticket_id = f"T{int(new_ticket_id[1:len(new_ticket_id)]) + 1}"
			print(f"RETURN TICKET ID: {return_new_ticket_id}")
			
			
			cursor.execute(add_ticket, (return_new_ticket_id, session['returning_flight_num'], session['returning_airline_name'], session['returning_depart_date'], session['returning_depart_time'], session['return_ticket_price'], card_type, card_num, card_name, exp_date, current_day, current_time))
			conn.commit()
			'''
			#add to purchase table
			cursor.execute(add_purchase(email, new_ticket_id))
			conn.commit()
			'''
			#new id for return flight
			return_new_ticket_id = f"T{int(new_ticket_id[1]) + 1}"
			cursor.execute(add_purchase, (email, return_new_ticket_id))
			conn.commit()
			

	if action == 'Buy Another':

		session['card_type'] = card_type
		session['card_name'] = card_name
		session['card_num'] = card_num
		session['exp_date'] = exp_date


		if session['flight_type'] == 'one-way':
			#session['total_price'] = session['total_price'] + session['ticket_price']
			return render_template('purchase.html', buy_another = action, email = email, card_type = card_type, card_name = card_name, card_num = card_num, exp_date = exp_date, flight_type = session['flight_type'], ticket_price = session['ticket_price'])
			#SESSION POP CARD INFO AFTER DONE?
		else:
			return render_template('purchase.html', buy_another = action, email = email, card_type = card_type, card_name = card_name, card_num = card_num, exp_date = exp_date, 
						  flight_type = session['flight_type'], ticket_price = session['ticket_price'], depart_ticket_price = session['depart_ticket_price'], return_ticket_price = session['return_ticket_price'], total = session['total'])
  
    #done
	else:
		return redirect('/customer_home')
	

@app.route('/cancel_trip', methods=['GET', 'POST'])
def cancel_trip():
	ticket_id = request.args.get('ticket_id')
	print("TICKET ID SHOULD BE")
	print(ticket_id)

	cursor = conn.cursor()
	
	query = '''DELETE FROM purchases 
                WHERE ticket_id = %s AND
                ticket_id IN(SELECT ticket_id FROM ticket
                        WHERE ticket_id = %s AND
                        depart_date > CURDATE() AND
                        depart_time > CURTIME())'''

	cursor.execute(query, (ticket_id, ticket_id))
	conn.commit()
	query = '''DELETE FROM ticket 
                WHERE ticket_id = %s AND
                depart_date > CURDATE() AND
                depart_time > CURTIME()'''
	
	cursor.execute(query, (ticket_id))
	conn.commit()
	cursor.close()
	
	return redirect('/customer_home')


#Checks if flight created is valid
@app.route('/create_flightAuth', methods=['GET', 'POST'])
def create_flightAuth():
	if 'username' not in session:
		render_template('staff_login.html')

	username = session['username']

	if request.method == 'POST':
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

		#Edge case: Check if airplane is under maintenance during flight period
		# checks if flight period is in between the maintenance time 
		# query = '''
        #     SELECT COUNT(*) AS count
        #     FROM Airplane
        #     WHERE airplane_id = %s AND airline_name = %s
        #     AND (
        #         (maintenance_start <= %s AND maintenance_end >= %s) OR
        #         (maintenance_start <= %s AND maintenance_end >= %s))
        # '''
		# cursor.execute(query, (airplane_id, airline_name, depart_date, arrival_date))
		# result = cursor.fetchone()

		# if result['count'] > 0:
		# 	error = "The airplane is under maintenance during this flight period. Please choose a different airplane or a different flight schedule"
		# 	return render_template('create_flight.html', error=error)

		#Inserts new flight into the database
		query = '''
            INSERT INTO Flight (flight_number, airline_name, depart_date, depart_time, airplane_name, airplane_id, arrival_time, arrival_date, base_price, flight_status, depart_airport, arrival_airport)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
		cursor.execute(query, (flight_number, airline_name, depart_date, depart_time, airplane_name, airplane_id, arrival_time, arrival_date, base_price, flight_status, depart_airport, arrival_airport))
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
		return render_template('staff_login.html')
	
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
		return render_template('staff_login.html')
	
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
		return render_template('staff_login.html')
	
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
		return render_template('staff_login.html')
	
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
		return render_template('staff_login.html')
    
	cursor = conn.cursor()
	query = '''
        SELECT c.first_name, c.last_name
        FROM Customer c
        JOIN Purchases p ON c.email = p.email
        JOIN Ticket t ON p.ticket_id = t.ticket_id
        WHERE t.flight_number = %s
    '''
	cursor.execute(query, (flight_number,))
	customers = cursor.fetchall()
	cursor.close()
	return render_template('view_customers.html', customers=customers)

#Authorizes staff to view the flights ratings operated by the airline they work at
@app.route('/view_flight_ratingsAuth', methods=['GET', 'POST'])
def view_flight_ratingsAuth():
    if 'username' not in session:
        return render_template('staff_login.html')
    
    if request.method == 'POST':
        flight_number = request.form['flight_number']
        
        cursor = conn.cursor()
        query = '''
            SELECT AVG(r.rate) AS average_rating, r.comment, c.first_name, c.last_name
            FROM Review r
            JOIN Customer c ON r.email = c.email
            WHERE r.flight_number = %s
            GROUP BY r.comment, c.first_name, c.last_name
        '''
        cursor.execute(query, (flight_number,))
        flight_ratings = cursor.fetchall()
        cursor.close()
        
        return render_template('view_flight_rating.html', flight_ratings=flight_ratings)
    
    cursor = conn.cursor()
    query = 'SELECT DISTINCT flight_number FROM Flight WHERE airline_name = %s'
    cursor.execute(query, (session['airline_name'],))
    flights = cursor.fetchall()
    cursor.close()
    return render_template('view_flight_rating.html', flights=flights)

#Authorizes staff to view the frequent customers of the airline
@app.route('/view_frequent_customersAuth', methods=['GET', 'POST'])
def view_frequent_customersAuth():
    if 'username' not in session:
        return render_template('staff_login.html')
    
    airline_name = session['airline_name']
    
    cursor = conn.cursor()
    query = '''
        SELECT c.first_name, c.last_name, COUNT(*) AS num_flights
        FROM Customer c
        JOIN Purchases p ON c.email = p.email
        JOIN Ticket t ON p.ticket_id = t.ticket_id
        JOIN Flight f ON t.flight_number = f.flight_number AND t.airline_name = f.airline_name
        WHERE f.airline_name = %s AND t.pur_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
        GROUP BY c.first_name, c.last_name
        ORDER BY num_flights DESC
        LIMIT 1
    '''
    cursor.execute(query, (airline_name,))
    most_frequent_customer = cursor.fetchone()
    cursor.close()
    return render_template('view_frequent_customer.html', most_frequent_customer=most_frequent_customer)

#Lets staff view customer flights 
@app.route('/view_customer_flights', methods=['POST'])
def view_customer_flights():
	if 'username' not in session:
		return render_template('staff_login.html')
	
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
	return render_template('view_frequent_customer.html', customer_flights=customer_flights)

#Authorizes staff to view the earned revenue 
@app.route('/view_revenueAuth')
def view_revenueAuth():
	if 'username' not in session:
		return render_template('staff_login.html')
    
	cursor = conn.cursor()

	#Get airline name for the staff
	airline_name = session['airline_name']

    # Calculate revenue for the last month
	query = '''
        SELECT COALESCE(SUM(t.ticket_price), 0) AS revenue
        FROM Ticket t
        JOIN Flight f ON t.flight_number = f.flight_number AND t.airline_name = f.airline_name AND t.depart_date = f.depart_date AND t.depart_time = f.depart_time
        WHERE f.airline_name = %s AND t.pur_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
    '''
	cursor.execute(query, (airline_name,))
	revenue_last_month = cursor.fetchone()['revenue']

	# Calculate revenue for the last year
	query = '''
        SELECT COALESCE(SUM(t.ticket_price), 0) AS revenue
        FROM Ticket t
        JOIN Flight f ON t.flight_number = f.flight_number AND t.airline_name = f.airline_name AND t.depart_date = f.depart_date AND t.depart_time = f.depart_time
        WHERE f.airline_name = %s AND t.pur_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    '''
	cursor.execute(query, (airline_name,))
	revenue_last_year = cursor.fetchone()['revenue']
	cursor.close()
	return render_template('view_revenue.html', revenue_last_month=revenue_last_month, revenue_last_year=revenue_last_year)

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
	return render_template('view_flight_rating.html')

#Define route for view frequent customers
@app.route('/view_frequent_customer')
def view_frequent_customer():
	return render_template('view_frequent_customer.html')

#Define route for view earned revenue
@app.route('/view_revenue')
def view_revenue():
	return render_template('view_revenue.html')

#Define route for customer to give rating and comments 
@app.route('/give_ratings_comments')
def give_ratings_comments():
	return render_template('give_ratings_comments.html')


#Lets user to give ratings and comments for prev flights they being on
@app.route('/give_ratings_commentsAuth', methods=['GET', 'POST'])
def give_ratings_commentsAuth():
	
    email = session['email']
    ticket_id = request.form.get('ticket_id')
    session['ticket_id']  = request.form.get('ticket_id')# create session for ticket_id 
	
    print("GOTTEN TICKET ID IS:")
    print(ticket_id)
    cursor = conn.cursor()

    query = '''SELECT ticket_id 
                FROM flight NATURAL JOIN ticket
                WHERE ((arrival_date < CURDATE()) OR 
                (arrival_date = CURDATE() AND arrival_time < CURTIME())) AND 
                ticket_id IN( SELECT ticket_id 
                                    FROM ticket 
                                    WHERE ticket_id IN( SELECT ticket_id 
                                                        FROM purchases as P 
                                                        WHERE P.email = %s))'''


    cursor.execute(query, (email))
    tickets = cursor.fetchall()
	
    print("ALL PAST FLIGHTS")
    print(tickets)
    cursor.close()
    return render_template('give_ratings_comments.html', previous_tickets = tickets)

		

@app.route('/post_ratings_comments', methods = ['GET', 'POST'])
def post_ratings_comments():
	email = session['email']
	rate = request.form['rating']
	comment = request.form['comment']
	ticket_id = session['ticket_id']

	print("TICKET_ID IS: ")
	print(ticket_id)

	cursor = conn.cursor()
	ticket_find = '''SELECT * 
			FROM ticket
			WHERE ticket_id = %s'''
	cursor.execute(ticket_find, (ticket_id,))
	ticket = cursor.fetchone()

	print(ticket)
	
	airline_name = ticket['airline_name']
	flight_number = ticket['flight_number']
	depart_date = ticket['depart_date']
	depart_time = ticket['depart_time']


	review_post = '''INSERT INTO Review(email, airline_name, flight_number, depart_date, depart_time, rate, comment)
	VALUES(%s, %s, %s, %s, %s, %s, %s)'''

	cursor.execute(review_post, (email, airline_name, flight_number, depart_date, depart_time, rate, comment))
	conn.commit()
	cursor.close()
	
	
	
	return redirect('/customer_home')

	

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)