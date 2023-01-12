import mysql.connector

from control_classes import DBaserV2
from error_class import ErrorClass
import time


class CLDBaser(DBaserV2):

    def __init__(self):
        super(CLDBaser, self).__init__()

    def get_cases(self, finished=None):
        query = "SELECT " \
                "   c.case_id, " \
                "   cl.name, " \
                "   cl.surname, " \
                "   cl.patronymic," \
                "   c.case_start_date, " \
                "   c.nom_price, " \
                "   c.description " \
                "FROM cases c " \
                "JOIN clients cl" \
                "   ON c.client_id = cl.client_id "
        if finished is True:
            query += "WHERE c.case_end_date is not NULL"
        elif finished is False:
            query += "WHERE c.case_end_date is NULL"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def get_case_lawyers(self, case_id: int):
        query = "SELECT " \
                "   l.lawyer_id, " \
                "   l.name, " \
                "   l.surname, " \
                "   l.patronymic, " \
                "   l.cases_won, " \
                "   l.cases_lost " \
                "FROM lawyers_list ll " \
                "JOIN lawyers l " \
                "WHERE ll.lawyer_id = l.lawyer_id " \
                "	AND ll.case_id = {}".format(case_id)
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def get_case_price(self, case_id: int):
        query = f"""SELECT sum(procedure_cost) + (SELECT nom_price FROM cases WHERE case_id = {case_id})
                    FROM procedures_list pl
                    JOIN legal_procedures lp ON pl.procedure_id = lp.procedure_id
                    WHERE case_id = {case_id};"""
        self.cursor.execute(query)
        return self.cursor.fetchall()[0][0]

    def finish_case(self, case_id: int, won: bool, case_end_date: mysql.connector.Date):
        case_data = self.get_table_data("cases", None, 0, where=" WHERE case_id={} ".format(case_id))
        case_data = list(case_data[0])
        if case_data[2] > case_end_date:
            raise ErrorClass("Дата окончания дела должна быть до даты его начала!")
        case_data[3] = case_end_date
        if won:
            case_data[4] = 1
        else:
            case_data[4] = 0
        case_data = [str(x) for x in case_data]
        try:
            self.change_data("cases", case_data, case_id)
        except Exception:
            raise ErrorClass("Введены некорректные данные!")

    def get_case_procedures(self, case_id):
        query = f"""SELECT procedure_name
                    FROM procedures_list pl
                    JOIN legal_procedures lp ON pl.procedure_id = lp.procedure_id 
                    WHERE case_id = {case_id}
                    ORDER BY lp.procedure_id;"""
        self.cursor.execute(query)
        return [proc[0] for proc in self.cursor.fetchall()]

    def get_case_procedures_with_cost(self, case_id):
        query = f"""SELECT procedure_name, lp.procedure_cost
                    FROM procedures_list pl
                    JOIN legal_procedures lp ON pl.procedure_id = lp.procedure_id 
                    WHERE case_id = {case_id}
                    ORDER BY lp.procedure_id;"""
        self.cursor.execute(query)
        return self.cursor.fetchall()


if __name__ == "__main__":
    ins = CLDBaser()
    print(ins.get_case_procedures_with_cost(1))
    print(ins.get_case_price(1))
