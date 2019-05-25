#!/usr/bin/python3
import os
import json
import PyQt5  # allows for the creation of a windows executable
from PyQt5 import QtCore, QtGui, QtWidgets
import qdarkstyle
from QTDark import sheet as darksheet2

"""
# TODO:
0) Add images to readme
1) move code into separate files.  For example, the completed fonts can be
loaded in from a python file similar to QTDark
3) Create a better solution for switching between themes.
4) implement the other method of recording grades (point system rather than weights)
5) In general, try to clean up and comment the code.
6) Once all of the above have been implemented, release the next version and create
the next windows executable.

This should all be finished before the start of next semester (seems very reasonable)
The final boss will be implementing undo/redo functionality.  If this can be achieved,
then the project is pretty much done.
"""


courseFont = QtGui.QFont()
courseFont.setBold(True)
courseFont.setWeight(100)
courseFont.setPointSize(18)

typeFont = QtGui.QFont()
typeFont.setUnderline(True)
typeFont.setPointSize(16)
typeFont.setWeight(50)

assFont = QtGui.QFont()
assFont.setItalic(True)
assFont.setPointSize(14)
assFont.setWeight(50)

extraCreditFont = QtGui.QFont()
extraCreditFont.setItalic(True)
extraCreditFont.setUnderline(True)
extraCreditFont.setPointSize(14)
extraCreditFont.setWeight(75)

not_in_calc_font = QtGui.QFont()
not_in_calc_font.setItalic(True)
not_in_calc_font.setPointSize(14)
not_in_calc_font.setWeight(50)
not_in_calc_font.setStrikeOut(True)


class KeyPressedTree(QtWidgets.QTreeWidget):
    keyPressed = QtCore.pyqtSignal(int)
    order_swapped = False
    current_course = -1

    def keyPressEvent(self, event):
        super(KeyPressedTree, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def dropEvent(self, QDropEvent):
        # helpful link https://www.walletfox.com/course/qtreorderabletree.php

        # index at which the dragged item is being dropped
        droppedIndex = self.indexAt(QDropEvent.pos())

        if not droppedIndex.isValid():
            return

        draggedItem = self.currentItem()  # item being moved
        if draggedItem:
            draggedParent = draggedItem.parent()  # parent of the item being moved
            if draggedParent:  # if it has a parent (the item isn't a course)
                # if the parents are different (ex: moving an assignment from one type to another type)
                if self.itemFromIndex(droppedIndex.parent()) != draggedParent:
                    return
            else:  # if i'm trying to move a course
                draggedParent = self.invisibleRootItem()
            draggedParent.removeChild(draggedItem)  # delete the dragged item
            draggedParent.insertChild(droppedIndex.row(), draggedItem)  # reinsert the dragged item
            self.order_swapped = True

    # next two methods let me iterate through the courses in the tree
    def __iter__(self):
        self.current_course = -1
        return self

    def __next__(self):
        self.current_course += 1
        if self.current_course >= self.topLevelItemCount():
            raise StopIteration
        else:
            return self.topLevelItem(self.current_course)

    def has_been_swapped(self):
        return self.order_swapped

    def set_swap_status(self, swap_status):
        self.order_swapped = swap_status


class Course(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, data=["New Course", "", ""], *__args):
        super().__init__(parent, data)
        self.setFont(0, courseFont)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled)


class AssignmentType(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, data=["New Assignment Type", "", ""], *__args):
        super().__init__(parent, data)
        self.setFont(0, typeFont)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled)

        self.extraCredit = False

    def set_extra_credit(self, is_extra):
        self.extraCredit = is_extra

    def is_extra_credit(self):
        return self.extraCredit


class ExtraCredit(AssignmentType):
    def __init__(self, parent, data=["Extra Credit", "", ""], *__args):
        super().__init__(parent, data)
        self.setFont(0, typeFont)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDropEnabled)


class Assignment(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, data=["New Assignment", "", ""], *__args):
        super().__init__(parent, data)
        self.setFont(0, assFont)
        self.extraCredit = False
        self.in_calculation = True
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)

    def setExtraCredit(self, is_extra):
        self.extraCredit = is_extra

    def set_in_calculation(self, in_calculation):
        self.in_calculation = in_calculation

    def is_extra_credit(self):
        return self.extraCredit

    def is_in_calculation(self):
        return self.in_calculation


class ValidWeightGradeInput(QtWidgets.QItemDelegate):
    def createEditor(self, parent, option, index):
        line = QtWidgets.QLineEdit(parent)
        reg_ex = QtCore.QRegExp(r"|0?\.\d+|\d*\.?\d+/\d*\.?\d+")
        input_validator = QtGui.QRegExpValidator(reg_ex, line)
        line.setValidator(input_validator)
        return line


class FloatDelegate(QtWidgets.QItemDelegate):
    def __init__(self, decimals, parent: KeyPressedTree):
        self.treeWidget = parent
        super(FloatDelegate, self).__init__(parent=parent)
        self.nDecimals = decimals

    def createEditor(self, parent, option, index):
        # if any of the below conditions are met, then the cell is editable.
        # basically, if the first index is zero, then it's editable
        # if the weight column for the assignment type item is selected, then it's editable
        # if the grade column for the assignment item is selected, it's editable
        # in all other cases, it's not editable.
        if index.column() == 0:
            return QtWidgets.QItemDelegate.createEditor(self, parent, option, index)
        elif (
                index.column() == 1 and isinstance(self.treeWidget.itemFromIndex(index), AssignmentType)) or (
                index.column() == 2 and isinstance(self.treeWidget.itemFromIndex(index), Assignment)):

            return ValidWeightGradeInput.createEditor(self, parent, option, index)

        else:
            return None

    def paint(self, painter, option, index):
        item = self.treeWidget.itemFromIndex(index)
        if index.column() != 0:
            font = courseFont
            color = QtCore.Qt.darkBlue
            if isinstance(item, AssignmentType):
                color = QtCore.Qt.darkGreen
                font = typeFont
            elif isinstance(item, Assignment):
                color = QtCore.Qt.blue
                font = assFont
            cg = QtGui.QPalette.Normal if option.state & QtWidgets.QStyle.State_Enabled else QtGui.QPalette.Disabled
            option.palette.setColor(cg, QtGui.QPalette.Text, color)
            option.font = font
            option.displayAlignment = QtCore.Qt.AlignCenter

        super(FloatDelegate, self).paint(painter, option, index)

    def drawDisplay(self, painter, option, rect, text):
        if "/" not in text:
            try:
                text = "{:.{}f}".format(float(text) * 100, self.nDecimals)
            except ValueError:
                pass
        super(FloatDelegate, self).drawDisplay(painter, option, rect, text)


class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, app):
        self.app = app

        # initializing cached settings
        self.settings = QtCore.QSettings("JSR", "Grade Manager")
        self.theme_num = int(self.settings.value("theme_num", -1)) % 3
        self.changeTheme()
        self.filename = self.settings.value("filename", None)

        self.setWindowTitle("Grade Manager")
        self.resize(620, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.treeWidget = KeyPressedTree(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setMinimumSize(QtCore.QSize(620, 600))

# Enable drag and drop within the tree widget
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.treeWidget.setDragEnabled(True)
        self.treeWidget.setAcceptDrops(True)
        self.treeWidget.setDropIndicatorShown(True)
        self.treeWidget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(100)
        self.treeWidget.setFont(font)

        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
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
        self.actionClose.setShortcut("Ctrl+D")
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
        if os.path.isfile(self.filename):
            self.openFile(self.filename)

    def clearPage(self):
        if self.change_made or self.treeWidget.has_been_swapped():
            answer = QtWidgets.QMessageBox.question(self, "Close Confirmation",
                                                    "Would you like to save before exiting?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)

            if answer == QtWidgets.QMessageBox.Cancel:
                return
            elif answer == QtWidgets.QMessageBox.Yes:
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
            ass_type_choices = ("Add New Assignment", "Remove Selected Assignment Type")
            assignment_choices = ("Remove Assignment", "Set As Not Extra Credit" if level == 2 and indices[0].is_extra_credit(
            ) else "Set As Extra Credit", "Remove from grade calculation" if level == 2 and indices[0].is_in_calculation() else "Include in grade calculation")
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
                indices[0].setFont(0, extraCreditFont if indices[0].is_extra_credit() else assFont)
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
                if not grade or not ass_type.child(i).is_in_calculation():  # if the column is empty
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
        type_grade = f"{type_grade / num_assignments}" if num_assignments > 0 else ""
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
                earned_weight += self.transformInput(weight) * self.transformInput(grade)
            else:
                if grade:
                    extra_credit += self.transformInput(grade)
        course_grade = str(earned_weight / total_weight + extra_credit) if total_weight > 0 else ""
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
                if (index.column() == 1 and isinstance(self.treeWidget.itemFromIndex(index), AssignmentType)) or (
                        index.column() == 2 and isinstance(self.treeWidget.itemFromIndex(index), Assignment)):
                    i.setText(self.treeWidget.selectedIndexes()[0].column(), "")
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
        if not filename:  # if a file hasn't been opened yet (save as or new file)
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "./",
                                                                "Gradebook Files (*.grdb)")
        if filename:
            data = {"Course": []}
            for course in self.treeWidget:
                c_data = {"Name": course.text(0), "Weight": course.text(1), "Grade": course.text(2),
                          "Expanded": course.isExpanded(), "Types": []}
                for i in range(course.childCount()):
                    t = course.child(i)
                    t_data = {"Name": t.text(0), "Weight": t.text(1), "Grade": t.text(2), "Expanded": t.isExpanded(),
                              "Assignments": [], "Extra Credit": isinstance(t, ExtraCredit)}
                    for j in range(t.childCount()):
                        ass = t.child(j)
                        t_data["Assignments"].append({"Name": ass.text(0), "Weight": ass.text(1), "Grade": ass.text(2),
                                                      "Extra Credit": ass.is_extra_credit(), "Included in Grade": ass.is_in_calculation()})
                    c_data["Types"].append(t_data)
                data["Course"].append(c_data)

            with open(filename.replace(".grdb", "") + ".grdb", "w+") as f:
                json.dump(data, f)
            self.change_made = False
            self.treeWidget.set_swap_status(False)
        return filename

    def readJSON(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", "",
                                                            "Gradebook Files (*.grdb)")
        if filename:
            self.openFile(filename)

    def openFile(self, filename):
        with open(filename) as json_file:
            self.clearPage()
            self.filename = filename
            data = json.load(json_file)

            for course_dict in data["Course"]:
                course = Course(self.treeWidget, [
                                course_dict["Name"], course_dict["Weight"], course_dict["Grade"]])
                course.setExpanded(course_dict["Expanded"])
                for type_dict in course_dict["Types"]:
                    c = ExtraCredit if type_dict["Extra Credit"] else AssignmentType
                    t = c(course, [type_dict["Name"], type_dict["Weight"], type_dict["Grade"]])
                    t.setExpanded(type_dict["Expanded"])
                    for assignment in type_dict["Assignments"]:
                        ass = Assignment(
                            t, [assignment["Name"], assignment["Weight"], assignment["Grade"]])
                        if assignment["Extra Credit"]:
                            ass.setExtraCredit(True)
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
            answer = QtWidgets.QMessageBox.question(self, "Close Confirmation",
                                                    "Would you like to save before exiting?",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)

            if answer == QtWidgets.QMessageBox.Cancel:
                return
            elif answer == QtWidgets.QMessageBox.Yes:
                self.saveJSON()

            event.accept()
        self.settings.setValue("theme_num", self.theme_num - 1)
        self.settings.setValue("filename", self.filename if self.filename else "")

    def changeTheme(self):
        if self.theme_num == 0:
            # switch to dark theme 1
            self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        elif self.theme_num == 1:
            # switch to dark theme 2
            self.app.setStyleSheet(darksheet2)
        else:
            # switch to light theme
            self.app.setStyleSheet("")

        self.theme_num = (self.theme_num + 1) % 3


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # set default style here?
    ui = Ui_MainWindow()
    ui.setupUi(app)
    ui.show()
    sys.exit(app.exec_())
