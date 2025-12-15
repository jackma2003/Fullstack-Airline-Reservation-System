# ✈️ Fullstack Airline Reservation System

<p align="center">A web application simulating real-life airline reservation systems.</p>
<p align="center"><em>Locally hosted for seamless development and testing</em></p>

## 🛠️ Tech Stack

- 🖥️ Frontend: HTML, CSS, JavaScript
- 🔧 Backend: Python Flask
- 🎨 Templating: Jinja2
- 🗄️ Database: MySQL
- 🛠️ GUI: MySQL Workbench

## 🚀 Setup Instructions

### Prerequisites

- 🐍 Python 3.x
- 🗄️ MySQL Server (via Homebrew on macOS)
- 🎨 MySQL Workbench (for database visualization)

### Installation

1. **Install MySQL:**
   ```bash
   brew install mysql
   brew services start mysql
   ```

2. **Install Python dependencies:**
   ```bash
   pip install Flask pymysql
   ```

3. **Install MySQL Workbench (Optional):**
   ```bash
   brew install --cask mysqlworkbench
   ```

### Database Setup

1. **Connect to MySQL:**
   ```bash
   mysql -u root -p
   ```

2. **Create the database:**
   ```sql
   CREATE DATABASE Airline_SystemV2;
   USE Airline_SystemV2;
   ```

3. **Import tables and data:**
   ```sql
   SOURCE /path/to/your/project/database/tables.sql;
   SOURCE /path/to/your/project/database/inserts.sql;
   ```

4. **Verify tables were created:**
   ```sql
   SHOW TABLES;
   exit;
   ```

### MySQL Workbench Setup (Optional)

1. Open MySQL Workbench
2. Create a new connection:
   - **Connection Name:** Local MySQL
   - **Hostname:** `127.0.0.1`
   - **Port:** `3306`
   - **Username:** `root`
   - **Password:** Your MySQL password
3. Test connection and connect to visualize your database

### Application Configuration

1. **Update database credentials in `init.py`:**
   ```python
   conn = pymysql.connect(
       host='localhost',
       port=3306,
       user='root',
       password='your_mysql_password',  # Update this
       db='Airline_SystemV2',
       charset='utf8mb4',
       cursorclass=pymysql.cursors.DictCursor
   )
   ```

### Application Deployment

1. **Run the application:**
   ```bash
   python init.py
   ```

2. **Access the application:**
   - Open your browser and navigate to `http://127.0.0.1:5000`

3. **Stop the application:**
   - Press `Ctrl + C` in the terminal

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