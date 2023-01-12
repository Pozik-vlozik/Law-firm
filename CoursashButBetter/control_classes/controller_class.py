from forms import MainFormClass, CasesListFormClass, DataChangeFormClass, NewCaseClass


class Controller:
    def __init__(self):

        self.mainForm = MainFormClass()
        self.casesListForm = CasesListFormClass()
        self.dataChangeForm = DataChangeFormClass()
        self.newCaseForm = NewCaseClass()

        # Main form properties
        self.mainForm.casesListBut.clicked.connect(self.show_cases_list_form)
        self.mainForm.exitBut.clicked.connect(lambda: self.mainForm.close())
        self.mainForm.changeDataBut.clicked.connect(self.show_change_data_form)

        # Data change form properties
        self.dataChangeForm.backToMainBut.clicked.connect(self.back_from_changes_to_main)

        # Cases list form properties
        self.casesListForm.backToMainBut.clicked.connect(self.back_from_cases_list_form)

        # New case form properties
        self.newCaseForm.backToMainBut.clicked.connect(self.back_from_new_case)
        self.mainForm.newCaseBut.clicked.connect(self.show_new_case_form)

    def start_programm(self):
        self.mainForm.show()

    def show_new_case_form(self):
        self.newCaseForm.show()
        self.mainForm.hide()

    def show_cases_list_form(self):
        self.casesListForm.show()
        self.mainForm.hide()

    def show_change_data_form(self):
        self.dataChangeForm.show()
        self.mainForm.hide()

    def back_from_changes_to_main(self):
        self.dataChangeForm.hide()
        self.mainForm.show()

    def back_from_cases_list_form(self):
        self.casesListForm.hide()
        self.mainForm.show()

    def back_from_new_case(self):
        self.newCaseForm.hide()
        self.mainForm.show()
