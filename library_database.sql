-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: localhost    Database: library
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `authors`
--

DROP TABLE IF EXISTS `authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authors` (
  `idauthor` int(11) NOT NULL AUTO_INCREMENT,
  `authors_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idauthor`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authors`
--

LOCK TABLES `authors` WRITE;
/*!40000 ALTER TABLE `authors` DISABLE KEYS */;
INSERT INTO `authors` VALUES (1,'gokul'),(2,'hari'),(3,'abs'),(4,'guru'),(5,'gggg'),(6,'hgfyg'),(7,'wiiei');
/*!40000 ALTER TABLE `authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book` (
  `idbook` int(11) NOT NULL AUTO_INCREMENT,
  `book_name` varchar(45) DEFAULT NULL,
  `book_description` varchar(45) DEFAULT NULL,
  `book_code` varchar(45) DEFAULT NULL,
  `book_category` varchar(45) DEFAULT NULL,
  `book_author` varchar(45) DEFAULT NULL,
  `book_publisher` varchar(45) DEFAULT NULL,
  `book_price` int(11) DEFAULT NULL,
  PRIMARY KEY (`idbook`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book`
--

LOCK TABLES `book` WRITE;
/*!40000 ALTER TABLE `book` DISABLE KEYS */;
INSERT INTO `book` VALUES (3,'war','warbook','#1111','action','gokul','brj',11111),(4,'ajshjaksja','najxnajx','zxnbjhxjzx','sports','gokul','brj',2332332),(5,'dbms','xzczvxv','121212','action','gokul','brj',21221),(6,'ccdva','dv','d2d','action','gokul','brj',11);
/*!40000 ALTER TABLE `book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `idcategory` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idcategory`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'action'),(2,'drama'),(3,'sports'),(4,'space'),(5,'sss'),(6,'spac wra'),(7,'jfjrj'),(8,'s');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients`
--

DROP TABLE IF EXISTS `clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clients` (
  `idclients` int(11) NOT NULL AUTO_INCREMENT,
  `client_name` varchar(45) DEFAULT NULL,
  `client_email` varchar(45) DEFAULT NULL,
  `client_nationalid` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idclients`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients`
--

LOCK TABLES `clients` WRITE;
/*!40000 ALTER TABLE `clients` DISABLE KEYS */;
INSERT INTO `clients` VALUES (2,'darshan ','dadsadd@','1233333'),(4,'xxxs','sdsih','askajxjkaj'),(7,'zzzzzzz','zzzzzzzz','zzzzzzzzzz');
/*!40000 ALTER TABLE `clients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `day_operations`
--

DROP TABLE IF EXISTS `day_operations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `day_operations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_name` varchar(45) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `days` varchar(45) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `client` varchar(45) DEFAULT NULL,
  `to_date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `day_operations`
--

LOCK TABLES `day_operations` WRITE;
/*!40000 ALTER TABLE `day_operations` DISABLE KEYS */;
INSERT INTO `day_operations` VALUES (9,'gokuljs','Retrieve ','1','2019-10-16','goks','2019-10-17'),(10,'spacewar','Retrieve ','5','2019-10-16','abs','2019-10-21'),(11,'spacewar1212','Rent','9','2019-10-16','gugugu','2019-10-25'),(12,'spacewar1212','Rent','9','2019-10-16','gugugu','2019-10-25'),(13,'world war2','Rent','11','2019-10-16','gokul','2019-10-27'),(14,'pyqt5','Retrieve ','2','2019-10-16','me','2019-10-18'),(15,'superman','Rent','7','2019-10-16','charan','2019-10-23'),(16,'nznzknhbbb','Retrieve ','4','2019-10-22','','2019-10-26');
/*!40000 ALTER TABLE `day_operations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `publisher`
--

DROP TABLE IF EXISTS `publisher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `publisher` (
  `idpublisher` int(11) NOT NULL AUTO_INCREMENT,
  `publisher_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idpublisher`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `publisher`
--

LOCK TABLES `publisher` WRITE;
/*!40000 ALTER TABLE `publisher` DISABLE KEYS */;
INSERT INTO `publisher` VALUES (1,'brj'),(2,'archith'),(3,'dheeraj'),(4,'ssss'),(5,'uyggy'),(6,'js'),(7,'shdghgdb'),(8,''),(9,''),(10,''),(11,''),(12,''),(13,''),(14,'');
/*!40000 ALTER TABLE `publisher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `idusers` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) DEFAULT NULL,
  `user_email` varchar(45) DEFAULT NULL,
  `user_password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idusers`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','admin@gmail.com','admin'),(2,'','','');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-10-29 22:50:35
