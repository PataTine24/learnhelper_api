CREATE DATABASE IF NOT EXISTS `learnhelper`;
USE `learnhelper`;

/* Create all tables */

CREATE TABLE IF NOT EXISTS `answers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question_id` int NOT NULL,
  `content` varchar(255) NOT NULL,
  `correct` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `con_test_question` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question_id` int NOT NULL,
  `test_id` int NOT NULL,
  `creation_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `con_test_question_answer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `answer_id` int NOT NULL,
  `test_id` int NOT NULL,
  `question_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `persons` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `creation_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `questions` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `test_type_id` INT NOT NULL,
    `content` VARCHAR(2000) NOT NULL,
    `singlechoice` TINYINT(1) NOT NULL DEFAULT '1',
    `creation_timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
)  ENGINE=INNODB AUTO_INCREMENT=20 DEFAULT CHARSET=UTF8MB4 COLLATE = UTF8MB4_0900_AI_CI;

CREATE TABLE `taken_tests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `person_id` int NOT NULL,
  `test_type_id` int NOT NULL,
  `number_of_questions` int NOT NULL,
  `start_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `test_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` varchar(255) NOT NULL,
  `main_type_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



/* Creation of views & procedures */

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `learnhelper`.`view_test_type_main_type` AS select `a`.`id` AS `id`,`a`.`content` AS `type`,`a`.`main_type_id` AS `parent_type_id`,ifnull(`b`.`content`,'NO PARENT') AS `parent_type` from (`learnhelper`.`test_types` `a` left join `learnhelper`.`test_types` `b` on((`a`.`main_type_id` = `b`.`id`))) order by `a`.`main_type_id`;

/* add_new_random_question_to_test */

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_new_random_question_to_test`(
IN t_id int
)
BEGIN

-- get test type from the taken test table, if test id not existing return 0
SELECT IFNULL(
	(SELECT `test_type_id`
    FROM `taken_tests`
    WHERE `id` = t_id
    LIMIT 1)
, 0) INTO @t_type_id;

IF @t_type_id != 0 THEN
	-- get new question id, if none are availabl return 0 and dont insert
	SELECT IFNULL(
		(SELECT `id`
		FROM `questions`
		WHERE `id` NOT IN(SELECT  `question_id` FROM `con_test_question` WHERE `test_id` = t_id)
		AND (`test_type_id` = @t_type_id OR
		`test_type_id` IN (
			SELECT `id` FROM `test_types`
			WHERE `main_type_id` = @t_type_id
			))
		ORDER BY RAND()
		LIMIT 1)
		, 0
	) INTO @q_id;

	IF @q_id != 0 THEN
		 INSERT INTO `con_test_question`(`test_id`, `question_id`)
		 VALUES(t_id, @q_id) ;
	END IF;
ELSE
SET @q_id = 0;
END IF;

-- return the question id, which can be 0 if test id was wrong or no question was found
SELECT @q_id;


END$$
DELIMITER ;

/* add_person */

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_person`(
IN n VARCHAR (63)
)
BEGIN
INSERT INTO persons(`name`)
VALUES(n);

END$$
DELIMITER ;

/* add_question */

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_question`(
IN q_content varchar(2000),
IN q_type int,
IN q_single bool,
IN a_a varchar(255),
IN a_b varchar(255),
IN a_c varchar(255),
IN a_d varchar(255),
IN a_a_correct bool,
IN a_b_correct bool,
IN a_c_correct bool,
IN a_d_correct bool
)
BEGIN
-- Adding question
INSERT INTO questions(content, test_type_id, singlechoice)
VALUES(q_content, q_type, q_single);
-- Getting the ID of the question table
SET @q_id := last_insert_id();

-- Adding the 4 answers into the table
INSERT INTO answers(question_id, content, correct)
VALUE(@q_id, a_a, a_a_correct);
INSERT INTO answers(question_id, content, correct)
VALUE(@q_id, a_b, a_b_correct);
INSERT INTO answers(question_id, content, correct)
VALUE(@q_id, a_c, a_c_correct);
INSERT INTO answers(question_id, content, correct)
VALUE(@q_id, a_d, a_d_correct);

END$$
DELIMITER ;

/* add_single_choice_question*/

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_single_choice_question`(
IN q_content varchar(2000),
IN q_type int,
IN a_a varchar(255),
IN a_b varchar(255),
IN a_c varchar(255),
IN a_d varchar(255)

)
BEGIN
-- Adding question
CALL add_question(q_content , q_type, True,
			a_a, a_b, a_c, a_d,
            True, False, False, False
            );


END$$
DELIMITER ;

/* add_taken_test */

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_taken_test`(
IN p_id int,
IN t_type_id int,
IN num_q int
)
BEGIN

INSERT INTO `taken_tests`(person_id, test_type_id, number_of_questions)
VALUES(p_id, t_type_id, num_q);

SELECT  last_insert_id();

END$$
DELIMITER ;

/* add_test_answer */

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_test_answer`(
IN test_id int,
IN q_id int,
IN a_id int
)
BEGIN
INSERT INTO `con_test_question_answer`(`test_id`, `question_id`, `answer_id`)
VALUES(test_id, q_id, a_id);

END$$
DELIMITER ;

/* add_test_type */

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_test_type`(
IN t_content varchar(63),
IN m_type_id int
)
BEGIN

INSERT INTO `test_types`(content, main_type_iD)
VALUES(t_content, m_type_id);

END$$
DELIMITER ;

/* delete_person_data */

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_person_data`(
IN p_id int
)
BEGIN

-- first delete answers in test given
DELETE `ctqa` FROM `con_test_question_answer` AS `ctqa`
WHERE `ctqa`.`id` != 0 AND `ctqa`.`test_id` IN(
		SELECT `tt`.`id` FROM `taken_tests` AS `tt` WHERE `tt`.`person_id` = p_id
		);

-- Then delete questions belonging to test
DELETE `ctq` FROM `con_test_question` AS `ctq`
WHERE `ctq`.`id` != 0 AND `ctq`.`test_id` IN(
		SELECT `tt`.`id` FROM `taken_tests` AS `tt` WHERE `tt`.`person_id` = p_id
		);

-- finally delete the tests
DELETE FROM `taken_tests`
WHERE `id` != 0 AND `person_id` = p_id;

-- and lastly delete the person
DELETE FROM `persons` WHERE `id`= p_id;

END$$
DELIMITER ;

/* delete_question */

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_question`(
IN q_id int
)
BEGIN

DELETE FROM `answers`
WHERE `id` != 0 AND `question_id` = q_id ;

DELETE FROM `questions`
WHERE `id` = q_id ;

END$$
DELIMITER ;

/* get_answers_by_question_id */

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_answers_by_question_id`(
IN q_id int
)
BEGIN
SELECT * FROM `answers`
WHERE `question_id`=q_id
ORDER BY RAND();
END$$
DELIMITER ;

/* get_person_infos_by_id */

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_person_infos_by_id`(
IN p_id int
)
BEGIN
SELECT `persons`.`name`, `persons`.`creation_timestamp`, COUNT(`taken_tests`.`id`) AS `number_of_tests`
FROM `persons` LEFT JOIN `taken_tests` ON `taken_tests`.`person_id` = `persons`.`id`
WHERE `persons`.`id`= p_id
GROUP BY `persons`.`id`;
END$$
DELIMITER ;

/* get_question_by_id */

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_question_by_id`(
IN q_id int
)
BEGIN

SELECT * FROM `questions`
WHERE `id`=q_id;

END$$
DELIMITER ;

/* get_question_ids_by_test_id */

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_question_ids_by_test_id`(
IN t_id int
)
BEGIN

SELECT `question_id`
FROM `con_test_question`
WHERE `test_id` = t_id;

END$$
DELIMITER ;

/* get_test_answer_and_question_ids_by_test_id */

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_test_answer_and_question_ids_by_test_id`(
IN t_id int
)
BEGIN

SELECT `answer_id`, `question_id`
FROM `con_test_question_answer`
WHERE `test_id` = t_id
ORDER BY `question_id` ASC, RAND();

END$$
DELIMITER ;

/* get_test_types_with_main_type */

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_test_types_with_main_type`(
)
BEGIN

SELECT * FROM `view_test_type_main_type`;

END$$
DELIMITER ;

/* update_question WIP */

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `update_question`(
IN q_id int,
IN q_content varchar(2000),
IN q_type int,
IN q_single bool,
IN a_a_id int,
IN a_b_id int,
IN a_c_id int,
IN a_d_id int,
IN a_a_content varchar(255),
IN a_b_content varchar(255),
IN a_c_content varchar(255),
IN a_d_content varchar(255),
IN a_a_correct bool,
IN a_b_correct bool,
IN a_c_correct bool,
IN a_d_correct bool
)
BEGIN
-- Update the question
UPDATE `questions`
SET `content` = q_content, `test_type_id` = q_type , `singlechoice` = q_single
WHERE `id` = q_id;

UPDATE `answers`
SET `content` = a_a_content, `correct` = a_a_correct
WHERE `id` = a_a_id;
UPDATE `answers`
SET `content` = a_b_content, `correct` = a_b_correct
WHERE `id` = a_b_id;
UPDATE `answers`
SET `content` = a_c_content, `correct` = a_c_correct
WHERE `ID` = a_c_id;
UPDATE `answers`
SET `content` = a_d_content, `correct` = a_d_correct
WHERE `id` = a_d_id;


END$$
DELIMITER ;


