"""
Author: Jacob Rodal
Email: jr6ff@virginia.edu
Code repository: https://github.com/jrodal98/Grade_Manager
"""

from PyQt5 import QtWidgets, QtCore
from fonts import courseFont, assFont, extraCreditFont, typeFont


class KeyPressedTree(QtWidgets.QTreeWidget):
    keyPressed = QtCore.pyqtSignal(int)
    order_swapped = False
    current_course = -1
    theme_num = 0

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
