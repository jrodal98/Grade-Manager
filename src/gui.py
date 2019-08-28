"""
Author: Jacob Rodal
Email: jr6ff@virginia.edu
Code repository: https://github.com/jrodal98/Grade_Manager
"""

import os
import json
import re

from PyQt5 import QtCore, QtWidgets
from fonts import assFont, extraCreditFont, not_in_calc_font
from widgets import Course, AssignmentType, Assignment, ExtraCredit, \
    GradebookTree
from themes import qdarkstyle, QTDark
from input_verifiers import FloatDelegate


class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, app):
        self.app = app
        self.centralwidget = QtWidgets.QWidget(self)
        self.treeWidget = GradebookTree(self.centralwidget)
        # initializing cached settings
        self.settings = QtCore.QSettings("JSR", "Grade Manager")
        self.theme_num = int(self.settings.value("theme_num", -1)) % 3
        self.changeTheme()
        self.filename = self.settings.value("filename", None)

        self.setWindowTitle("Grade Manager")
        self.resize(int(self.settings.value("window_width", 620)),
                    int(self.settings.value("window_height", 600)))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(
            self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setMinimumSize(QtCore.QSize(620, 600))

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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = self.size().width()
        self.treeWidget.setColumnWidth(0, 370/630 * width)
        self.treeWidget.setColumnWidth(1, 130/630 * width)
        self.treeWidget.setColumnWidth(2, 100/630 * width)

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

    def addAssignment(self, assignment_type, text="New Assignment"):
        ass = Assignment(assignment_type, data=[text, "", ""])
        assignment_type.addChild(ass)
        self.change_made = True

    def removeItem(self, item, level):
        root = self.treeWidget.invisibleRootItem()
        parent = item.parent()
        (parent or root).removeChild(item)

        # if the assignment was removed
        # or if the assignment type was removed
        if level == 1 or level == 2:  # if just the assignment was removed
            parent.updateGrade()
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
                indices[0].parent().updateGrade()
                indices[0].setFont(0, extraCreditFont)
                self.change_made = True
            elif action == "Set As Not Extra Credit":
                indices[0].set_extra_credit(False)
                indices[0].parent().updateGrade()
                indices[0].setFont(0, assFont)
                self.change_made = True
            elif action == "Remove from grade calculation":
                indices[0].set_in_calculation(False)
                indices[0].parent().updateGrade()
                indices[0].setFont(0, not_in_calc_font)
                self.change_made = True
            elif action == "Include in grade calculation":
                indices[0].set_in_calculation(True)
                indices[0].parent().updateGrade()
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

    def itemClicked(self, item, col):
        self.change_made = True
        if isinstance(item, Course):
            return
        elif isinstance(item, Assignment) and col == 0:
            # determine if the bash `mkdir example{0..10}` syntax is used.
            # if so, make multiple assignments following such syntax.
            m = re.search(r"(.+){(\d+)\.\.(\d+)}", item.text(0))
            if m:
                text = m.group(1)
                item.setText(0, text + m.group(2))
                for i in range(int(m.group(2))+1, int(m.group(3)) + 1):
                    self.addAssignment(item.parent(), f"{text}{i}")
            return
        elif isinstance(item, Assignment):
            item = item.parent()  # changes assignment to the assignment type
            item.updateGrade()
        # from this point, the item must be an assignment type.
        item.parent().updateGrade()

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
        self.settings.setValue("window_width", self.size().width())
        self.settings.setValue("window_height", self.size().height())

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
