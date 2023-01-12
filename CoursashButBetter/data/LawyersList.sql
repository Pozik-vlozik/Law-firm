-- lawyers_list constraints --

USE LawersFirm;

SELECT * FROM cases;
SELECT * FROM clients;
SELECT * FROM lawyers;
SELECT * FROM lawyers_list;
SELECT * FROM legal_procedures;
SELECT * FROM procedures_list;


SELECT lawyer_id FROM lawyers_list WHERE case_id = 2;


-- Вставка в таблицу списка адвокатов --

SELECT * FROM lawyers_list WHERE case_id = 5;
INSERT INTO lawyers_list (case_id, lawyer_id) VALUES (2, 3);
SELECT @message;

DROP FUNCTION IF EXISTS lawyer_is_in_case;
delimiter $$
CREATE FUNCTION lawyer_is_in_case(idLawyer INT, idCase INT)
RETURNS BOOLEAN DETERMINISTIC
BEGIN
	IF idLawyer IN (SELECT lawyer_id FROM lawyers_list WHERE case_id = idCase) 
    THEN 
		RETURN TRUE;
	ELSE 
		RETURN FALSE;
    END IF;
END$$
delimiter ;

delimiter $$
DROP TRIGGER IF EXISTS tr_ins_same_lawyers$$
CREATE TRIGGER tr_ins_same_lawyers
BEFORE INSERT ON lawyers_list
FOR EACH ROW 
	IF lawyer_is_in_case(NEW.lawyer_id, NEW.case_id)
	THEN 
		SET @message = 'Этот адвокат уже работает над данным делом!';
		SIGNAL SQLSTATE '45000';
	END IF;
    SET @message = NULL$$
delimiter ;

-- Вставка в таблицу списка адвокатов --















