from error_class import ErrorClass
from temp import cols_names_rus
from PyQt5 import QtWidgets
import mysql.connector


class DBaserV2:

    def __init__(self, host="localhost", user="root", passwd="password", database="LawersFirm"):
        try:
            self.db = mysql.connector.connect(
                host=host,
                user=user,
                passwd=passwd,
                database=database,
                autocommit=True
            )
            self.cursor = self.db.cursor()
        except mysql.connector.errors.DatabaseError:
            raise ErrorClass("Невозможно подключиться к базе данных!")

    def simple_select(self, query: str):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_error_message(self):
        self.cursor.execute("SELECT @message")
        return self.cursor.fetchall()[0][0]

    def get_table_names(self):
        self.cursor.execute("SHOW FULL tables WHERE Table_Type = 'BASE TABLE'")
        return [tname[0] for tname in self.cursor.fetchall()]

    def get_table_headers(self, table_name: str):
        self.cursor.execute("DESCRIBE {}".format(table_name))
        return [tname[0] for tname in self.cursor.fetchall()]

    def get_table_data(self, table_name: str, sorting_by=None, limit=0, where=None):
        query = "SELECT * FROM {} ".format(table_name)
        if where is not None:
            query += where
        if sorting_by is not None:
            query += " ORDER BY {} ".format(sorting_by)
        if limit != 0:
            query += " LIMIT {} ".format(limit)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def add_data(self, table_name: str, data: list, columns=None):
        if columns is None:
            cols = self.get_table_headers(table_name)
            cols = ", ".join([col for col in cols[1:]])
        else:
            cols = ", ".join([col for col in columns])
        values = []
        for dat in data:
            if data is not None:
                values.append("'" + str(dat) + "'")
            else:
                values.append(dat)
        values = ", ".join(values)
        query = f"INSERT INTO {table_name} ({cols}) VALUES ({values})"
        try:
            self.cursor.execute(query)
        except mysql.connector.errors.DatabaseError as e:
            err_msg = self.get_error_message()
            if err_msg is None:
                raise ErrorClass(e.msg)
            else:
                raise ErrorClass(err_msg)

    def change_data(self, table_name: str, data: list, index: int):
        query = "UPDATE {} SET ".format(table_name)
        values = ["'" + val + "'" for val in data[1:]]
        columns = self.get_table_headers(table_name)
        updated_columns = []
        row_id = columns[0]
        for val in zip(columns[1:], values):
            updated_columns.append(val[0] + " = " + val[1])
        query += ", ".join(updated_columns)
        query += " WHERE {} = {}".format(row_id, index)
        try:
            self.cursor.execute(query)
        except mysql.connector.errors.DatabaseError as e:
            err_msg = self.get_error_message()
            if err_msg is None:
                raise ErrorClass(e.msg)
            else:
                raise ErrorClass(err_msg)

    def delete_data(self, table_name: str, index: int):
        row_id = self.get_table_headers(table_name)[0]
        query = "DELETE FROM {} WHERE {}={}".format(table_name, row_id, index)
        self.cursor.execute(query)
        self.db.commit()

    def get_client_cases(self, client_id: int):
        query = f"SELECT case_id FROM cases WHERE client_id = {client_id}"
        self.cursor.execute(query)
        return [x[0] for x in self.cursor.fetchall()]

    def get_client_procedures_amount(self, client_id: int):
        query = f"""SELECT count(procedure_id)
                    FROM procedures_list 
                    WHERE case_id IN
                        (SELECT case_id 
                        FROM cases 
                        WHERE client_id = {client_id})"""
        self.cursor.execute(query)
        amount = self.cursor.fetchall()
        return amount[0][0]

    def get_laywer_cases(self, lawyer_id: int):
        query = f"""SELECT * 
                    FROM cases 
                    WHERE case_id IN
                        (SELECT case_id 
                         FROM lawyers_list 
                         WHERE lawyer_id = {lawyer_id})"""
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_case_client(self, case_id: int):
        query = f"""SELECT CONCAT(name, " ", surname, " ", patronimyc) 
                    FROM clients
                        WHERE client_id IN
                        (SELECT client_id 
                        FROM cases 
                        WHERE case_id = {case_id})"""
        self.cursor.execute(query)
        return self.cursor.fetchall()[0][0]


def fill_table(table_name: str, table: QtWidgets.QTableWidget, dbaser: DBaserV2):
    labels = dbaser.get_table_headers(table_name)
    labels = [cols_names_rus[name] for name in labels]
    data = dbaser.get_table_data(table_name)
    if len(data) == 0:
        raise ErrorClass("Отсутствуют данные для отображения!")
    custome_fill_table(table, data, labels)


def custome_fill_table(table: QtWidgets.QTableWidget, data: list, labels: list):
    table.setColumnCount(len(labels))
    table.setHorizontalHeaderLabels(labels)

    header = table.horizontalHeader()
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
    for i in range(1, len(labels)):
        header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

    rows_count = len(data)
    table.setRowCount(rows_count)
    for row in range(rows_count):
        for column in range(len(labels)):
            table.setItem(row, column, QtWidgets.QTableWidgetItem(str(data[row][column])))
    # table.resizeRowsToContents()
    # table.resizeColumnsToContents()


if __name__ == "__main__":
    dBaser = DBaserV2()
    for case in dBaser.get_table_data("cases"):
        print(case)


