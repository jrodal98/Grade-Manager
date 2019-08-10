"""
Author: Jacob Rodal
Email: jr6ff@virginia.edu
Code repository: https://github.com/jrodal98/Grade_Manager
"""

import os
import json

from PyQt5 import QtCore, QtGui, QtWidgets
from fonts import assFont, extraCreditFont, not_in_calc_font
from widgets import Course, AssignmentType, Assignment, ExtraCredit, \
    KeyPressedTree
from themes import qdarkstyle, QTDark
from input_verifiers import FloatDelegate


class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, app):
        self.app = app
        self.centralwidget = QtWidgets.QWidget(self)
        self.treeWidget = KeyPressedTree(self.centralwidget)
        # initializing cached settings
        self.settings = QtCore.QSettings("JSR", "Grade Manager")
        self.theme_num = int(self.settings.value("theme_num", -1)) % 3
        self.changeTheme()
        self.filename = self.settings.value("filename", None)

        self.setWindowTitle("Grade Manager")
        self.resize(620, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(
            self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setMinimumSize(QtCore.QSize(620, 600))

# Enable drag and drop within the tree widget
        self.treeWidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.treeWidget.setDragEnabled(True)
        self.treeWidget.setAcceptDrops(True)
        self.treeWidget.setDropIndicatorShown(True)
        self.treeWidget.setDragDropMode(
            QtWidgets.QAbstractItemView.InternalMove)

        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(100)
        self.treeWidget.setFont(font)

        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectItems)
        self.treeWidget.setAnimated(True)
        self.treeWidget.setWordWrap(True)

        self.treeWidget.headerItem().setText(0, "Course")
        self.treeWidget.headerItem().setText(1, "Weight")
        self.treeWidget.headerItem().setText(2, "Grade")
        self.treeWidget.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.treeWidget.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        self.treeWidget.headerItem().setTextAlignment(2, QtCore.Qt.AlignCenter)

        self.treeWidget.setColumnWidth(0, 370)
        self.treeWidget.setColumnWidth(1, 130)
        self.treeWidget.setColumnWidth(2, 100)
        # self.treeWidget.header().setDefaultSectionSize(275)
        # self.treeWidget.header().setMinimumSectionSize(50)
        self.treeWidget.header().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.treeWidget)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 912, 35))

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setTitle("Fi&le")
        self.themeFile = QtWidgets.QMenu(self.menubar)
        self.themeFile.setTitle("Style")

        self.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction(self, text="&Open")
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionClose = QtWidgets.QAction(self, text="&Close")
        self.actionClose.setShortcut("Ctrl+W")
        self.actionNew = QtWidgets.QAction(self, text="&New")
        self.actionSave = QtWidgets.QAction(self, text="&Save")
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave_as = QtWidgets.QAction(self, text="Sa&ve as...")
        self.actionSave_as.setShortcut("Ctrl+Shift+S")

        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menubar.addAction(self.menuFile.menuAction())

        self.changeStyle = QtWidgets.QAction(self, text="&Change Style")
        self.themeFile.addAction(self.changeStyle)
        self.menubar.addAction(self.themeFile.menuAction())

        self.treeWidget.setItemDelegate(FloatDelegate(2, self.treeWidget))

        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.treeWidget.customContextMenuRequested.connect(self.openMenu)

        self.actionSave.triggered.connect(self.saveJSON)
        self.actionOpen.triggered.connect(self.readJSON)
        self.actionSave_as.triggered.connect(self.saveAsJSON)
        self.actionNew.triggered.connect(self.clearPage)
        self.actionClose.triggered.connect(self.close)
        self.changeStyle.triggered.connect(self.changeTheme)

        self.treeWidget.itemChanged.connect(self.itemClicked)
        self.treeWidget.keyPressed.connect(self.keyPressed)

        self.change_made = False

        # if a file has been cached and it still exists:
        if self.filename and os.path.isfile(self.filename):
            self.openFile(self.filename)

    def clearPage(self):
        if self.change_made or self.treeWidget.has_been_swapped():
            ans = QtWidgets.QMessageBox \
                .question(self, "Close Confirmation",
                          "Would you like to save before exiting?",
                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
                          | QtWidgets.QMessageBox.Cancel)

            if ans == QtWidgets.QMessageBox.Cancel:
                return
            elif ans == QtWidgets.QMessageBox.Yes:
                self.saveJSON()
        self.treeWidget.clear()
        self.treeWidget.set_swap_status(False)
        self.filename = None
        self.change_made = False

    def addCourse(self):
        course = Course(self.treeWidget)
        course.setExpanded(True)
        self.change_made = True

    def addType(self, course):
        t = AssignmentType(course)
        t.setExpanded(True)
        course.addChild(t)
        self.change_made = True

    def addExtraCredit(self, course):
        extra = ExtraCredit(course)
        extra.setExpanded(True)
        course.addChild(extra)
        self.change_made = True

    def addAssignment(self, assignment_type):
        ass = Assignment(assignment_type)
        assignment_type.addChild(ass)
        self.change_made = True

    def removeItem(self, item, level):
        root = self.treeWidget.invisibleRootItem()
        parent = item.parent()
        (parent or root).removeChild(item)

        if level == 2:  # if just the assignment was removed
            self.updateTypeGrade(parent)
        elif level == 1:  # if the assignment type was just removed
            self.updateCourseGrade(parent)
        self.change_made = True

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

            course_choices = ("Add New Course", "Add New Assignment Type",
                              "Add Extra Credit", "Remove Selected Course")
            ass_type_choices = ("Add New Assignment",
                                "Remove Selected Assignment Type")
            assignment_choices = ("Remove Assignment",
                                  "Set As Not Extra Credit" if level == 2 and
                                  indices[0].is_extra_credit(
                                  ) else "Set As Extra Credit",
                                  "Remove from grade calculation" if level == 2
                                  and indices[0].is_in_calculation()
                                  else "Include in grade calculation")
            choices = (course_choices, ass_type_choices, assignment_choices)

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
            elif action == "Set As Extra Credit":
                indices[0].set_extra_credit(True)
                self.updateTypeGrade(indices[0].parent())
                indices[0].setFont(0, extraCreditFont)
                self.change_made = True
            elif action == "Set As Not Extra Credit":
                indices[0].set_extra_credit(False)
                self.updateTypeGrade(indices[0].parent())
                indices[0].setFont(0, assFont)
                self.change_made = True
            elif action == "Remove from grade calculation":
                indices[0].set_in_calculation(False)
                self.updateTypeGrade(indices[0].parent())
                indices[0].setFont(0, not_in_calc_font)
                self.change_made = True
            elif action == "Include in grade calculation":
                indices[0].set_in_calculation(True)
                self.updateTypeGrade(indices[0].parent())
                indices[0].setFont(
                    0, extraCreditFont if indices[0].is_extra_credit()
                    else assFont)
                self.change_made = True
            elif action == "Add Extra Credit":
                self.addExtraCredit(indices[0])
            else:
                self.removeItem(indices[0], level)

    def saveJSON(self):
        self.filename = self.save(self.filename)

    def saveAsJSON(self):
        self.save()

    def transformInput(self, data: str):
        if "/" in data:
            i = data.find("/")
            return float(data[:i]) / float(data[i + 1:])
        return float(data)

    def updateTypeGrade(self, ass_type):
        type_grade = 0.0
        num_assignments = ass_type.childCount()
        if not isinstance(ass_type, ExtraCredit):
            for i in range(num_assignments):
                grade = ass_type.child(i).text(2)
                # if the column is empty
                if not grade or not ass_type.child(i).is_in_calculation():
                    num_assignments -= 1
                    continue
                if ass_type.child(i).is_extra_credit():
                    num_assignments -= 1
                type_grade += self.transformInput(grade)
        else:
            for i in range(num_assignments):
                grade = ass_type.child(i).text(2)
                if grade:  # if the column is empty
                    type_grade += self.transformInput(grade)
            num_assignments = 1
        type_grade = f"{type_grade / num_assignments}" if num_assignments > 0 \
            else ""
        ass_type.setText(2, type_grade)

    def updateCourseGrade(self, course):
        total_weight = 0.0
        earned_weight = 0.0
        extra_credit = 0.0
        for i in range(course.childCount()):
            t = course.child(i)
            weight = t.text(1)
            grade = t.text(2)
            if not isinstance(t, ExtraCredit):
                if not weight or not grade:  # if no weight is entered
                    continue
                total_weight += self.transformInput(weight)
                earned_weight += self.transformInput(
                    weight) * self.transformInput(grade)
            else:
                if grade:
                    extra_credit += self.transformInput(grade)
        course_grade = str(earned_weight / total_weight +
                           extra_credit) if total_weight > 0 else ""
        course.setText(2, course_grade)

    def itemClicked(self, item, col):
        self.change_made = True
        if isinstance(item, Course) or col == 0:
            return
        elif isinstance(item, Assignment):
            item = item.parent()  # changes assignment to the assignment type
            self.updateTypeGrade(item)
        # from this point, the item must be an assignment type.
        self.updateCourseGrade(item.parent())

    def keyPressed(self, key):
        items = self.treeWidget.selectedItems()

        level = 0
        if not items:  # if no tree item is selected
            if key == QtCore.Qt.Key_Insert:
                self.addCourse()
        else:
            i = items[0]
            while i.parent():
                i = i.parent()
                level += 1
            i = items[0]
            if key == QtCore.Qt.Key_Delete:
                index = self.treeWidget.selectedIndexes()[0]
                if (index.column() == 1 and isinstance(
                    self.treeWidget.itemFromIndex(index), AssignmentType)) or (
                        index.column() == 2 and isinstance(
                            self.treeWidget.itemFromIndex(index), Assignment)):
                    i.setText(self.treeWidget.selectedIndexes()
                              [0].column(), "")
                elif index.column() == 0:
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

    def save(self, filename=None):
        # if a file hasn't been opened yet (save as or new file)
        if not filename:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                "Save File",
                                                                "./",
                                                                "Gradebook \
                                                                    Files \
                                                                    (*.grdb)")
        if filename:
            data = {"Course": []}
            for course in self.treeWidget:
                c_data = {"Name": course.text(0), "Weight": course.text(1),
                          "Grade": course.text(2),
                          "Expanded": course.isExpanded(), "Types": []}
                for i in range(course.childCount()):
                    t = course.child(i)
                    t_data = {"Name": t.text(0), "Weight": t.text(1),
                              "Grade": t.text(2), "Expanded": t.isExpanded(),
                              "Assignments": [],
                              "Extra Credit": isinstance(t, ExtraCredit)}
                    for j in range(t.childCount()):
                        ass = t.child(j)
                        t_data["Assignments"].append({"Name": ass.text(0),
                                                      "Weight": ass.text(1),
                                                      "Grade": ass.text(2),
                                                      "Extra Credit":
                                                      ass.is_extra_credit(),
                                                      "Included in Grade":
                                                      ass.is_in_calculation()})
                    c_data["Types"].append(t_data)
                data["Course"].append(c_data)

            with open(filename.replace(".grdb", "") + ".grdb", "w+") as f:
                json.dump(data, f)
            self.change_made = False
            self.treeWidget.set_swap_status(False)
        return filename

    def readJSON(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                            "Select File", "",
                                                            "Gradebook Files \
                                                                 (*.grdb)")
        if filename:
            self.openFile(filename)

    def openFile(self, filename):
        with open(filename) as json_file:
            self.clearPage()
            self.filename = filename
            data = json.load(json_file)

            for course_dict in data["Course"]:
                course = Course(self.treeWidget, [
                                course_dict["Name"], course_dict["Weight"],
                                course_dict["Grade"]])
                course.setExpanded(course_dict["Expanded"])
                for type_dict in course_dict["Types"]:
                    c = ExtraCredit if type_dict["Extra Credit"] else \
                        AssignmentType
                    t = c(course, [type_dict["Name"],
                                   type_dict["Weight"], type_dict["Grade"]])
                    t.setExpanded(type_dict["Expanded"])
                    for assignment in type_dict["Assignments"]:
                        ass = Assignment(
                            t, [assignment["Name"], assignment["Weight"],
                                assignment["Grade"]])
                        if assignment["Extra Credit"]:
                            ass.set_extra_credit(True)
                            ass.setFont(0, extraCreditFont)
                        if not assignment["Included in Grade"]:
                            ass.set_in_calculation(False)
                            ass.setFont(0, not_in_calc_font)
                        t.addChild(ass)
                    course.addChild(t)
        self.change_made = False
        self.treeWidget.set_swap_status(False)

    def closeEvent(self, event):
        if self.change_made or self.treeWidget.has_been_swapped():
            event.ignore()
            ans = QtWidgets.QMessageBox.question(self,
                                                 "Close Confirmation",
                                                 "Would you like to save \
                                                         before exiting?",
                                                 QtWidgets.QMessageBox.Yes |
                                                 QtWidgets.QMessageBox.No |
                                                 QtWidgets.QMessageBox.Cancel)

            if ans == QtWidgets.QMessageBox.Cancel:
                return
            elif ans == QtWidgets.QMessageBox.Yes:
                self.saveJSON()

            event.accept()
        self.settings.setValue("theme_num", self.theme_num - 1)
        self.settings.setValue(
            "filename", self.filename if self.filename else "")

    def changeTheme(self):
        if self.theme_num == 0:
            # switch to dark theme 1
            self.app.setStyleSheet(qdarkstyle)
        elif self.theme_num == 1:
            # switch to dark theme 2
            self.app.setStyleSheet(QTDark)
        else:
            # switch to light theme
            self.app.setStyleSheet("")

        self.theme_num = (self.theme_num + 1) % 3
        self.treeWidget.set_theme_num(self.theme_num)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.setupUi(app)
    ui.show()
    sys.exit(app.exec_())
