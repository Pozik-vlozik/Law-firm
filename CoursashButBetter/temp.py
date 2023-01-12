table_names_rus = {"cases": "Дела",
                   "clients": "Клиенты",
                   "lawyers_list": "Список адвокатов",
                   "lawyers": "Адвокаты",
                   "procedures_list": "Списко процедур",
                   "legal_procedures": "Юридические процедуры"
                   }

cols_names_rus = {"case_id": "Номер дела",
                  "lawyer_id": "Номер адвоката",
                  "client_id": "Номер клиента",
                  "case_start_date": "Дата начала",
                  "case_end_date": "Дата окончания",
                  "case_won": "Дело выиграно",
                  "name": "Имя",
                  "surname": "Фамилия",
                  "patronymic": "Отчество",
                  "string_id": "Номер строки",
                  "cases_won": "Дел выиграно",
                  "cases_lost": "Дел проиграно",
                  "procedure_id": "Номер процедуры",
                  "procedure_name": "Наименование процедуры",
                  "procedure_cost": "Стоимость процедуры",
                  "passport_number": "Номер паспорта",
                  "description": "Описание"
                  }
table_names_eng = {v: k for k, v in table_names_rus.items()}
cols_names_eng = {v: k for k, v in cols_names_rus.items()}
