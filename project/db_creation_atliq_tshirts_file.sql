-- Create the database
CREATE DATABASE IF NOT EXISTS atliq_tshirts;
USE atliq_tshirts;

-- Create the t_shirts table
CREATE TABLE IF NOT EXISTS t_shirts (
    t_shirt_id INT AUTO_INCREMENT PRIMARY KEY,
    brand ENUM('Van Huesen', 'Levi', 'Nike', 'Adidas') NOT NULL,
    color ENUM('Red', 'Blue', 'Black', 'White') NOT NULL,
    size ENUM('XS', 'S', 'M', 'L', 'XL') NOT NULL,
    price INT CHECK (price BETWEEN 10 AND 50),
    stock_quantity INT NOT NULL,
    UNIQUE KEY brand_color_size (brand, color, size)  -- Ensures no duplicate brand-color-size combinations
);

-- Create the discounts table with a foreign key constraint
CREATE TABLE IF NOT EXISTS discounts (
    discount_id INT AUTO_INCREMENT PRIMARY KEY,
    t_shirt_id INT NOT NULL,
    pct_discount DECIMAL(5,2) CHECK (pct_discount BETWEEN 0 AND 100),
    FOREIGN KEY (t_shirt_id) REFERENCES t_shirts(t_shirt_id) ON DELETE CASCADE
);

-- Create a stored procedure to populate the t_shirts table
DELIMITER $$
CREATE PROCEDURE PopulateTShirts()
BEGIN
    DECLARE counter INT DEFAULT 0;
    DECLARE max_records INT DEFAULT 100;
    DECLARE brand ENUM('Van Huesen', 'Levi', 'Nike', 'Adidas');
    DECLARE color ENUM('Red', 'Blue', 'Black', 'White');
    DECLARE size ENUM('XS', 'S', 'M', 'L', 'XL');
    DECLARE price INT;
    DECLARE stock INT;

    WHILE counter < max_records DO
        -- Generate random values for brand, color, size
        SET brand = ELT(FLOOR(1 + RAND() * 4), 'Van Huesen', 'Levi', 'Nike', 'Adidas');
        SET color = ELT(FLOOR(1 + RAND() * 4), 'Red', 'Blue', 'Black', 'White');
        SET size = ELT(FLOOR(1 + RAND() * 5), 'XS', 'S', 'M', 'L', 'XL');
        SET price = FLOOR(10 + RAND() * 41);
        SET stock = FLOOR(10 + RAND() * 91);

        -- Insert only if it doesn't already exist (handles unique constraint on brand, color, size)
        BEGIN
            DECLARE CONTINUE HANDLER FOR 1062 BEGIN END; -- Ignore duplicate entry errors
            INSERT INTO t_shirts (brand, color, size, price, stock_quantity)
            VALUES (brand, color, size, price, stock);
            IF ROW_COUNT() > 0 THEN
                SET counter = counter + 1;
            END IF;
        END;
    END WHILE;
END$$
DELIMITER ;

-- Call the stored procedure to populate the t_shirts table
CALL PopulateTShirts();

-- Verify data in t_shirts table
SELECT * FROM t_shirts;

-- Insert at least 10 records into the discounts table
INSERT INTO discounts (t_shirt_id, pct_discount)
SELECT t_shirt_id, ELT(FLOOR(1 + RAND() * 10), 5, 10, 15, 20, 25, 30, 35, 40, 45, 50)
FROM t_shirts
LIMIT 10;

-- Verify data in discounts table
SELECT * FROM discounts;



