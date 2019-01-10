# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gradebook.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

"""
TODO:
Implement the new functionality
Implement the close functionality (make sure to ask about saving!)
Implement calculating grades
Add undo and redo functionality
Make the delete key delete selected items
"""

import json

from PyQt5 import QtCore, QtGui, QtWidgets


class Course(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, data = ["New Course","",""], *__args):
        super().__init__(parent, data)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.setFont(0, font)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)


class AssignmentType(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, data = ["New Assignment Type","",""], *__args):
        super().__init__(parent, data)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.setFont(0, font)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)


class Assignment(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, data = ["New Assignment","",""], *__args):
        super().__init__(parent, data)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)


class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(912, 647)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setMinimumSize(QtCore.QSize(900, 600))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.treeWidget.setFont(font)
        self.treeWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.treeWidget.setMouseTracking(False)
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.treeWidget.setAutoFillBackground(False)
        self.treeWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.treeWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.treeWidget.setUniformRowHeights(False)
        self.treeWidget.setAnimated(True)
        self.treeWidget.setWordWrap(True)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.treeWidget.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        self.treeWidget.headerItem().setTextAlignment(2, QtCore.Qt.AlignCenter)
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.treeWidget.header().setDefaultSectionSize(275)
        self.treeWidget.header().setMinimumSectionSize(50)
        self.treeWidget.header().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.treeWidget)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 912, 35))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction(self)
        self.actionOpen.setObjectName("actionOpen")
        self.actionClose = QtWidgets.QAction(self)
        self.actionClose.setObjectName("actionClose")
        self.actionNew = QtWidgets.QAction(self)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(self)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(self)
        self.actionSave_as.setObjectName("actionSave_as")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.courses = []
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.openMenu)

        self.actionSave.triggered.connect(self.saveJSON)
        self.actionOpen.triggered.connect(self.readJSON)
        self.actionSave_as.triggered.connect(self.saveAsJSON)
        self.actionNew.triggered.connect(self.clearPage)

        self.filename = None

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Course"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "Weight"))
        self.treeWidget.headerItem().setText(2, _translate("MainWindow", "Grade"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.actionOpen.setText(_translate("MainWindow", "&Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionClose.setText(_translate("MainWindow", "&Close"))
        self.actionNew.setText(_translate("MainWindow", "&New"))
        self.actionSave.setText(_translate("MainWindow", "&Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_as.setText(_translate("MainWindow", "Sa&ve as..."))
        self.actionSave_as.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))


    def clearPage(self):
        self.treeWidget.clear()
        self.courses = []
        self.filename = []


    def openMenu(self, position):
        menu = QtWidgets.QMenu(self)
        indices = self.treeWidget.selectedIndexes()

        level = 0
        if not indices:
            menu.addAction(self.tr("Add New Course"))

        else:
            i = indices[0]
            while i.parent().isValid():
                i = i.parent()
                level += 1
            if level == 0:
                menu.addAction(self.tr("Add New Course"))
                menu.addAction(self.tr("Add New Assignment Type"))
                menu.addAction(self.tr("Remove Selected Course"))
            elif level == 1:
                menu.addAction(self.tr("Add New Assignment"))
                menu.addAction(self.tr("Remove Selected Assignment Type"))
            elif level == 2:
                menu.addAction(self.tr("Remove Assignment"))

        action = menu.exec_(self.treeWidget.viewport().mapToGlobal(position))
        if action:
            action = action.text()
            if action == "Add New Course":
                self.courses.append(Course(self.treeWidget))
            elif action == "Add New Assignment Type":
                course = self.treeWidget.itemFromIndex(indices[0])
                course.addChild(AssignmentType(course))
            elif action == "Add New Assignment":
                assignment_type = self.treeWidget.itemFromIndex(indices[0])
                assignment_type.addChild(Assignment(assignment_type))
            else:
                root = self.treeWidget.invisibleRootItem()
                for item in self.treeWidget.selectedItems():
                    (item.parent() or root).removeChild(item)


    def saveJSON(self):
        self.filename = self.save(self.filename)

    def saveAsJSON(self):
        self.save()

    def save(self,filename=None):
        if not filename:  # if a file hasn't been opened yet (save as or new file)
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                                     "Gradebook Files (*.grdb)")
        if filename:
            data = {"Course": []}
            for course in self.courses:
                c_data = {"Name": course.text(0), "Weight": course.text(1), "Grade": course.text(2), "Types": []}
                for i in range(course.childCount()):
                    t = course.child(i)
                    t_data = {"Name": t.text(0), "Weight": t.text(1), "Grade": t.text(2), "Assignments": []}
                    for j in range(t.childCount()):
                        ass = t.child(j)
                        t_data["Assignments"].append({"Name": ass.text(0), "Weight": ass.text(1), "Grade": ass.text(2)})
                    c_data["Types"].append(t_data)
                data["Course"].append(c_data)

            with open(filename.replace(".grdb","")+".grdb", "w+") as f:
                json.dump(data, f)
        return filename

    def readJSON(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Gradebook Files (*.grdb)")
        if filename:
            with open(filename) as json_file:
                self.clearPage()
                self.filename = filename
                data = json.load(json_file)



                for course_dict in data["Course"]:
                    course = Course(self.treeWidget,[course_dict["Name"],course_dict["Weight"],course_dict["Grade"]])
                    for type_dict in course_dict["Types"]:
                        t = AssignmentType(course,[type_dict["Name"],type_dict["Weight"],type_dict["Grade"]])
                        for assignment in type_dict["Assignments"]:
                            t.addChild(Assignment(t,[assignment["Name"],assignment["Weight"],assignment["Grade"]]))
                        course.addChild(t)
                    self.courses.append(course)



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.setupUi()
    ui.show()
    sys.exit(app.exec_())
