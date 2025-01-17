# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/CasesListForm.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CasesListWindow(object):
    def setupUi(self, CasesListWindow):
        CasesListWindow.setObjectName("CasesListWindow")
        CasesListWindow.resize(1075, 588)
        CasesListWindow.setMouseTracking(False)
        CasesListWindow.setAutoFillBackground(False)
        CasesListWindow.setAnimated(True)
        CasesListWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(CasesListWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.casesTable = QtWidgets.QTableWidget(self.centralwidget)
        self.casesTable.setGeometry(QtCore.QRect(10, 10, 641, 461))
        self.casesTable.setObjectName("casesTable")
        self.casesTable.setColumnCount(0)
        self.casesTable.setRowCount(0)
        self.casesTable.horizontalHeader().setCascadingSectionResizes(False)
        self.casesTable.horizontalHeader().setDefaultSectionSize(1)
        self.casesTable.horizontalHeader().setMinimumSectionSize(0)
        self.casesTable.horizontalHeader().setSortIndicatorShown(True)
        self.casesTable.horizontalHeader().setStretchLastSection(False)
        self.showProceduresBut = QtWidgets.QPushButton(self.centralwidget)
        self.showProceduresBut.setEnabled(True)
        self.showProceduresBut.setGeometry(QtCore.QRect(320, 480, 171, 41))
        self.showProceduresBut.setObjectName("showProceduresBut")
        self.deleteCaseBut = QtWidgets.QPushButton(self.centralwidget)
        self.deleteCaseBut.setGeometry(QtCore.QRect(10, 480, 121, 41))
        self.deleteCaseBut.setObjectName("deleteCaseBut")
        self.finishingCaseBut = QtWidgets.QPushButton(self.centralwidget)
        self.finishingCaseBut.setEnabled(False)
        self.finishingCaseBut.setGeometry(QtCore.QRect(500, 480, 151, 41))
        self.finishingCaseBut.setObjectName("finishingCaseBut")
        self.finishingSW = QtWidgets.QStackedWidget(self.centralwidget)
        self.finishingSW.setGeometry(QtCore.QRect(670, 10, 401, 321))
        self.finishingSW.setObjectName("finishingSW")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.tablesListCB = QtWidgets.QComboBox(self.page)
        self.tablesListCB.setGeometry(QtCore.QRect(20, 20, 131, 31))
        self.tablesListCB.setObjectName("tablesListCB")
        self.tablesListCB.addItem("")
        self.tablesListCB.addItem("")
        self.tablesListCB.addItem("")
        self.label_2 = QtWidgets.QLabel(self.page)
        self.label_2.setGeometry(QtCore.QRect(20, 100, 21, 19))
        self.label_2.setObjectName("label_2")
        self.startDate = QtWidgets.QDateEdit(self.page)
        self.startDate.setGeometry(QtCore.QRect(40, 100, 110, 28))
        self.startDate.setObjectName("startDate")
        self.label_3 = QtWidgets.QLabel(self.page)
        self.label_3.setGeometry(QtCore.QRect(160, 100, 31, 19))
        self.label_3.setObjectName("label_3")
        self.endDate = QtWidgets.QDateEdit(self.page)
        self.endDate.setGeometry(QtCore.QRect(190, 100, 110, 28))
        self.endDate.setObjectName("endDate")
        self.showIntervalBut = QtWidgets.QPushButton(self.page)
        self.showIntervalBut.setGeometry(QtCore.QRect(310, 80, 81, 31))
        self.showIntervalBut.setObjectName("showIntervalBut")
        self.label_4 = QtWidgets.QLabel(self.page)
        self.label_4.setGeometry(QtCore.QRect(20, 70, 151, 19))
        self.label_4.setObjectName("label_4")
        self.returBut = QtWidgets.QPushButton(self.page)
        self.returBut.setEnabled(True)
        self.returBut.setGeometry(QtCore.QRect(310, 120, 81, 31))
        self.returBut.setObjectName("returBut")
        self.finishingSW.addWidget(self.page)
        self.calendarPage = QtWidgets.QWidget()
        self.calendarPage.setObjectName("calendarPage")
        self.calendar = QtWidgets.QCalendarWidget(self.calendarPage)
        self.calendar.setGeometry(QtCore.QRect(0, 40, 392, 221))
        self.calendar.setObjectName("calendar")
        self.label = QtWidgets.QLabel(self.calendarPage)
        self.label.setGeometry(QtCore.QRect(10, 10, 251, 16))
        self.label.setObjectName("label")
        self.finishCaseBut = QtWidgets.QPushButton(self.calendarPage)
        self.finishCaseBut.setGeometry(QtCore.QRect(270, 270, 111, 31))
        self.finishCaseBut.setObjectName("finishCaseBut")
        self.cancelFinishBut = QtWidgets.QPushButton(self.calendarPage)
        self.cancelFinishBut.setGeometry(QtCore.QRect(150, 270, 111, 31))
        self.cancelFinishBut.setObjectName("cancelFinishBut")
        self.finishStateCB = QtWidgets.QComboBox(self.calendarPage)
        self.finishStateCB.setGeometry(QtCore.QRect(10, 270, 131, 31))
        self.finishStateCB.setObjectName("finishStateCB")
        self.finishStateCB.addItem("")
        self.finishStateCB.addItem("")
        self.finishingSW.addWidget(self.calendarPage)
        self.backToMainBut = QtWidgets.QPushButton(self.centralwidget)
        self.backToMainBut.setGeometry(QtCore.QRect(940, 490, 111, 41))
        self.backToMainBut.setObjectName("backToMainBut")
        self.showLawyersBut = QtWidgets.QPushButton(self.centralwidget)
        self.showLawyersBut.setEnabled(True)
        self.showLawyersBut.setGeometry(QtCore.QRect(140, 480, 171, 41))
        self.showLawyersBut.setObjectName("showLawyersBut")
        CasesListWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(CasesListWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1075, 24))
        self.menubar.setObjectName("menubar")
        CasesListWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(CasesListWindow)
        self.statusbar.setObjectName("statusbar")
        CasesListWindow.setStatusBar(self.statusbar)

        self.retranslateUi(CasesListWindow)
        self.finishingSW.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CasesListWindow)

    def retranslateUi(self, CasesListWindow):
        _translate = QtCore.QCoreApplication.translate
        CasesListWindow.setWindowTitle(_translate("CasesListWindow", "Список дел"))
        self.casesTable.setSortingEnabled(True)
        self.showProceduresBut.setText(_translate("CasesListWindow", "Посмотреть процедуры"))
        self.deleteCaseBut.setText(_translate("CasesListWindow", "Удалить дело"))
        self.finishingCaseBut.setText(_translate("CasesListWindow", "Завершение дела"))
        self.tablesListCB.setItemText(0, _translate("CasesListWindow", "Все дела"))
        self.tablesListCB.setItemText(1, _translate("CasesListWindow", "Активные дела"))
        self.tablesListCB.setItemText(2, _translate("CasesListWindow", "Завершенные дела"))
        self.label_2.setText(_translate("CasesListWindow", "С"))
        self.label_3.setText(_translate("CasesListWindow", "ПО"))
        self.showIntervalBut.setText(_translate("CasesListWindow", "Показать"))
        self.label_4.setText(_translate("CasesListWindow", "Дела за промежуток:"))
        self.returBut.setText(_translate("CasesListWindow", "Вернуть"))
        self.label.setText(_translate("CasesListWindow", "Выберите дату завершения дела:"))
        self.finishCaseBut.setText(_translate("CasesListWindow", "Завершить"))
        self.cancelFinishBut.setText(_translate("CasesListWindow", "Отмена"))
        self.finishStateCB.setItemText(0, _translate("CasesListWindow", "Дело проиграно"))
        self.finishStateCB.setItemText(1, _translate("CasesListWindow", "Дело выиграно"))
        self.backToMainBut.setText(_translate("CasesListWindow", "Назад"))
        self.showLawyersBut.setText(_translate("CasesListWindow", "Посмотреть адвокатов"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CasesListWindow = QtWidgets.QMainWindow()
    ui = Ui_CasesListWindow()
    ui.setupUi(CasesListWindow)
    CasesListWindow.show()
    sys.exit(app.exec_())
