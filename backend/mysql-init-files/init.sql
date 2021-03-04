SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS esd_db DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

GRANT ALL PRIVILEGES ON esd_db.* TO 'esd_user'@'%' WITH GRANT OPTION;

USE esd_db;

--
-- User Table
--

DROP TABLE IF EXISTS `User`;
CREATE TABLE IF NOT EXISTS `User` (
  `email` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `jwt_kid` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `User` (`email`, `name`, `password_hash`, `jwt_kid`) VALUES
('b@gmail.com', 'Brandon', '1516239022','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJAZ21haWwuY29tIiwibmFtZSI6IkJyYW5kb24iLCJwYXNzd29yZF9oYXNoIjoxNTE2MjM5MDIyfQ.se4cFTK8NwHb2Mt08tdDbwmylBBfIMceuMLP21Gy648'),
('p@gmail.com', 'Phyo','1516239022', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBAZ21haWwuY29tIiwibmFtZSI6IlBoeW8iLCJwYXNzd29yZF9oYXNoIjoxNTE2MjM5MDIyfQ.d8PH76iLJyeyZUMOf14AuqnEKaeEdFeZeMBK1DCWYiY');

--
-- Module Verfication Table
--
DROP TABLE IF EXISTS `ModuleVerification`;
CREATE TABLE IF NOT EXISTS `ModuleVerification` (
  `email` varchar(255) NOT NULL,
  `module_code` varchar(255) NOT NULL,
  `module_grade` varchar(255) NOT NULL,
  PRIMARY KEY (`email`,`module_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `ModuleVerification` (`email`, `module_code`, `module_grade`) VALUES
('b@gmail.com', 'IS111', 'A-'),
('b@gmail.com', 'IS210', 'A+'),
('p@gmail.com', 'IS210', 'A+'),
('p@gmail.com', 'IS111', 'A+');

--
-- Module Table
--
DROP TABLE IF EXISTS `Module`;
CREATE TABLE IF NOT EXISTS `Module` (
  `module_code` varchar(255) NOT NULL,
  `module_name` varchar(255) NOT NULL,
  PRIMARY KEY (`module_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `Module` (`module_code`, `module_name`) VALUES
('IS111', 'Introduction to Programming'),
('IS210', 'Business Process Analysis Solutioning');

--
-- Bubble Table
--
DROP TABLE IF EXISTS `Bubble`;
CREATE TABLE IF NOT EXISTS `Bubble` (
  `bubble_id` int(255) NOT NULL,
  `bubble_name` varchar(255) NOT NULL,
  `create_timestamp` int(255) NOT NULL,
  `meet_timestamp` int(255) NOT NULL,
  `capacity` int(255) NOT NULL,
  `agenda` varchar(255) NOT NULL,
  `module_code` varchar(255) NOT NULL,
  PRIMARY KEY (`bubble_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `Bubble` (`bubble_id`, `bubble_name`, `create_timestamp`, `meet_timestamp`,`capacity`, `agenda`, `module_code`) VALUES
('1', 'IS111 Workshop', '1619798400', '1619798400', '20','Recap on dictionaries','IS111'),
('2', 'IS210 Workshop', '1619798400', '1619798400','20','How to draw workflow diagrams','IS210');

--
-- Bubble Comment Table
--
DROP TABLE IF EXISTS `BubbleComment`;
CREATE TABLE IF NOT EXISTS `BubbleComment` (
  `bubble_id` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `timestamp` int(255) NOT NULL,
  `comment` varchar(255) NOT NULL,
  PRIMARY KEY (`bubble_id`,`email`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `BubbleComment` (`bubble_id`,`email`, `timestamp`,`comment`) VALUES
('1', 'b@gmail.com', '1619798400', 'This app is amazing.'),
('1', 'p@gmail.com', '1619798402', 'I think so too!'),
('2', 'p@gmail.com', '1619798401', 'This app is amazing.');

--
-- Bubble File Table
--
DROP TABLE IF EXISTS `BubbleFile`;
CREATE TABLE IF NOT EXISTS `BubbleFile` (
  `bubble_id` int(255) NOT NULL,
  `timestamp` int(255) NOT NULL,
  `s3_bucket` varchar(255) NOT NULL,
  PRIMARY KEY (`bubble_id`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `BubbleFile` (`bubble_id`, `timestamp`,`s3_bucket`) VALUES
('1', '1619798400', '#'),
('2', '1619798401', '#');

--
-- Bubble Role Table
--
DROP TABLE IF EXISTS `BubbleRole`;
CREATE TABLE IF NOT EXISTS `BubbleRole` (
  `bubble_id` int(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  PRIMARY KEY (`bubble_id`,`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `BubbleRole` (`bubble_id`, `email`,`type`) VALUES
('1', 'b@gmail.com', 'mentor'),
('1', 'p@gmail.com', 'participant'),
('2', 'b@gmail.com', 'participant'),
('2', 'p@gmail.com', 'mentor');

--
-- Log Table
--
DROP TABLE IF EXISTS `Log`;
CREATE TABLE IF NOT EXISTS `Log` (
  `email` varchar(255) NOT NULL,
  `timestamp` int(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `json_data_string` varchar(255) NOT NULL,
  PRIMARY KEY (`email`,`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `Log` (`email`, `timestamp`,`type`,`json_data_string`) VALUES
('b@gmail.com', '1619798400', 'log', '{message: \"hello world\"');

COMMIT;