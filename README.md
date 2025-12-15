# ✈️ Fullstack Airline Reservation System

<p align="center">A web application simulating real-life airline reservation systems.</p>
<p align="center"><em>Locally hosted for seamless development and testing</em></p>

## 🛠️ Tech Stack

- 🖥️ Frontend: HTML, CSS, JavaScript
- 🔧 Backend: Python Flask
- 🗄️ Database: MySQL

## 🚀 Setup Instructions

### Prerequisites

- 📦 XAMPP with phpMyAdmin
- 🐍 Python with Flask and PyMySQL modules installed

### Database Setup

1. 🟢 Ensure MySQL Database and Apache web server are running in XAMPP.
2. ⚙️ Configure MySQL: 
   - Port: `3306`
   - User: `root`
   - Charset: `utf8mb4`
3. 🗃️ Create a database named `Airline_SystemV2` in phpMyAdmin.
4. 📥 Import tables and data from the `database` folder.

### Application Deployment

1. 🚀 Run the application:
   ```
   python3 init.py
   ```
2. 🌐 Access the application at `http://127.0.0.1:5000`

## 📋 Use Cases

### Public Access
- View public flight information
- Search for future flights
- Check flight status
- Register as a customer or airline staff
- Login

### Customer Use Cases
1. View purchased flights
2. Search for flights
3. Purchase tickets
4. Cancel trips
5. Rate and comment on previous flights
6. Track spending
7. Logout

### Airline Staff Use Cases
1. View flights operated by their airline
2. Create new flights
3. Change flight status
4. Add new airplanes
5. Add new airports
6. View flight ratings
7. Schedule maintenance for airplanes
8. View frequent customers
9. View earned revenue
10. Logout
