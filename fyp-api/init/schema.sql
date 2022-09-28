-- -------------------------------------------------------------
-- TablePlus 4.8.2(436)
--
-- https://tableplus.com/
--
-- Database: FYP
-- Generation Time: 2022-09-28 16:57:41.7440
-- -------------------------------------------------------------


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


CREATE TABLE `Block` (
  `BID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT 'Uniquely identifies a block',
  `SID` varchar(255) NOT NULL COMMENT 'References Solution (SID)',
  PRIMARY KEY (`BID`),
  KEY `SID` (`SID`),
  CONSTRAINT `block_ibfk_1` FOREIGN KEY (`SID`) REFERENCES `Solution` (`SID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Class` (
  `CID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT 'Uniquely identifies a class',
  `Cname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Class name',
  `UID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'References User (UID)',
  PRIMARY KEY (`CID`),
  KEY `UID` (`UID`),
  CONSTRAINT `class_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `User` (`UID`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Comment` (
  `CMTID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT 'Uniquely identifies a comment',
  `Content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Comment content',
  `FID` varchar(255) NOT NULL COMMENT 'References Fragment (FID)',
  PRIMARY KEY (`CMTID`),
  KEY `FID` (`FID`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`FID`) REFERENCES `Fragment` (`FID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Distractor` (
  `DID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT 'Uniquely identifies a distractor',
  `Code` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Code',
  `FID` varchar(255) NOT NULL COMMENT 'References Fragment (FID)',
  PRIMARY KEY (`DID`),
  KEY `FID` (`FID`),
  CONSTRAINT `distractor_ibfk_1` FOREIGN KEY (`FID`) REFERENCES `Fragment` (`FID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Feedback` (
  `FBID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT 'Uniquely identifies a feedback',
  `Content` text NOT NULL COMMENT 'Feedback content',
  `DID` varchar(255) NOT NULL COMMENT 'References Distractor (DID)',
  PRIMARY KEY (`FBID`),
  KEY `DID` (`DID`),
  CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`DID`) REFERENCES `Distractor` (`DID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Fragment` (
  `FID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT 'Uniquely identifies a fragment',
  `Code` text NOT NULL COMMENT 'Code',
  `BID` varchar(255) NOT NULL COMMENT 'References Block (BID)',
  PRIMARY KEY (`FID`),
  KEY `BID` (`BID`),
  CONSTRAINT `fragment_ibfk_1` FOREIGN KEY (`BID`) REFERENCES `Block` (`BID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Question` (
  `QID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT 'Uniquely identifies a question',
  `Date` date NOT NULL COMMENT 'Question generated date',
  `Scope` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Question scope',
  `Description` text NOT NULL COMMENT 'Question description',
  `PIC` text COMMENT 'Question picture name',
  `Tag` varchar(255) NOT NULL COMMENT 'Question tag (standard, multiple solutions, insert key code )',
  `UID` varchar(255) NOT NULL COMMENT 'References User (UID)',
  PRIMARY KEY (`QID`),
  KEY `UID` (`UID`),
  CONSTRAINT `question_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `User` (`UID`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Solution` (
  `SID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT 'Uniquely identifies a solution',
  `Sname` text NOT NULL COMMENT 'Solution file name',
  `QID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'References Question (QID)',
  PRIMARY KEY (`SID`),
  KEY `QID` (`QID`),
  CONSTRAINT `solution_ibfk_1` FOREIGN KEY (`QID`) REFERENCES `Question` (`QID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `User` (
  `UID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT 'Uniquely identifies a user',
  `Uname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'User name',
  `HashedPassword` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Encrypted user password',
  `Email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'User E-mail',
  `Utype` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'User type (admin, teacher, student)',
  `CID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'References Class (CID)',
  PRIMARY KEY (`UID`),
  KEY `CID` (`CID`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`CID`) REFERENCES `Class` (`CID`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;