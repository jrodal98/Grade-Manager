"""
Author: Jacob Rodal
Email: jr6ff@virginia.edu
Code repository: https://github.com/jrodal98/Grade_Manager
"""

from PyQt5 import QtWidgets, QtCore
from fonts import courseFont, assFont, extraCreditFont, typeFont, treeFont


class GradebookTree(QtWidgets.QTreeWidget):
    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self, central_widget):
        super().__init__(central_widget)
        self.order_swapped = False
        self.current_course = -1
        self.theme_num = 0
        self.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(
            QtWidgets.QAbstractItemView.InternalMove)
        self.setFont(treeFont)

        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectItems)
        self.setAnimated(True)
        self.setWordWrap(True)

        self.headerItem().setText(0, "Course")
        self.headerItem().setText(1, "Weight")
        self.headerItem().setText(2, "Grade")
        self.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        self.headerItem().setTextAlignment(2, QtCore.Qt.AlignCenter)

        self.header().setStretchLastSection(True)

    def keyPressEvent(self, event):
        super(GradebookTree, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def dropEvent(self, QDropEvent):
        # helpful link https://www.walletfox.com/course/qtreorderabletree.php

        # index at which the dragged item is being dropped
        droppedIndex = self.indexAt(QDropEvent.pos())

        if not droppedIndex.isValid():
            return

        draggedItem = self.currentItem()  # item being moved
        if draggedItem:
            draggedParent = draggedItem.parent()  # parent of the moved item
            if draggedParent:  # if it has a parent (the item isn't a course)
                # if the parents are different
                # (ex: moving an assignment from one type to another type)
                if self.itemFromIndex(droppedIndex.parent()) != draggedParent:
                    return
            else:  # if i'm trying to move a course
                draggedParent = self.invisibleRootItem()
            draggedParent.removeChild(draggedItem)  # delete the dragged item
            # reinsert the dragged item
            draggedParent.insertChild(droppedIndex.row(), draggedItem)
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

    def set_theme_num(self, num):
        self.theme_num = num

    def get_theme_num(self):
        return self.theme_num


def transformInput(data: str):
    if "/" in data:
        i = data.find("/")
        return float(data[:i]) / float(data[i + 1:])
    return float(data)


class Course(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, data=["New Course", "", ""], *__args):
        super().__init__(parent, data)
        self.setFont(0, courseFont)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable |
            QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled |
            QtCore.Qt.ItemIsDropEnabled)

    def get_color(self, theme_num):
        if theme_num > 0:  # dark theme
            return QtCore.Qt.cyan
        else:  # light theme
            return QtCore.Qt.darkBlue

    def updateGrade(self):
        total_weight = 0.0
        earned_weight = 0.0
        extra_credit = 0.0
        for i in range(self.childCount()):
            t = self.child(i)
            weight = t.text(1)
            grade = t.text(2)
            if not isinstance(t, ExtraCredit):
                if not weight or not grade:  # if no weight is entered
                    continue
                total_weight += transformInput(weight)
                earned_weight += transformInput(weight) * transformInput(grade)
            else:
                if grade:
                    extra_credit += transformInput(grade)
        course_grade = str(earned_weight / total_weight +
                           extra_credit) if total_weight > 0 else ""
        self.setText(2, course_grade)


class AssignmentType(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, data=["New Assignment Type", "", ""], *__args):
        super().__init__(parent, data)
        self.setFont(0, typeFont)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable |
            QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled |
            QtCore.Qt.ItemIsDropEnabled)

        self.extraCredit = False

    def get_color(self, theme_num):
        if theme_num > 0:  # dark theme
            return QtCore.Qt.green
        else:  # light theme
            return QtCore.Qt.darkGreen

    def set_extra_credit(self, is_extra):
        self.extraCredit = is_extra

    def is_extra_credit(self):
        return self.extraCredit

    def updateGrade(self):
        # The general idea here is two handle two forms of grade entering.
        # 1) Assignments in the type have equal weighting
        # or 2) Assignments in the type are weighted differently
        # For example, you may have 3 midterms and they are carry the same
        #  weight. This would be scenario 1.
        # You may have a semester long project with checkpoints varying in
        #  weight i.e. the final product is worth the most and maybe the draft
        # is worth less - this is an example of scenario 2.
        # I highly doubt you would combine the two scenarios for a single type,
        # but there is theoretically support included via my magic below.
        # this sorcery is pretty much untested, so proceed with caution if
        # attempting to mix and match.

        # get all assignments with a grade included in calculation
        assigns = filter(lambda x: bool(x.text(2) and x.is_in_calculation()),
                         (self.child(i) for i in range(self.childCount())))
        weighted_grades = 0.0
        weight = 0.0
        non_weighted_grades = 0.0
        nnwnec = 0  # number of non weighted, non extra credit
        for assignment in assigns:
            w = assignment.text(1)
            grade = assignment.text(2)
            if w:
                if not assignment.is_extra_credit():
                    weight += transformInput(w)
                weighted_grades += transformInput(w) * transformInput(grade)
            else:
                if not assignment.is_extra_credit():
                    nnwnec += 1
                non_weighted_grades += transformInput(grade)
        print(weight, weighted_grades, non_weighted_grades, nnwnec)
        if weight == 0 and nnwnec == 0:
            type_grade = ""
        elif nnwnec == 0 and weight != 0:
            type_grade = str(weighted_grades/weight)
        else:
            wg = weighted_grades * (weight != 0)
            type_grade = f"{wg + (non_weighted_grades / nnwnec) * (1-weight)}"

        self.setText(2, type_grade)


class Assignment(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, data=["New Assignment", "", ""], *__args):
        super().__init__(parent, data)
        self.setFont(0, assFont)
        self.extraCredit = False
        self.in_calculation = True
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable |
            QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled)

    def get_color(self, theme_num):
        if theme_num > 0:  # dark theme
            return QtCore.Qt.yellow
        else:  # light theme
            return QtCore.Qt.blue

    def set_extra_credit(self, is_extra):
        self.extraCredit = is_extra

    def set_in_calculation(self, in_calculation):
        self.in_calculation = in_calculation

    def is_extra_credit(self):
        return self.extraCredit

    def is_in_calculation(self):
        return self.in_calculation


class ExtraCredit(AssignmentType):
    def __init__(self, parent, data=["Extra Credit", "", ""], *__args):
        super().__init__(parent, data)
        self.setFont(0, extraCreditFont)
        self.setFlags(
            QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable |
            QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsEnabled |
            QtCore.Qt.ItemIsDropEnabled)

    def updateGrade(self):
        type_grade = 0.0
        num_assignments = self.childCount()
        for i in range(num_assignments):
            grade = self.child(i).text(2)
            if grade:  # if the column is empty
                type_grade += transformInput(grade)
        type_grade = str(type_grade) if num_assignments > 0 \
            else ""
        self.setText(2, type_grade)
