-- legal_procedures constraints --

SELECT * FROM legal_procedures;
UPDATE legal_procedures SET procedure_cost = 400 WHERE procedure_id = 4;

SHOW CREATE TABLE legal_procedures;
SELECT @message;
SHOW triggers;

SELECT * FROM procedures_list;
SELECT * FROM legal_procedures;
SELECT procedure_id FROM procedures_list WHERE case_id = 1;

SELECT pl.string_id, lp.procedure_name, lp.procedure_cost
FROM procedures_list pl
JOIN legal_procedures lp ON pl.procedure_id = lp.procedure_id
WHERE case_id = 1
ORDER BY lp.procedure_id;

-- Check constraints --

delimiter $$
DROP TRIGGER IF EXISTS tr_ins_positive_cost$$
CREATE TRIGGER tr_ins_positive_cost
BEFORE INSERT ON legal_procedures
FOR EACH ROW 
	IF NEW.procedure_cost < 0
	THEN 	
		SET @message = 'Стоимость процедуры не может быть отрицательной!';
		SIGNAL SQLSTATE '45000';
	END IF;
	SET @message = NULL$$

DROP TRIGGER IF EXISTS tr_upd_positive_cost$$
CREATE TRIGGER tr_upd_positive_cost
BEFORE UPDATE ON legal_procedures
FOR EACH ROW 
	IF NEW.procedure_cost < 0
	THEN 
		SET @message = 'Стоимость процедуры не может быть отрицательной!';
		SIGNAL SQLSTATE '45000';
	END IF;
    SET @message = NULL$$
delimiter ;
