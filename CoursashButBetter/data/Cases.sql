-- cases constraints -- 

SELECT @message;

SELECT * FROM cases;
UPDATE cases SET nom_price = -1 WHERE case_id = 1;
UPDATE cases SET case_end_date = '2022-04-28', case_won = 2 WHERE case_id = 1;
UPDATE cases SET case_end_date = NULL, case_won = NULL WHERE case_id = 1;

SELECT * FROM lawyers;
UPDATE lawyers SET cases_won = 0, cases_lost = 0 WHERE 1;
SELECT lawyer_id FROM lawyers_list WHERE case_id = 1;
UPDATE lawyers SET cases_won = cases_won + 1 WHERE lawyer_id IN (SELECT lawyer_id FROM lawyers_list WHERE case_id = 2);

SHOW TRIGGERS;

delimiter $$
DROP TRIGGER IF EXISTS tr_ins_positive_case_processing$$
CREATE TRIGGER tr_ins_positive_case_processing
BEFORE INSERT ON cases
FOR EACH ROW
	IF NEW.nom_price < 0
    THEN
		SET @message = 'Цена должна быть положительным числом!';
        SIGNAL SQLSTATE '45000';
	END IF;
    SET @message = NULL$$

DROP TRIGGER tr_upd_positive_case_processing$$
CREATE TRIGGER tr_upd_positive_case_processing
BEFORE UPDATE ON cases
FOR EACH ROW
BEGIN
	IF NEW.nom_price < 0
    THEN
		SET @message = 'Цена должна быть положительным числом!';
        SIGNAL SQLSTATE '45000';
	END IF;
    IF NEW.case_won NOT IN (0, 1)
    THEN 
		SET @message = 'Дело может быть либо выигранным, либо проигранным!';
        SIGNAL SQLSTATE '45000';
	END IF;
    IF NOT ISNULL(NEW.case_end_date) 
    THEN 
		IF NEW.case_start_date > NEW.case_end_date
		THEN
        BEGIN
			SET @message = 'Дата окончания дела должна быть после даты его начала!';
			SIGNAL SQLSTATE '45000';
		END;
        ELSE
			IF ISNULL(NEW.case_won)
			THEN
				SET @message = 'Оконченное дело должно быть выигранными или проигранным!';
				SIGNAL SQLSTATE '45000';
			ELSE
				IF NEW.case_won
                THEN
					UPDATE lawyers 
                    SET cases_won =cases_won + 1
                    WHERE lawyer_id IN (SELECT lawyer_id 
										FROM lawyers_list 
                                        WHERE case_id = NEW.case_id);
				ELSE
					UPDATE lawyers 
                    SET cases_lost = cases_lost + 1
                    WHERE lawyer_id IN (SELECT lawyer_id 
										FROM lawyers_list 
                                        WHERE case_id = NEW.case_id);
                END IF;
			END IF;
		END IF;
	ELSE
		IF NOT ISNULL(NEW.case_won)
        THEN
			SET @message = 'Законченное дело должно иметь дату окончания!';
			SIGNAL SQLSTATE '45000';
		end if;
	END IF;
    SET @message = NULL;
END$$
delimiter ;
-- case nom_price --
		




























