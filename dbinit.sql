SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS
  employees,
  employee_logins,
  payment_methods;

CREATE TABLE
  payment_methods (
    id INT NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    card VARCHAR(255) NOT NULL,
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
    subject_class ENUM('employee', 'superuser') NOT NULL,
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
          "dummy",
          "tp5I8U3c5XD1fvhD32N27kjWAWp4a2yG69iJzU3284355NTFOB7St077kX1331yT");

INSERT INTO employee_logins (employee_id, login, passwd_hash, passwd_salt)
  VALUES ((SELECT id FROM employees WHERE first_name = "James" LIMIT 1),
          "james",
          "dummy",
          "pF7xu220NtQf2CM8y2coWsN5do445bu34122yC7P7Qo8c6Re74lubr6kw5TM3jCo");

SET FOREIGN_KEY_CHECKS = 1;