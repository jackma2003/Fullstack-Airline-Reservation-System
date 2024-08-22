-- a.) One Airline name "Jet Blue" --
INSERT INTO Airline(airline_name) VALUES ('Jet Blue');

-- b.) At least Two airports named "JFK" in NYC and "PVG" in Shanghai -- 
INSERT INTO Airport(airport_code, airport_name, city, country, terminals, airport_type) VALUES ('JFK', 'John F. Kennedy Airport', 'NYC', 'United States', 6, 'both');

INSERT INTO Airport(airport_code, airport_name, city, country, terminals, airport_type) VALUES ('PVG', 'Shanghai Pudong International Airport', 'Shanghai', 'China', 2, 'international');

-- c.) Insert at least three customers with appropriate names and other attributes -- 
INSERT INTO Customer(email, the_password, first_name, last_name, building_num, street, apt_num, city, the_state, zip_code, passport_num, passport_expiration, pass_country, dob) 
VALUES ('jm9223@nyu.edu', 'password123', 'Jack', 'Ma', 130, 'Main St', 1, 'Flushing', 'NY', 11355, 'A12345678', '2025-03-14', 'United States', '2003-03-14');

INSERT INTO Customer_Phone(email, phone_number) VALUES ('jm9223@nyu.edu', '9178850332');

INSERT INTO Customer(email, the_password, first_name, last_name, building_num, street, apt_num, city, the_state, zip_code, passport_num, passport_expiration, pass_country, dob) 
VALUES ('an3299@nyu.edu', 'password456', 'Andy', 'Ng', 140, 'Maple Ave', 2, 'Fresh Meadows', 'CA', 24987, 'B87654321', '2026-09-27', 'United States', '2002-09-27');

INSERT INTO Customer_Phone(email, phone_number) VALUES ('an3299@nyu.edu', '9295009232');

INSERT INTO Customer(email, the_password, first_name, last_name, building_num, street, apt_num, city, the_state, zip_code, passport_num, passport_expiration, pass_country, dob) 
VALUES ('cj2371@nyu.edu', 'password789', 'Chris', 'Jin', 150, 'Broadway', 3, 'Forest Hills', 'FL', 39664, 'C25315679', '2027-01-09', 'United States', '2004-01-09');

INSERT INTO Customer_Phone(email, phone_number) VALUES ('cj2371@nyu.edu', '9178864608');

-- d.) Insert at least three airplanes -- 

INSERT INTO Airplane (airplane_id, airline_name, seats, company, model_num, manu_date, age, maintenance_start, maintenance_end)
VALUES ('ABC123', 'Jet Blue', 200, 'Boeing', '737', '2010-01-01', 14, '2022-06-01', '2022-06-15');

INSERT INTO Airplane (airplane_id, airline_name, seats, company, model_num, manu_date, age, maintenance_start, maintenance_end)
VALUES ('DEF456', 'Jet Blue', 150, 'Airbus', 'A320', '2015-03-15', 9, '2022-09-01', '2022-09-10');

INSERT INTO Airplane (airplane_id, airline_name, seats, company, model_num, manu_date, age, maintenance_start, maintenance_end)
VALUES ('GHI789', 'Jet Blue', 180, 'Boeing', '787', '2018-07-01', 6, '2023-01-01', '2023-01-15');

INSERT INTO Airplane (airplane_id, airline_name, seats, company, model_num, manu_date, age, maintenance_start, maintenance_end)
VALUES ('VWT796', 'Delta', 250, 'Airbus', '800', '2018-07-01', 6, '2023-01-01', '2023-01-15');


-- e.) Insert at least One airline Staff working for Jet Blue -- 

INSERT INTO Airline_staff (username, the_password, first_name, last_name, dob, airline_name)
VALUES ('staff1', 'password123', 'Ratan', 'Dey', '1988-04-10', 'Jet Blue');

-- f.) Insert several flights with on-time, and delayed statuses -- 

INSERT INTO Flight (flight_number, airline_name, depart_date, depart_time, flight_status, depart_airport, arrival_airport, arrival_date, arrival_time, base_price,airplane_name, airplane_id)
VALUES ('JB101', 'Jet Blue', '2023-07-01', '09:00:00', 'on-time', 'JFK', 'PVG', '2023-07-02', '10:00:00', 1000, 'JetBlue', 'ABC123');

INSERT INTO Flight (flight_number, airline_name, depart_date, depart_time, flight_status, depart_airport, arrival_airport, arrival_date, arrival_time, base_price, airplane_name, airplane_id)
VALUES ('JB102', 'Jet Blue', '2025-07-05', '14:30:00', 'delayed', 'PVG', 'JFK', '2025-07-06', '16:00:00', 1200, 'JetBlue', 'DEF456');

INSERT INTO Flight (flight_number, airline_name, depart_date, depart_time, flight_status, depart_airport, arrival_airport, arrival_date, arrival_time, base_price, airplane_name, airplane_id)
VALUES ('JB103', 'Jet Blue', '2026-08-10', '11:00:00', 'on-time', 'JFK', 'PVG', '2026-08-11', '12:30:00', 900, 'JetBlue','GHI789');

INSERT INTO Flight (flight_number, airline_name, depart_date, depart_time, flight_status, depart_airport, arrival_airport, arrival_date, arrival_time, base_price, airplane_name, airplane_id)
VALUES ('JB104', 'Jet Blue', '2026-08-30', '12:30:00', 'on-time', 'JFK', 'PVG', '2026-08-31', '3:15:00', 900, 'Delta', 'VWT796');

-- g.) Insert some tickets for corresponding flights and insert some purchase records(customer bought some tickets) -- 

INSERT INTO Ticket (ticket_id, flight_number, airline_name, depart_date, depart_time, ticket_price, card_type, card_num, card_name, exp_date, pur_date, pur_time)
VALUES ('T1', 'JB101', 'Jet Blue', '2023-07-01', '09:00:00', 1000, 'Visa', '1234567890123456', 'Jack Ma', '2025-12-31', '2023-06-01', '2023-06-01 10:00:00');

INSERT INTO Ticket (ticket_id, flight_number, airline_name, depart_date, depart_time, ticket_price, card_type, card_num, card_name, exp_date, pur_date, pur_time)
VALUES ('T2', 'JB102', 'Jet Blue', '2025-07-05', '14:30:00', 1200, 'MasterCard', '9876543210987654', 'Andy Ng', '2024-06-30', '2023-06-10', '2023-06-10 15:30:00');

INSERT INTO Purchases (email, ticket_id)
VALUES ('jm9223@nyu.edu', 'T1');

INSERT INTO Purchases (email, ticket_id)
VALUES ('an3299@nyu.edu', 'T2');