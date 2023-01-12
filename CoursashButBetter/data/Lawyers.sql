

SELECT * FROM lawyers;
UPDATE lawyers SET cases_lost = -3 WHERE lawyer_id = 1;
SELECT @message;

SELECT string_id, CONCAT(name, ' ', surname, ' ', patronymic), cases_won, cases_lost
FROM lawyers_list ll
JOIN lawyers l ON ll.lawyer_id = l.lawyer_id
WHERE case_id = 2
ORDER BY l.lawyer_id;


SELECT l.lawyer_id, CONCAT(name, ' ', surname, ' ', patronymic), cases_won, cases_lost
FROM lawyers l
WHERE l.lawyer_id NOT IN (SELECT lawyer_id 
						  FROM lawyers_list
                          WHERE case_id = 1)
ORDER BY l.lawyer_id;

SELECT lawyer_id FROM lawyers_list WHERE case_id = 2;


-- lawyers constraints -- 

delimiter $$
DROP TRIGGER IF EXISTS tr_ins_positive_cases_amount$$
CREATE TRIGGER tr_ins_positive_cases_amount
BEFORE INSERT ON lawyers
FOR EACH ROW 
	IF NEW.cases_won < 0 OR NEW.cases_lost < 0
	THEN 	
		SET @message = 'Количество дел не может быть отрицательным!';
		SIGNAL SQLSTATE '45000';
	END IF;
	SET @message = NULL$$

DROP TRIGGER IF EXISTS tr_upd_positive_cases_amount$$
CREATE TRIGGER tr_upd_positive_cases_amount
BEFORE UPDATE ON lawyers
FOR EACH ROW 
	IF NEW.cases_won < 0 OR NEW.cases_lost < 0
	THEN 
		SET @message = 'Количество дел не может быть отрицательным!';
		SIGNAL SQLSTATE '45000';
	END IF;
    SET @message = NULL$$
delimiter ;













