DROP DATABASE IF EXISTS LMS;
CREATE DATABASE LMS;
CREATE USER 'admin'@localhost IDENTIFIED BY 'group_25';
GRANT ALL privileges ON `LMS`.* TO 'admin'@localhost;
GRANT USAGE ON *.* TO 'admin'@localhost IDENTIFIED BY 'group_25';
SHOW GRANTS FOR 'admin'@localhost;
SHOW DATABASES;


system mysql -u 'admin' -p'group_25';
