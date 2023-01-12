from control_classes import custome_fill_table, DBaserV2
from error_class import ErrorClass
from NewCaseCreateForm import Ui_NewCaseForm
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtGui


class NewCaseClass(QMainWindow, Ui_NewCaseForm):
    def __init__(self):
        super(NewCaseClass, self).__init__()
        self.setupUi(self)
        self.dBaser = DBaserV2()
        self.client_id = -1
        self.labels = ["Номер клиента", "Имя клиента", "Номер паспорта"]

        self.continueBut.clicked.connect(self.select_client)
        self.backToClientChoiceBut.clicked.connect(self.back_to_client_select)
        self.addCaseBut.clicked.connect(self.create_case)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.fill_table()

    def fill_table(self):
        try:
            data = self.dBaser.get_table_data("clients")
        except ErrorClass as e:
            e.show_error_message(self)
            return
        data = create_full_name(data)
        custome_fill_table(self.clientsTable, data, self.labels)
        self.clientsTable.setColumnHidden(0, True)

    def select_client(self):
        if len(self.clientsTable.selectedItems()) == 1:
            self.client_id = self.clientsTable.item(self.clientsTable.currentRow(), 0).text()
            self.caseDataSW.setCurrentIndex(1)

    def back_to_client_select(self):
        self.caseDataSW.setCurrentIndex(0)
        self.caseDescrLe.clear()
        self.nominalPriceLE.clear()

    def create_case(self):
        nom_price = self.nominalPriceLE.text()
        date = self.calendarCW.selectedDate().toString("yyyy-MM-dd")
        description = self.caseDescrLe.toPlainText()
        if len(description) == 0:
            ErrorClass("Дело должно содержать описание!").show_error_message(self)
            return
        try:
            self.dBaser.add_data("cases",
                                 [self.client_id, date, nom_price, description],
                                 ["client_id", "case_start_date", "nom_price", "description"])
        except ErrorClass as e:
            e.show_error_message(self)
            return
        self.back_to_client_select()
        ErrorClass("Дело успешно добавлено!").show_error_message(self, "Успех!")


def is_digit(num: str):
    if not num.isdigit():
        return False
    try:
        float(num)
    except ValueError:
        return False
    return True


def create_full_name(data: list):
    for i in range(len(data)):
        full_name = " ".join(data[i][1:4])
        data[i] = [x for i, x in enumerate(data[i]) if i not in [1, 2, 3]]
        data[i].insert(1, full_name)
    return data


if __name__ == "__main__":
    import sys
    print("Executing from form class")
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = NewCaseClass()
    MainWindow.show()
    sys.exit(app.exec_())
