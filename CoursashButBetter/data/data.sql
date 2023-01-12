USE LawersFirm;

SET SQL_SAFE_UPDATES = 0;

SELECT * FROM clients WHERE (lower(name) LIKE '%') ;
SELECT * FROM lawyers;
SELECT * FROM lawyers_list ORDER BY case_id;
SELECT * FROM legal_procedures;
SELECT * FROM procedures_list ORDER BY case_id;

SELECT * FROM cases;

DESCRIBE cases;

SET @message = '';

DELETE FROM clients WHERE client_id = 1;
DELETE FROM lawyers WHERE lawyer_id = 1;
DELETE FROM cases WHERE case_id = 5;
DELETE FROM procedures_list WHERE case_id > 0;


INSERT INTO clients (name, surname, patronymic, passport_number)
VALUES ("Стулов", "Стол", "Иванович", "pAssportNumber1"),
	   ("Чепцов", "Кирпич", "Металлович", "pAssportNumber2"),
	   ("Жиов", "Жижа", "Васильевич", "pAssportNumber3"),
	   ("Ножнов", "Внос", "Кириллович", "pAssportNumber4"),
	   ("Гвоздов", "Саморез", "Винтович", "pAssportNumber5");

INSERT INTO lawyers (name, surname, patronimyc)
VALUES ("Лэбтопов", "Денис", "Мышкович"),
	   ("Жечный", "Кворис", "Тровавович"),
	   ("Кнопочный", "Жульен", "Траволтавич"),
	   ("Крол", "Пятерка", "Запятая"),
	   ("Эфпятый", "Дорис", "Жальнобьяр");

INSERT INTO cases (client_id, case_start_date, nom_price, description)
VALUES (1, "2022-04-28", 1000, "Article 1"),
	   (2, "2022-03-17", 2000, "Article 1, Article 2"),
	   (3, "2022-04-09", 3000, "Article 3"),
	   (4, "2022-02-13", 6000, "Article 8, Article 4"),
	   (5, "2022-04-30", 10000, "Article 0, Article 9");

INSERT INTO legal_procedures (procedure_name, procedure_cost)
VALUES ("Proc 1", 100),
	   ("Proc 2", 200),
	   ("Proc 3", 300),
	   ("Proc 4", 400),
	   ("Proc 5", 500),
	   ("Proc 6", 600);

INSERT INTO lawyers_list (case_id, lawyer_id)
VALUES (1, 1),
	   (1, 2),
	   (2, 3),
	   (4, 4),
	   (5, 5),
	   (3, 2),
	   (4, 1),
	   (2, 4),
	   (2, 5);

INSERT INTO procedures_list (procedure_id, case_id)
VALUES (1, 1),
	   (2, 1),
	   (3, 2),
	   (4, 4),
	   (5, 5),
	   (6, 1),
	   (1, 5),
	   (2, 3),
	   (3, 2),
	   (4, 1);















