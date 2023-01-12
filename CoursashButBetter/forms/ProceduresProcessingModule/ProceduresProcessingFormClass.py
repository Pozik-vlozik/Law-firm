from ProceduresProcessingForm import Ui_ProceduresProcessingForm
from ProceduresProcessingDb import ProcDbaser, ErrorClass
from control_classes import custome_fill_table
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtGui


class ProceduresProcessingForm(QMainWindow, Ui_ProceduresProcessingForm):

    def __init__(self, parent=None):
        super(ProceduresProcessingForm, self).__init__()
        self.case_id = 1
        self.setupUi(self)
        self.dBaser = ProcDbaser()
        self.cur_table = ""
        self.changable = False
        self.proc_headers = ["ID", "Название процедуры", "Стоимость"]
        self.law_headers = ["ID", "Имя адвоката", "Выиграно дел", "Проиграно дел"]

        self.parent_form = parent

        self.backToCasesListBut.clicked.connect(self.back_to_cases_list_form)
        self.unincludeProcedureBut.clicked.connect(self.uninclude_but)
        self.includeProcedureBut.clicked.connect(self.include_but)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        if self.changable:
            self.includeProcedureBut.setEnabled(True)
            self.unincludeProcedureBut.setEnabled(True)
            self.nonIncludedProceduresTW.setEnabled(True)
        else:
            self.includeProcedureBut.setEnabled(False)
            self.unincludeProcedureBut.setEnabled(False)
            self.nonIncludedProceduresTW.setEnabled(False)

        if self.cur_table == "procedures":
            self.includedLB.setText("Невключенные процедуры")
            self.nonIncludedLB.setText("Включенные процедуры")
            self.fill_proc_tables()
        else:
            self.includedLB.setText("Невключенные адвокаты")
            self.nonIncludedLB.setText("Включенные адвокаты")
            self.fill_lawyers_tables()

    def include_but(self):
        indexes = set()
        for row_index in self.nonIncludedProceduresTW.selectedIndexes():
            indexes.add(int(self.nonIncludedProceduresTW.item(row_index.row(), 0).text()))
        for index in indexes:
            if self.cur_table == "procedures":
                self.include_procedure(index)
            else:
                self.include_lawyer(index)

    def uninclude_but(self):
        indexes = set()
        for row_index in self.includedProceduresTW.selectedIndexes():
            indexes.add(int(self.includedProceduresTW.item(row_index.row(), 0).text()))
        for index in indexes:
            if self.cur_table == "procedures":
                self.uninclude_procedure(index)
            else:
                self.uninclude_lawyer(index)

        # Working with procedures

    def uninclude_procedure(self, index):
        try:
            self.dBaser.delete_procedure(index)
            self.fill_proc_tables()
        except ErrorClass as e:
            e.show_error_message(self)

    def include_procedure(self, index):
        try:
            self.dBaser.include_procedure(self.case_id, index)
            self.fill_proc_tables()
        except ErrorClass as e:
            e.show_error_message(self)

    def back_to_cases_list_form(self):
        if self.parent_form is not None:
            self.parent_form.show()
            self.hide()

    def fill_incl_proc_table(self):
        try:
            data = self.dBaser.get_procedures(self.case_id, included=True)
            custome_fill_table(self.includedProceduresTW, data, self.proc_headers)
        except ErrorClass as e:
            e.show_error_message(self)

    def fill_non_incl_proc_table(self):
        try:
            data = self.dBaser.get_procedures(self.case_id, included=False)
            custome_fill_table(self.nonIncludedProceduresTW, data, self.proc_headers)
        except ErrorClass as e:
            e.show_error_message(self)

    def fill_proc_tables(self):
        self.fill_incl_proc_table()
        self.fill_non_incl_proc_table()
        self.includedProceduresTW.setColumnHidden(0, True)
        self.nonIncludedProceduresTW.setColumnHidden(0, True)

        # Working with lawyers

    def fill_incl_lawyers_table(self):
        try:
            data = self.dBaser.get_lawyers(self.case_id, True)
            custome_fill_table(self.includedProceduresTW, data, self.law_headers)
        except ErrorClass as e:
            e.show_error_message(self)

    def fill_non_incl_lawyers_table(self):
        try:
            data = self.dBaser.get_lawyers(self.case_id, False)
            custome_fill_table(self.nonIncludedProceduresTW, data, self.law_headers)
        except ErrorClass as e:
            e.show_error_message(self)

    def fill_lawyers_tables(self):
        self.fill_incl_lawyers_table()
        self.fill_non_incl_lawyers_table()
        self.includedProceduresTW.setColumnHidden(0, True)
        self.nonIncludedProceduresTW.setColumnHidden(0, True)

    def include_lawyer(self, index):
        try:
            self.dBaser.include_lawyer(self.case_id, index)
            self.fill_lawyers_tables()
        except ErrorClass as e:
            e.show_error_message(self)

    def uninclude_lawyer(self, index):
        try:
            self.dBaser.delete_lawyer(index)
            self.fill_lawyers_tables()
        except ErrorClass as e:
            e.show_error_message(self)


if __name__ == "__main__":
    import sys
    print("Executing from form class")
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = ProceduresProcessingForm(None)
    MainWindow.show()
    sys.exit(app.exec_())
