from control_classes import fill_table, DBaserV2, custome_fill_table
from temp import table_names_eng, cols_names_rus, cols_names_eng
from DataChangeForm import Ui_DataChange
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtGui
from error_class import ErrorClass

import matplotlib.pyplot as plt
import time


class DataChangeFormClass(QMainWindow, Ui_DataChange):
    def __init__(self):
        super(DataChangeFormClass, self).__init__()
        self.setupUi(self)
        self.dBaser = DBaserV2()
        self.msgBx = QtWidgets.QMessageBox()

        self.tableForChangeCB.currentTextChanged.connect(self.change_table_data)
        self.addDataBut.clicked.connect(self.add_data)
        self.row_index_for_change = -1
        self.tableWidget.itemClicked.connect(self.row_selected)
        self.changeDataBut.clicked.connect(self.change_data)
        self.deleteDataBut.clicked.connect(self.delete_data)
        self.clientCasesBut.clicked.connect(self.show_client_cases)
        self.proceduresSortBut.clicked.connect(self.sort_clients)
        self.lawyersDiagrammBut.clicked.connect(self.lawyers_diagram)
        self.searchLE.textChanged.connect(self.text_changed)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.change_table_data()

    def text_changed(self):
        cur_table = self.tableForChangeCB.currentText()
        labels = self.dBaser.get_table_headers(table_names_eng[cur_table])
        labels = [cols_names_rus[label] for label in labels]
        column = cols_names_eng[self.searchCB.currentText()]
        like = "%" + self.searchLE.text().lower() + "%"
        data = self.dBaser.get_table_data(table_names_eng[cur_table], where=f" WHERE (LOWER({column}) LIKE '{like}')")
        custome_fill_table(self.tableWidget, data, labels)

    def lawyers_diagram(self):
        cases_amount = []
        laywers = []
        start_date = time.strptime(self.startDate.text(), "%d.%m.%Y")
        end_date = time.strptime(self.endDate.text(), "%d.%m.%Y")
        if start_date > end_date:
            ErrorClass("Дата начала промежутка не может быть больше даты конца.").show_error_message(self)
            return
        for i in range(self.tableWidget.rowCount()):
            cases = self.dBaser.get_laywer_cases(self.tableWidget.item(i, 0).text())
            dates = []
            for case in cases:
                if start_date <= time.strptime(case[2].strftime("%d-%m-%Y"), "%d-%m-%Y") <= end_date:
                    dates.append(case[2])
            cases_amount.append(dates.copy())
            dates.clear()
            laywers.append(self.tableWidget.item(i, 2).text())
        cases_amount = [len(case) for case in cases_amount]
        if sum(cases_amount) != 0:
            plt.bar(laywers, cases_amount)
            for i in range(len(cases_amount)):
                plt.text(laywers[i], cases_amount[i], str(cases_amount[i]))
            plt.title = "Дела адвокатов за указанный период"
            plt.show()
        else:
            ErrorClass("За данный промежуток времени не было заведено ни одного дела").show_error_message(self)

    def sort_clients(self):
        proc_amounts = {}
        try:
            for i in range(self.tableWidget.rowCount()):
                client_id = int(self.tableWidget.item(i, 0).text())
                proc_amounts.setdefault(str(client_id), self.dBaser.get_client_procedures_amount(client_id))
        except ErrorClass as e:
            e.show_error_message(self)
        for i in range(self.tableWidget.rowCount() - 1, 0, -1):
            for index in range(i):
                if proc_amounts[self.tableWidget.item(index, 0).text()] < \
                        proc_amounts[self.tableWidget.item(index + 1, 0).text()]:
                    swap_rows(self.tableWidget, index, index + 1)

    def show_client_cases(self):
        if len(self.tableWidget.selectedItems()) == 1:
            info = "Все дела по данному клиенту:\n"
            cases = self.dBaser.get_client_cases(self.tableWidget.item(self.tableWidget.currentRow(), 0).text())
            if len(cases) != 0:
                cases = [str(case) for case in cases]
                info += ", ".join(cases)
            else:
                info += "У данного клиента отсутствуют дела\n"
            ErrorClass(info).show_error_message(self)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.stackOfButs.setCurrentIndex(0)
        self.row_index_for_change = -1

    def msgBox(self, title: str, text: str, icon=None):
        self.msgBx.setText(text)
        self.msgBx.setWindowTitle(title)
        if icon is not None:
            self.msgBx.setIcon(icon)
        self.msgBx.exec()

    def row_selected(self):
        self.row_index_for_change = self.tableWidget.item(self.tableWidget.currentRow(), 0).text()
        values = []
        for i in range(self.tableWidget.columnCount()):
            values.append(self.tableWidget.item(self.tableWidget.currentRow(), i).text())

        index = 1
        for widget in self.stackOfLEs.currentWidget().children():
            widget.setText(values[index])
            index += 1
        self.stackOfButs.setCurrentIndex(1)

    def change_table_data(self):
        cur_text = self.tableForChangeCB.currentText()
        if cur_text == "Клиенты":
            self.clientCasesBut.setVisible(True)
            self.proceduresSortBut.setVisible(True)
        else:
            self.clientCasesBut.setVisible(False)
            self.proceduresSortBut.setVisible(False)
        if cur_text == "Адвокаты":
            self.groupBox.setVisible(True)
        else:
            self.groupBox.setVisible(False)

        try:
            fill_table(table_names_eng[cur_text],
                       self.tableWidget,
                       self.dBaser)
            self.tableWidget.setColumnHidden(0, True)
        except ErrorClass as e:
            e.show_error_message(self)
            return

        self.searchCB.clear()
        labels = self.dBaser.get_table_headers(table_names_eng[cur_text])
        for label in labels[1::]:
            self.searchCB.addItem(cols_names_rus[label])
        self.stackOfLEs.setCurrentIndex(self.tableForChangeCB.findText(cur_text))
        self.stackOfButs.setCurrentIndex(0)
        self.row_index_for_change = -1
        self.clear_text()

    def add_data(self):
        values = []
        for widget in self.stackOfLEs.currentWidget().children():
            if isinstance(widget, QtWidgets.QLineEdit):
                values.append(widget.text())
            elif isinstance(widget, QtWidgets.QTextEdit):
                values.append(widget.toPlainText())
        table_name = table_names_eng[self.tableForChangeCB.currentText()]
        try:
            self.dBaser.add_data(table_name, values)
            fill_table(table_name, self.tableWidget, self.dBaser)
        except ErrorClass as e:
            e.show_error_message(self)
            return
        self.clear_text()

    def change_data(self):
        values = []
        for widget in self.stackOfLEs.currentWidget().children():
            if isinstance(widget, QtWidgets.QLineEdit):
                values.append(widget.text())
            elif isinstance(widget, QtWidgets.QTextEdit):
                values.append(widget.toPlainText())
        table_name = table_names_eng[self.tableForChangeCB.currentText()]
        values.insert(0, self.row_index_for_change)
        try:
            self.dBaser.change_data(table_name, values, self.row_index_for_change)
            fill_table(table_name, self.tableWidget, self.dBaser)
        except ErrorClass as e:
            e.show_error_message(self)
            return

    def delete_data(self):
        table_name = table_names_eng[self.tableForChangeCB.currentText()]
        try:
            self.dBaser.delete_data(table_name, self.row_index_for_change)
            fill_table(table_name, self.tableWidget, self.dBaser)
        except ErrorClass as e:
            e.show_error_message(self)
        self.stackOfButs.setCurrentIndex(0)
        self.row_index_for_change = -1
        self.clear_text()

    def clear_text(self):
        for widget in self.stackOfLEs.currentWidget().children():
            widget.clear()


def swap_rows(table: QtWidgets.QTableWidget, first: int, second: int):
    items = [[], []]
    for i in range(table.columnCount()):
        items[0].append(table.item(first, i).text())
        items[1].append(table.item(second, i).text())
    for i in range(table.columnCount()):
        table.setItem(first, i, QtWidgets.QTableWidgetItem(items[1][i]))
        table.setItem(second, i, QtWidgets.QTableWidgetItem(items[0][i]))


if __name__ == "__main__":
    import sys
    print("Executing from form class")
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = DataChangeFormClass()
    MainWindow.show()
    sys.exit(app.exec_())
