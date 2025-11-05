CREATE TABLE User (
	is_active BOOLEAN DEFAULT 0 NOT NULL,
 	hotel INT,
 	FOREIGN KEY(hotel) REFERENCES Hotel(hotel_id)
--     FOREIGN KEY(room_type) REFERENCES RoomType(type_id),
--     FOREIGN KEY(room_price) REFERENCES RoomType(price)
);

CREATE TABLE Package (
	package_id INT AUTO_INCREMENT PRIMARY KEY,
	package_info VARCHAR(30),
 	room VARCHAR(20),
 	ski_pass INT,
 	FOREIGN KEY(room) REFERENCES Room(room_number),
 	FOREIGN KEY(ski_pass) REFERENCES SkiPass(ski_pass_id)
);

CREATE TABLE Reservation (
	reservation_id INT AUTO_INCREMENT PRIMARY KEY,
 	customer INT,
	check_in_date DATE DEFAULT CURRENT_TIME NOT NULL,
	check_out_date DATE NOT NULL,
 	booking_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
	payment_method VARCHAR(30),
	reservation_status VARCHAR(10) CHECK (reservation_status IN ('pending', 'confirmed', 'cancelled', 'no-show')) NOT NULL,
    package INT,
    total_price INT,
 	FOREIGN KEY(customer) REFERENCES Customer(customer_id),
    FOREIGN KEY(package) REFERENCES Package(package_id)
);