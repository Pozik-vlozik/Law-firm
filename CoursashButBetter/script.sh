#!/bin/bash
pyuic5 -x uis/MainForm.ui > forms/MainFormModule/MainForm.py
pyuic5 -x uis/CasesListForm.ui > forms/CasesListModule/CasesListForm.py
pyuic5 -x uis/DataChangeForm.ui > forms/DataChangeModule/DataChangeForm.py
pyuic5 -x uis/NewCaseCreateForm.ui > forms/NewCaseFormModule/NewCaseCreateForm.py
pyuic5 -x uis/ProceduresProcessingForm.ui > forms/ProceduresProcessingModule/ProceduresProcessingForm.py
