import mysql.connector

from control_classes import DBaserV2
from error_class import ErrorClass


class ProcDbaser(DBaserV2):

    def __init__(self):
        try:
            super(ProcDbaser, self).__init__()
        except mysql.connector.errors.DatabaseError:
            raise ErrorClass("Ошибка в открытии базы данных!")

    def get_procedures(self, index: int, included=True):
        if included:
            query = f"SELECT pl.string_id, lp.procedure_name, lp.procedure_cost " \
                    f"FROM procedures_list pl "\
                    f"JOIN legal_procedures lp ON pl.procedure_id = lp.procedure_id " \
                    f"WHERE case_id = {index} " \
                    f"ORDER BY lp.procedure_id;"
            self.cursor.execute(query)
        else:
            self.cursor.execute("SELECT * FROM legal_procedures;")
        return self.cursor.fetchall()

    def delete_procedure(self, string_id: int):
        try:
            self.cursor.execute(f"DELETE FROM procedures_list WHERE string_id = {string_id};")
        except mysql.connector.errors.DatabaseError as e:
            err_msg = self.get_error_message()
            if err_msg is None:
                raise ErrorClass(e.msg)
            else:
                raise ErrorClass(err_msg)

    def include_procedure(self, case_id: int, procedure_id: int):
        try:
            self.cursor.execute(f"INSERT INTO procedures_list (case_id, procedure_id) VALUES({case_id}, "
                                f"{procedure_id});")
        except mysql.connector.errors.DatabaseError as e:
            err_msg = self.get_error_message()
            if err_msg is None:
                raise ErrorClass(e.msg)
            else:
                raise ErrorClass(err_msg)

    def get_lawyers(self, case_id: int, included=True):
        if included:
            query = "SELECT string_id, CONCAT(name, ' ', surname, ' ', patronymic), cases_won, cases_lost " \
                    "FROM lawyers_list ll " \
                    "JOIN lawyers l ON ll.lawyer_id = l.lawyer_id " \
                    f"WHERE case_id = {case_id} " \
                    "ORDER BY l.lawyer_id;"
        else:
            query = "SELECT l.lawyer_id, CONCAT(name, ' ', surname, ' ', patronymic), cases_won, cases_lost " \
                    "FROM lawyers l " \
                    "WHERE l.lawyer_id NOT IN (SELECT lawyer_id " \
                    "						   FROM lawyers_list " \
                    f"                         WHERE case_id = {case_id}) " \
                    "ORDER BY l.lawyer_id;"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def include_lawyer(self, case_id: int, lawyer_id: int):
        try:
            self.cursor.execute(f"INSERT INTO lawyers_list (case_id, lawyer_id) VALUES({case_id}, {lawyer_id});")
        except mysql.connector.errors.DatabaseError as e:
            err_msg = self.get_error_message()
            if err_msg is None:
                raise ErrorClass(e.msg)
            else:
                raise ErrorClass(err_msg)

    def delete_lawyer(self, string_id: str):
        try:
            self.cursor.execute(f"DELETE FROM lawyers_list WHERE string_id = {string_id};")
        except mysql.connector.errors.DatabaseError as e:
            err_msg = self.get_error_message()
            if err_msg is None:
                raise ErrorClass(e.msg)
            else:
                raise ErrorClass(err_msg)


if __name__ == "__main__":
    db = ProcDbaser()
    data = db.get_lawyers(1, True)
    for row in data:
        print(row)
