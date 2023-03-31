

pip3 install mysql-connector-python --user

docker run -d -p 3306:3306 --name mysql \
-e MYSQL_ROOT_PASSWORD=123456 \
-e TIMEZONE=Asia/Shanghai \
-e MYSQL_GENERAL_LOG=1 \
mysql:latest

CREATE TABLE `employees` (
      `emp_no` int(11) NOT NULL AUTO_INCREMENT,
      `birth_date` date NOT NULL,
      `first_name` varchar(14) NOT NULL,
      `last_name` varchar(16) NOT NULL,
      `gender` enum('M','F') NOT NULL,
      `hire_date` date NOT NULL,
      PRIMARY KEY (`emp_no`)
    ) ENGINE=InnoDB;


mysqldiff --overwrite 覆盖    