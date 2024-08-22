CREATE TABLE Customer(
    email varchar(255) not null, 
    the_password varchar(255) not null,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    building_num int not null,
    street varchar(255) not null,
    apt_num int not null,
    city varchar(255) not null,
    the_state varchar(255) not null,
    zip_code numeric(5,0) not null,
    passport_num char(9) not null,
    passport_expiration date not null,
    pass_country varchar(255) not null,
    dob date not null,
    primary key(email)
);

CREATE TABLE Customer_Phone(
    email varchar(255) not null,
    phone_number varchar(255) not null,
    primary key(email, phone_number),
    foreign key(email) references Customer(email)
);

CREATE TABLE Ticket(
    ticket_id varchar(255) not null,
    ticket_price int not null,
    card_type varchar(255) not null,
    card_num varchar(255) not null,
    card_name varchar(255) not null,
    exp_date date not null,
    pur_date date not null,
    pur_time datetime not null,
    airline_name varchar(255) not null,
    flight_number varchar(255) not null,
    depart_date date not null,
    depart_time time not null,
    primary key(ticket_id),
    foreign key(flight_number, airline_name, depart_date, depart_time) references Flight(flight_number, airline_name, depart_date, depart_time)
);

CREATE TABLE Purchases(
    email varchar(255) not null,
    ticket_id varchar(255) not null,
    primary key(email, ticket_id),
    foreign key(email) references Customer(email),
    foreign key(ticket_id) references Ticket(ticket_id)
);

CREATE TABLE Airline(
    airline_name varchar(255) not null,
    primary key(airline_name)
);

CREATE TABLE Airport(
    airport_code varchar(255) not null,
    airport_name varchar(255) not null,
    city varchar(255) not null,
    country varchar(255) not null,
    terminals int not null,
    airport_type varchar(255) not null check (airport_type in ('domestic', 'international', 'both')),
    primary key(airport_code)
);

CREATE TABLE Airplane(
    airplane_id varchar(255) not null,
    airline_name varchar(255) not null,
    seats int not null,
    company varchar(255) not null,
    model_num varchar(255) not null,
    manu_date date not null,
    age int not null,
    maintenance_start date not null, 
    maintenance_end date not null,
    primary key(airplane_id, airline_name),
    foreign key(airline_name) references Airline(airline_name)
);

CREATE TABLE Flight(
    flight_number varchar(255) not null,
    airline_name varchar(255) not null,
    depart_date date not null,
    depart_time time not null,
    airplane_name varchar(255) not null,
    airplane_id varchar(255) not null,
    arrival_time time not null,
    arrival_date date not null,
    base_price int not null,
    flight_status varchar(255) not null check (flight_status in ('on-time', 'delayed')),
    depart_airport varchar(255) not null,
    arrival_airport varchar(255) not null,
    primary key(flight_number, airline_name, depart_date, depart_time),
    foreign key(airline_name) references Airline(airline_name),
    foreign key(airplane_name) references Airplane(airline_name),
    foreign key(airplane_id) references Airplane(airplane_id),
    foreign key(depart_airport) references Airport(airport_code),
    foreign key(arrival_airport) references Airport(airport_code)
);

CREATE TABLE Airline_Staff(
    username varchar(255) not null,
    the_password varchar(255) not null,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    dob date not null,
    airline_name varchar(255) not null,
    primary key(username),
    foreign key(airline_name) references Airline(airline_name)
);

CREATE TABLE Airline_Staff_Phone(
    username varchar(255) not null,
    phone_number varchar(255) not null,
    primary key(username, phone_number),
    foreign key(username) references Airline_Staff(username)
);

CREATE TABLE Airline_Staff_Email(
    username varchar(255) not null,
    email varchar(255) not null,
    primary key(username, email),
    foreign key(username) references Airline_Staff(username)
);

CREATE TABLE Review(
    email varchar(255) not null,
    airline_name varchar(255) not null,
    flight_number varchar(255) not null, 
    depart_date date not null,
    depart_time time not null,
    rate int not null check (rate in (1,2,3,4,5)),
    comment varchar(255) not null,
    primary key (email, airline_name, flight_number, depart_date, depart_time),
    foreign key(email) references Customer(email),
    foreign key(flight_number, airline_name, depart_date, depart_time) references Flight(flight_number, airline_name, depart_date, depart_time)
);