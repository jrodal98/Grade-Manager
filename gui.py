# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gradebook.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

"""
TODO:
Implement the close functionality (make sure to ask about saving!)
Add undo and redo functionality
"""

import json

from PyQt5 import QtCore, QtGui, QtWidgets



class KeyPressedTree(QtWidgets.QTreeWidget):
    keyPressed = QtCore.pyqtSignal(int)

    def keyPressEvent(self, event):
        super(KeyPressedTree, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())


class Course(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, data = ["New Course","",""], *__args):
        super().__init__(parent, data)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.setFont(0, font)
        self.setFont(2, font)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)


class AssignmentType(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, data = ["New Assignment Type","",""], *__args):
        super().__init__(parent, data)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.setFont(0, font)
        self.setTextAlignment(1, QtCore.Qt.AlignCenter)
        self.setTextAlignment(2, QtCore.Qt.AlignCenter)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)


class Assignment(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, data = ["New Assignment","",""], *__args):
        super().__init__(parent, data)
        self.setTextAlignment(2, QtCore.Qt.AlignCenter)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)


class FloatDelegate(QtWidgets.QItemDelegate):
    def __init__(self, decimals, parent=None):
        QtWidgets.QItemDelegate.__init__(self, parent=parent)
        self.nDecimals = decimals

    def paint(self, painter, option, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        try:
            number = float(value)
            painter.drawText(option.rect, QtCore.Qt.AlignCenter, "{:.{}f}".format(number, self.nDecimals))

        except :
            QtWidgets.QItemDelegate.paint(self, painter, option, index)

# class WeightDelegate(QtWidgets.QItemDelegate):
#     def __init__(self, decimals, parent=None):
#         QtWidgets.QItemDelegate.__init__(self, parent=parent)
#
#     def paint(self, painter, option, index):
#         value = index.model().data(index, QtCore.Qt.EditRole)
#         try:
#             if "/" in value:
#                 i = value.find("/")
#                 x = float(value[:i]) / float(value[i + 1:])
#                 if x > 1:
#                     raise Exception
#
#             else:
#                 value = float(value)
#                 if value > 1:
#                     value /= 100
#                     if value > 1:
#                         raise Exception
#         except:
#             value = ""
#
#         finally:
#             painter.drawText(option.rect, QtCore.Qt.AlignCenter, value)




class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self):
        self.setObjectName("Grade Manager")
        self.resize(912, 647)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidget = KeyPressedTree(self.centralwidget)
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
        self.treeWidget.setItemDelegateForColumn(2,FloatDelegate(4))
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.openMenu)

        self.actionSave.triggered.connect(self.saveJSON)
        self.actionOpen.triggered.connect(self.readJSON)
        self.actionSave_as.triggered.connect(self.saveAsJSON)
        self.actionNew.triggered.connect(self.clearPage)
        self.actionClose.triggered.connect(self.close)

        self.treeWidget.itemChanged.connect(self.itemClicked)
        self.treeWidget.keyPressed.connect(self.keyPressed)

        self.filename = None



    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Grade Manager", "Grade Manager"))
        self.treeWidget.headerItem().setText(0, _translate("Grade Manager", "Course"))
        self.treeWidget.headerItem().setText(1, _translate("Grade Manager", "Weight"))
        self.treeWidget.headerItem().setText(2, _translate("Grade Manager", "Grade"))
        self.menuFile.setTitle(_translate("Grade Manager", "Fi&le"))
        self.actionOpen.setText(_translate("Grade Manager", "&Open"))
        self.actionOpen.setShortcut(_translate("Grade Manager", "Ctrl+O"))
        self.actionClose.setText(_translate("Grade Manager", "&Close"))
        self.actionNew.setText(_translate("Grade Manager", "&New"))
        self.actionSave.setText(_translate("Grade Manager", "&Save"))
        self.actionSave.setShortcut(_translate("Grade Manager", "Ctrl+S"))
        self.actionSave_as.setText(_translate("Grade Manager", "Sa&ve as..."))
        self.actionSave_as.setShortcut(_translate("Grade Manager", "Ctrl+Shift+S"))


    def clearPage(self):
        answer = QtWidgets.QMessageBox.question(self, "Close Confirmation",
                                                "Would you like to save before exitting?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)

        if answer == QtWidgets.QMessageBox.Cancel:
            return
        elif answer == QtWidgets.QMessageBox.Yes:
            self.saveJSON()
        self.treeWidget.clear()
        self.courses = []
        self.filename = None

    def addCourse(self):
        course = Course(self.treeWidget)
        course.setExpanded(True)
        self.courses.append(course)
    def addType(self,course):
        t = AssignmentType(course)
        t.setExpanded(True)
        course.addChild(t)

    def addAssignment(self,assignment_type):
        ass = Assignment(assignment_type)
        assignment_type.addChild(ass)

    def removeItem(self,item,level):
        root = self.treeWidget.invisibleRootItem()
        parent = item.parent()
        (parent or root).removeChild(item)

        if level == 2:  # if just the assignment was removed
            self.updateTypeGrade(parent)
        elif level == 1:  # if the assignment type was just removed
            self.updateCourseGrade(parent)

    def openMenu(self, position):
        menu = QtWidgets.QMenu(self)
        indices = self.treeWidget.selectedItems()

        level = 0
        if not indices:
            menu.addAction(self.tr("Add New Course"))

        else:
            i = indices[0]
            while i.parent():
                i = i.parent()
                level += 1
            choices = (("Add New Course","Add New Assignment Type","Remove Selected Course"),
                       ("Add New Assignment","Remove Selected Assignment Type"),("Remove Assignment",))


            [menu.addAction(self.tr(act)) for act in choices[level]]

        action = menu.exec_(self.treeWidget.viewport().mapToGlobal(position))
        if action:
            action = action.text()
            if action == "Add New Course":
                self.addCourse()
            elif action == "Add New Assignment Type":
                self.addType(indices[0])
            elif action == "Add New Assignment":
                self.addAssignment(indices[0])
            else:
                self.removeItem(indices[0],level)



    def saveJSON(self):
        self.filename = self.save(self.filename)

    def saveAsJSON(self):
        self.save()

    def transformInput(self,data:str):
        if "/" in data:
            i = data.find("/")
            return float(data[:i])/float(data[i+1:])
        return float(data)

    def updateTypeGrade(self,ass_type):
        type_grade = 0.0
        num_assignments = ass_type.childCount()
        for i in range(num_assignments):
            grade = ass_type.child(i).text(2)
            if not grade:  # if the column is empty
                num_assignments -= 1
                continue
            type_grade += self.transformInput(grade)
        type_grade = f"{type_grade / num_assignments}" if num_assignments > 0 else ""
        ass_type.setText(2, type_grade)

    def updateCourseGrade(self,course):
        total_weight = 0.0
        earned_weight = 0.0
        for i in range(course.childCount()):
            t = course.child(i)
            weight = t.text(1)
            grade = t.text(2)
            if not weight or not grade:  # if no weight is entered
                continue
            total_weight += self.transformInput(weight)
            earned_weight += self.transformInput(weight) * self.transformInput(grade)
        course_grade = str(earned_weight / total_weight) if total_weight > 0 else ""
        course.setText(2, course_grade)

    def itemClicked(self, item, col):
        """
        Handles input validation and grade calculation.
        :param item:
        :param col:
        :return:
        """

        if isinstance(item, Course) or col == 0:
            return
        elif isinstance(item, Assignment):
            item = item.parent() # changes assignment to the assignment type
            self.updateTypeGrade(item)
        # from this point, the item must be an assignment type.
        self.updateCourseGrade(item.parent())

    def keyPressed(self,key):
        indices = self.treeWidget.selectedItems()

        level = 0
        if not indices: # if no tree item is selected
            if key == QtCore.Qt.Key_Insert:
                self.addCourse()
        else:
            i = indices[0]
            while i.parent():
                i = i.parent()
                level += 1
            i = indices[0]
            if key == QtCore.Qt.Key_Delete:
                self.removeItem(i, level)

            else:
                if level == 0:
                    if key == QtCore.Qt.Key_Insert:
                        self.addType(i)
                elif level == 1:
                    if key == QtCore.Qt.Key_Insert:
                        self.addAssignment(i)
                elif level == 2:
                    pass

    def save(self,filename=None):
        if not filename:  # if a file hasn't been opened yet (save as or new file)
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                                     "Gradebook Files (*.grdb)")
        if filename:
            data = {"Course": []}
            for course in self.courses:
                c_data = {"Name": course.text(0), "Weight": course.text(1), "Grade": course.text(2), "Expanded": course.isExpanded(), "Types": []}
                for i in range(course.childCount()):
                    t = course.child(i)
                    t_data = {"Name": t.text(0), "Weight": t.text(1), "Grade": t.text(2), "Expanded": t.isExpanded(),"Assignments": []}
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
                    course.setExpanded(course_dict["Expanded"])
                    for type_dict in course_dict["Types"]:
                        t = AssignmentType(course,[type_dict["Name"],type_dict["Weight"],type_dict["Grade"]])
                        t.setExpanded(type_dict["Expanded"])
                        for assignment in type_dict["Assignments"]:
                            t.addChild(Assignment(t,[assignment["Name"],assignment["Weight"],assignment["Grade"]]))
                        course.addChild(t)
                    self.courses.append(course)


    def closeEvent(self, event):
        event.ignore()
        answer = QtWidgets.QMessageBox.question(self,"Close Confirmation",
                                                "Would you like to save before exitting?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)

        if answer == QtWidgets.QMessageBox.Cancel:
            return
        elif answer == QtWidgets.QMessageBox.Yes:
            self.saveJSON()

        event.accept()






if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.setupUi()
    ui.show()
    sys.exit(app.exec_())




