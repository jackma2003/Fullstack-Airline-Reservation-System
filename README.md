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
