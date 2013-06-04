SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS
  employees,
  employee_logins,
  payment_methods,
  auth_tokens;

CREATE TABLE
  payment_methods (
    id INT NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    card_number VARCHAR(32) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
  )
  ENGINE=InnoDB
  CHARACTER SET=UTF8;

CREATE TABLE
  employees (
    id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    payment_method_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (payment_method_id) REFERENCES payment_methods(id) ON DELETE SET NULL,
    INDEX (first_name(12)),
    INDEX (last_name(12))
  )
  ENGINE=InnoDB
  CHARACTER SET=UTF8;

CREATE TABLE
  employee_logins (
    id INT NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    login VARCHAR(32) NOT NULL,
    passwd_hash VARCHAR(64) NOT NULL,
    passwd_salt VARCHAR(64) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE,
    UNIQUE (login),
    UNIQUE (employee_id)
  )
  ENGINE=InnoDB
  CHARACTER SET=UTF8;

CREATE TABLE
  auth_tokens (
    id INT NOT NULL AUTO_INCREMENT,
    subject_class ENUM('employee', 'superuser', 'paybot') NOT NULL,
    subject_id INT,
    token VARCHAR(64) NOT NULL,
    valid_from DATETIME NOT NULL,
    valid_until DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (token)
  )
  CHARACTER SET=UTF8;

#
# Populate employees

INSERT INTO employees (first_name, last_name)
  VALUES ("Dexter", "Morgan");

INSERT INTO employees (first_name, last_name)
  VALUES ("Olivia", "Cooper");

INSERT INTO employees (first_name, last_name)
  VALUES ("James", "Patrick");

#
# Populate logins

INSERT INTO employee_logins (employee_id, login, passwd_hash, passwd_salt)
  VALUES ((SELECT id FROM employees WHERE first_name = "Dexter" LIMIT 1),
          "dexter",
          "1f812e3b6fc87a9e77448e32d8cbc290bab0c2c738b4bea2d40896cbd951b2ec",
          "x91o32qji29825167F6Y3q9xX2D02k7B2839lnP48jape1ss4AG58143z520k4Ie");

INSERT INTO employee_logins (employee_id, login, passwd_hash, passwd_salt)
  VALUES ((SELECT id FROM employees WHERE first_name = "Olivia" LIMIT 1),
          "olivia",
          "9442e25019390c7125a554cec3fbf70d59c6869b8cd1d9a58cf8151a9ee0bc3d",
          "tp5I8U3c5XD1fvhD32N27kjWAWp4a2yG69iJzU3284355NTFOB7St077kX1331yT");

INSERT INTO employee_logins (employee_id, login, passwd_hash, passwd_salt)
  VALUES ((SELECT id FROM employees WHERE first_name = "James" LIMIT 1),
          "james",
          "4ac0f3ab844c60e4f3c006b540c8829a3b83a35d683de54fd82eea5d83e8ceaf",
          "pF7xu220NtQf2CM8y2coWsN5do445bu34122yC7P7Qo8c6Re74lubr6kw5TM3jCo");

#
# Populate payment methods

INSERT INTO payment_methods (employee_id, card_number)
  VALUES ((SELECT id FROM employees WHERE first_name = "Dexter" LIMIT 1), "4864 1323 5783 2522");

INSERT INTO payment_methods (employee_id, card_number)
  VALUES ((SELECT id FROM employees WHERE first_name = "Dexter" LIMIT 1), "5775 2457 1631 4656");

UPDATE employees
  SET payment_method_id = (SELECT id FROM payment_methods WHERE card_number = "4864 1323 5783 2522" LIMIT 1)
  WHERE first_name = "Dexter";

INSERT INTO payment_methods (employee_id, card_number)
  VALUES ((SELECT id FROM employees WHERE first_name = "Olivia" LIMIT 1), "2544 3462 2436 6846");

UPDATE employees
  SET payment_method_id = (SELECT id FROM payment_methods WHERE card_number = "2544 3462 2436 6846" LIMIT 1)
  WHERE first_name = "Olivia";

INSERT INTO payment_methods (employee_id, card_number)
  VALUES ((SELECT id FROM employees WHERE first_name = "James" LIMIT 1), "5565 7863 5475 6733");

UPDATE employees
  SET payment_method_id = (SELECT id FROM payment_methods WHERE card_number = "5565 7863 5475 6733" LIMIT 1)
  WHERE first_name = "James";

#
# Populate some tokens

INSERT INTO auth_tokens (subject_class, subject_id, token, valid_from, valid_until)
  VALUES ('superuser', NULL, '14fca4b4fd367c1a8e2942a11bd28515fbb8e1215a2295339b1234305488f6ea',
          (NOW()), (NOW() + INTERVAL 6000 HOUR));

INSERT INTO auth_tokens (subject_class, subject_id, token, valid_from, valid_until)
  VALUES ('paybot', NULL, 'b1555127084a674fa386d2ec12d02cb57881dde57080d8cea7fd04538c1d63c8',
          (NOW()), (NOW() + INTERVAL 6000 HOUR));

SET FOREIGN_KEY_CHECKS = 1;