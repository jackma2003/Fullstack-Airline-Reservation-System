# Fullstack Airline Reservation System

<p>A web application simulating real-life airline reservation systems.</p>
<p>It is a locally hosted web application</p>

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Database: MySQL

## Database Schema

[View Relational Schema](https://github.com/user-attachments/files/16367518/Project_1.pdf)

## Setup Instructions

### Prerequisites

- XAMPP with phpMyAdmin
- Python with Flask and PyMySQL modules installed

### Database Setup

1. Ensure MySQL Database and Apache web server are running in XAMPP.
2. Configure MySQL: 
   - Port: 3306
   - User: root
   - Charset: utf8mb4
3. Create a database named `Airline_SystemV2` in phpMyAdmin.
4. Import tables and data from the `database` folder.

### Application Deployment

1. Run the application:
```
python3 init.py
```

2. Access the application at `http://127.0.0.1:5000`


## All CRUD Functionalities

1. Structure:
   - Group related functionalities together (e.g., all customer actions, all staff actions).
   - Use consistent formatting for each entry.
   - Add a brief introduction for each major section.

2. Explanations:
   - Make them more concise and focused on the key points.
   - Ensure consistency in the level of detail provided.

3. Queries:
   - Use consistent formatting for SQL queries.
   - Consider using placeholder comments for complex queries to save space.

Here's a revised version of your document:

```markdown
# FullStack Airline Reservation System CRUD Features

## Public Features

### 1. Search for Future Flights
```sql
SELECT flight_status, airline_name, flight_number, depart_date, arrival_date,
       arrival_time, depart_airport, arrival_airport
FROM flight
WHERE depart_date = %s 
  AND (depart_date > CURDATE() OR (depart_date = CURDATE() AND depart_time > CURTIME()))
  AND depart_airport = %s AND arrival_airport = %s
```
Retrieves future flight information based on user-provided departure date, departure airport, and arrival airport.

### 2. Search for Flight Status
```sql
SELECT flight_status
FROM Flight
WHERE airline_name = %s AND flight_number = %s 
  AND depart_date = %s AND arrival_date = %s
```
Fetches the status of a specific flight based on airline name, flight number, departure date, and arrival date.

## User Authentication

### 3. Customer Registration
```sql
SELECT * FROM Customer WHERE email = %s
```
Checks if the email already exists. If not, inserts new customer data into the database.

### 4. Staff Registration
```sql
SELECT * FROM airline_staff WHERE username = %s
```
Verifies if the username is available. If so, adds new staff information to the database.

### 5. Customer Login
```sql
SELECT * FROM Customer WHERE email = %s AND the_password = %s
```
Authenticates customer login credentials.

### 6. Staff Login
```sql
SELECT * FROM Airline_Staff WHERE username = %s AND the_password = %s
```
Verifies staff login credentials.

## Customer Features

### 7. View Customer Flights
```sql
SELECT t.ticket_id, f.airline_name, f.flight_number, f.depart_date, f.depart_time,
       f.depart_airport, f.arrival_airport
FROM Ticket t
JOIN Purchases p ON t.ticket_id = p.ticket_id
JOIN Flight f ON t.airline_name = f.airline_name 
             AND t.flight_number = f.flight_number 
             AND t.depart_date = f.depart_date 
             AND t.depart_time = f.depart_time
WHERE p.email = %s
ORDER BY f.depart_date ASC
```
Retrieves flight information for tickets purchased by a specific customer.

### 8-10. Search Flights, Purchase Tickets, Cancel Trip
(Similar to previous queries, implementation details omitted for brevity)

### 11. Rate and Comment on Previous Flights
```sql
-- Find eligible tickets for rating
SELECT * FROM ticket AS T 
WHERE T.depart_date < CURDATE() AND T.depart_time < CURTIME() 
  AND T.ticket_id IN (SELECT P.ticket_id FROM purchases AS P WHERE P.ticket_id = %s)

-- Insert review
INSERT INTO Review(email, airline_name, flight_number, depart_date, depart_time, rate, comment)
VALUES(%s, %s, %s, %s, %s, %s, %s)
```
Allows customers to rate and comment on past flights.

### 12. Track Customer Spending
(Query omitted, implementation details needed)

### 13. Logout
(No query required, handled by session management in Flask)

## Airline Staff Features

### 14. View Airline Flights
```sql
SELECT f.flight_number, f.depart_date, f.depart_time, f.arrival_date, f.arrival_time
FROM Flight f
WHERE f.airline_name = %s
  AND f.depart_date BETWEEN %s AND %s
  AND f.depart_airport = %s AND f.arrival_airport = %s
```
Retrieves flight information for a specific airline within a date range and route.

### 15-18. Create Flight, Change Flight Status, Add Airplane, Add Airport
(INSERT and UPDATE queries, details omitted for brevity)

### 19. View Flight Ratings
```sql
SELECT AVG(r.rate) AS average_rating, r.comment, c.first_name, c.last_name
FROM Review r
JOIN Customer c ON r.email = c.email
WHERE r.flight_number = %s
GROUP BY r.comment, c.first_name, c.last_name
```
Calculates average rating and displays comments for a specific flight.

### 20-22. Schedule Maintenance, View Frequent Customers, View Earned Revenue
(Queries omitted, implementation details needed)

### 23. Logout
(No query required, handled by session management in Flask)
```

This revised version:
- Groups related functionalities
- Uses consistent formatting
- Provides concise explanations
- Omits repetitive or less crucial details
- Highlights key CRUD operations

Would you like me to elaborate on any specific section or provide more details on how to improve certain aspects of your documentation?

