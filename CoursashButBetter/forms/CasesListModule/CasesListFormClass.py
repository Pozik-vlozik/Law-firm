from ProceduresProcessingModule import ProceduresProcessingForm, ProcDbaser
from control_classes import custome_fill_table
from CasesListDb import CLDBaser, ErrorClass
from CasesListForm import Ui_CasesListWindow
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtGui
from docxtpl import DocxTemplate

import mysql.connector
import openpyxl


class CasesListFormClass(QMainWindow, Ui_CasesListWindow):

    def __init__(self):
        super(CasesListFormClass, self).__init__()

        self.setupUi(self)
        self.dBaser = CLDBaser()
        self.db = ProcDbaser()
        self.proc_form = ProceduresProcessingForm(self)
        self.msgBx = QtWidgets.QMessageBox()
        self.tableName = "cases"
        self.labels = ["Номер дела", "Клиент", "Дата начала дела", "Стоимость", "Описание"]

        self.deleteCaseBut.clicked.connect(self.delete_case)
        self.finishingCaseBut.clicked.connect(self.case_finishing)
        self.cancelFinishBut.clicked.connect(self.cancel_case_finishing)
        self.showProceduresBut.clicked.connect(self.show_procedures_form)
        self.showLawyersBut.clicked.connect(self.show_lawyers_form)
        self.tablesListCB.currentIndexChanged.connect(self.current_table_changed)
        self.finishCaseBut.clicked.connect(self.case_finish)
        self.showIntervalBut.clicked.connect(self.show_interval_cases)
        self.returBut.clicked.connect(self.return_but)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.setup_table()

    def show_interval_cases(self):
        start_date = get_date(self.startDate)
        end_date = get_date(self.endDate)
        if start_date > end_date:
            ErrorClass("Дата начала промежутка не может быть больше даты конца.").show_error_message(self)
            return
        if self.tablesListCB.currentIndex() == 0:
            cases = self.dBaser.get_cases()
        elif self.tablesListCB.currentIndex() == 1:
            cases = self.dBaser.get_cases(False)
        else:
            cases = self.dBaser.get_cases(True)
        val_cases = create_full_name([case for case in cases if start_date <= case[4] <= end_date])
        if len(val_cases) == 0:
            ErrorClass("Нет дел за данный промежуток времени!").show_error_message(self)
            return
        custome_fill_table(self.casesTable, val_cases, self.labels)

    def return_but(self):
        self.setup_table()

    def current_table_changed(self):
        self.setup_table()
        if self.tablesListCB.currentIndex() == 0:
            self.finishingCaseBut.setEnabled(False)
        elif self.tablesListCB.currentIndex() == 1:
            self.finishingCaseBut.setEnabled(True)
        elif self.tablesListCB.currentIndex() == 2:
            self.finishingCaseBut.setEnabled(False)

    def show_procedures_form(self):
        if len(self.casesTable.selectedItems()) == 1:
            if self.tablesListCB.currentIndex() in [0, 2]:
                self.proc_form.changable = False
            else:
                self.proc_form.changable = True
            self.proc_form.case_id = self.casesTable.item(self.casesTable.currentRow(), 0).text()
            self.proc_form.cur_table = "procedures"
            self.proc_form.show()
            self.hide()

    def show_lawyers_form(self):
        if len(self.casesTable.selectedItems()) == 1:
            if self.tablesListCB.currentIndex() in [0, 2]:
                self.proc_form.changable = False
            else:
                self.proc_form.changable = True
            self.proc_form.case_id = self.casesTable.item(self.casesTable.currentRow(), 0).text()
            self.proc_form.cur_table = "lawyers"
            self.proc_form.show()
            self.hide()

    def msgBox(self, title: str, text: str, icon=None):
        self.msgBx.setText(text)
        self.msgBx.setWindowTitle(title)
        if icon is not None:
            self.msgBx.setIcon(icon)
        self.msgBx.exec()

    def setup_table(self):
        finished = None
        if self.tablesListCB.currentIndex() == 1:
            finished = False
        elif self.tablesListCB.currentIndex() == 2:
            finished = True
        try:
            data = self.dBaser.get_cases(finished)
        except ErrorClass as e:
            e.show_error_message(self)
            return
        data = create_full_name(data)
        custome_fill_table(self.casesTable, data, self.labels)
        self.casesTable.setColumnHidden(0, True)

    def delete_case(self):
        if len(self.casesTable.selectedItems()) == 1:
            del_index = self.casesTable.item(self.casesTable.currentRow(), 0).text()
            try:
                self.dBaser.delete_data(self.tableName, del_index)
                self.setup_table()
            except ErrorClass as e:
                e.show_error_message(self)

    def case_finishing(self):
        if len(self.casesTable.selectedItems()) == 1:
            lawyers = self.dBaser.get_case_lawyers(self.casesTable.item(self.casesTable.currentRow(), 0).text())
            if len(lawyers) == 0:
                ErrorClass("Вы не можете завершить дело, в котором нет адвокатов!").show_error_message(self,
                                                                                                       "Внимание!")
                return
            self.finishingSW.setCurrentIndex(1)
            self.casesTable.setEnabled(False)
            self.deleteCaseBut.setEnabled(False)
            self.showLawyersBut.setEnabled(False)
            self.showProceduresBut.setEnabled(False)

    def cancel_case_finishing(self):
        self.finishingSW.setCurrentIndex(0)
        self.casesTable.setEnabled(True)
        self.deleteCaseBut.setEnabled(True)
        self.showLawyersBut.setEnabled(True)
        self.showProceduresBut.setEnabled(True)

    def case_finish(self):
        case_id = self.casesTable.item(self.casesTable.currentRow(), 0).text()
        state = self.finishStateCB.currentIndex() == 1
        finish_date = mysql.connector.Date(self.calendar.selectedDate().year(),
                                           self.calendar.selectedDate().month(),
                                           self.calendar.selectedDate().day())

        try:
            self.dBaser.finish_case(self.casesTable.item(self.casesTable.currentRow(), 0).text(), state, finish_date)
        except ErrorClass as e:
            e.show_error_message(self)
            return
        contract_number = str(case_id)
        client_name = self.casesTable.item(self.casesTable.currentRow(), 1).text()
        case_description = self.casesTable.item(self.casesTable.currentRow(), 4).text()
        lawyers = self.dBaser.get_case_lawyers(case_id)
        lawyer_names = ", ".join([" ".join(lawyer[1:4]) for lawyer in lawyers])
        case_price = self.dBaser.get_case_price(case_id)
        case_procedures = self.dBaser.get_case_procedures(case_id)
        if len(case_procedures) > 1:
            case_procedures = ", ".join(case_procedures)
        elif len(case_procedures) == 0:
            case_procedures = ""

        doc = DocxTemplate("template/contr_template.docx")
        context = {
            "contract_number": str(contract_number),
            "client_name": client_name,
            "case_description": case_description,
            "lawyer_names": lawyer_names,
            "case_price": str(case_price),
            "procedure_names": case_procedures
        }
        doc.render(context)

        try:
            doc.save(f"contracts/contract{str(contract_number)}.docx")
        except Exception:
            ErrorClass("Не удалось сохранить документ!\n"
                       " Проверьте наличие папки 'contracts'!").show_error_message(self)

        case_procedures = self.dBaser.get_case_procedures_with_cost(case_id)
        try:
            wb = openpyxl.load_workbook("template/procds_template.xlsx")
            sheet = wb["Лист1"]
            for i in range(len(case_procedures)):
                sheet[f"A{i + 2}"] = str(case_procedures[i][0])
                sheet[f"B{i + 2}"] = str(case_procedures[i][1])
            wb.save(f"contracts/contract{str(contract_number)}.xlsx")
        except Exception:
            ErrorClass("Не удалось найти шаблон документа!").show_error_message(self)

        self.cancel_case_finishing()
        self.setup_table()
        ErrorClass("Дело успешно завершено!").show_error_message(self, "Успех!")


def get_date(date_edit: QtWidgets.QDateEdit):
    date = mysql.connector.Date(
        date_edit.date().year(),
        date_edit.date().month(),
        date_edit.date().day()
    )
    return date


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
    MainWindow = CasesListFormClass()
    MainWindow.show()
    sys.exit(app.exec_())
