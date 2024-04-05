CREATE DATABASE `academicsystem` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

-- academicsystem.student definition

CREATE TABLE `student` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sno` varchar(100) NOT NULL,
  `sname` varchar(100) NOT NULL,
  `password` varchar(500) NOT NULL,
  `dept` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `major` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `grade` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `semester` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `core_credits` float DEFAULT NULL,
  `personal_development_credits` float DEFAULT NULL,
  `general_core_credits` float DEFAULT NULL,
  `general_required_credits` float DEFAULT NULL,
  `total` float DEFAULT NULL,
  `Column1` varchar(100) DEFAULT NULL,
  `Column2` varchar(100) DEFAULT NULL,
  `Column3` varchar(100) DEFAULT NULL,
  `Column4` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO academicsystem.student (sno,sname,password,dept,major,grade,semester,location,core_credits,personal_development_credits,general_core_credits,general_required_credits,total,Column1,Column2,Column3,Column4) VALUES
	 ('2021214001','www','123456','计算机学院','计算机科学与技术','2021','1',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);



-- academicsystem.course definition

CREATE TABLE `course` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cno` varchar(100) NOT NULL,
  `cname` varchar(100) NOT NULL,
  `credit` float DEFAULT NULL,
  `course_weekday` varchar(100) DEFAULT NULL,
  `course_time` varchar(16) DEFAULT NULL,
  `tname` varchar(100) DEFAULT NULL,
  `dept` varchar(100) DEFAULT NULL,
  `grade` varchar(100) DEFAULT NULL,
  `semester` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `classroom` varchar(100) DEFAULT NULL,
  `location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `floor` varchar(100) DEFAULT NULL,
  `description` text,
  `capacity` int DEFAULT NULL,
  `enrolled_students` int DEFAULT NULL,
  `Column1` varchar(100) DEFAULT NULL,
  `Column2` varchar(100) DEFAULT NULL,
  `Column3` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO academicsystem.course (cno,cname,credit,course_weekday,course_time,tname,dept,grade,semester,`type`,classroom,location,floor,description,capacity,enrolled_students,Column1,Column2,Column3) VALUES
	 ('001','软件工程',2.0,'星期一','7-8','张老师','计算机学院','2','1','专业主干课','n301','南湖校区','3','kkkkkk',45,28,NULL,NULL,NULL),
	 ('003','编译原理',3.0,'星期二','7-8','王老师','计算机学院','2','2','专业主干课','n302','南湖校区','3','pppppppp',40,20,NULL,NULL,NULL),
	 ('004','大数据技术',2.5,'星期一','3-4','林老师','计算机学院','3','2','个性发展课','n210','南湖校区','2','uuuuuuu',47,39,NULL,NULL,NULL);



-- academicsystem.sc definition

CREATE TABLE `sc` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sno` text NOT NULL,
  `cno` varchar(100) NOT NULL,
  `tname` varchar(100) DEFAULT NULL,
  `credit` float DEFAULT NULL,
  `academic_year` varchar(100) DEFAULT NULL,
  `semester` varchar(100) DEFAULT NULL,
  `score` float DEFAULT NULL,
  `type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `cname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `course_weekday` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `course_time` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `classroom` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `Column2` varchar(100) DEFAULT NULL,
  `Column3` varchar(100) DEFAULT NULL,
  `Column4` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO academicsystem.sc (sno,cno,tname,credit,academic_year,semester,score,`type`,cname,course_weekday,course_time,classroom,Column2,Column3,Column4) VALUES
	 ('2021214001','003','王老师',2.0,'2023-2024','2',90.0,'专业主干课','编译原理','星期四','7-8','n302',NULL,NULL,NULL),
	 ('2021214001','001','张老师',3.0,'2023-2024','2',89.0,'专业主干课','软件工程','星期三','7-8','n301',NULL,NULL,NULL);



-- academicsystem.room definition

CREATE TABLE `room` (
  `id` int NOT NULL AUTO_INCREMENT,
  `classroom` varchar(100) DEFAULT NULL,
  `location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `floor` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `description` text,
  `Column1` varchar(100) DEFAULT NULL,
  `Column2` varchar(100) DEFAULT NULL,
  `Column3` varchar(100) DEFAULT NULL,
  `Column4` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO academicsystem.room (classroom,location,floor,`type`,description,Column1,Column2,Column3,Column4) VALUES
	 ('n301','南湖','3','上课','ssssss',NULL,NULL,NULL,NULL),
	 ('n302','南湖','3','上课','kkkkk',NULL,NULL,NULL,NULL),
	 ('8201','本部','2','上课','oooo',NULL,NULL,NULL,NULL);



-- academicsystem.teacher definition

CREATE TABLE `teacher` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tno` varchar(100) NOT NULL,
  `tname` varchar(100) NOT NULL,
  `dept` varchar(100) DEFAULT NULL,
  `major` varchar(100) DEFAULT NULL,
  `Column1` varchar(100) DEFAULT NULL,
  `Column2` varchar(100) DEFAULT NULL,
  `Column3` varchar(100) DEFAULT NULL,
  `Column4` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO academicsystem.teacher (tno,tname,dept,major,Column1,Column2,Column3,Column4) VALUES
	 ('20210001','张毅','计算机学院','计算机科学与技术',NULL,NULL,NULL,NULL);


