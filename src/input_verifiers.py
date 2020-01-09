"""
Author: Jacob Rodal
Email: jr6ff@virginia.edu
Code repository: https://github.com/jrodal98/Grade_Manager
"""

from PyQt5 import QtWidgets, QtCore, QtGui
from widgets import GradebookTree, Assignment, AssignmentType, Course
import re


class ValidWeightGradeValidator(QtGui.QValidator):
    def __init__(self, parent=None):
        QtGui.QValidator.__init__(self, parent)

    def validate(self, line, pos):
        """
        Handles the validation of grades and weights.

        Intermediate means that the input isn't valid yet, but it
        might be valid soon.

        Acceptable means that the input is valid
        """
        # divide by 0 checker
        if re.match(r".*\/0([^.]|$|\.(0{4,}.*|0{1,4}([^0-9]|$))).*", line):
            return QtGui.QValidator.Intermediate, line, pos

        if line in ("", "0", "1") or \
                re.match(r"^0?\.\d+|\d*\.?\d+/\d*\.?\d+$", line):
            return QtGui.QValidator.Acceptable, line, pos
        elif re.match(r"^|0?\.\d*|\d*\.?\d*/\d*\.?\d*$", line):
            return QtGui.QValidator.Intermediate, line, pos
        else:
            return QtGui.QValidator.Invalid, line, pos


class ValidWeightGradeInput(QtWidgets.QItemDelegate):
    def createEditor(self, parent, option, index):
        line = QtWidgets.QLineEdit(parent)
        line.setValidator(ValidWeightGradeValidator())
        return line


class FloatDelegate(QtWidgets.QItemDelegate):
    def __init__(self, decimals, parent: GradebookTree):
        self.treeWidget = parent
        super(FloatDelegate, self).__init__(parent=parent)
        self.nDecimals = decimals

    def createEditor(self, parent, option, index):
        # if any of the below conditions are met, then the cell is editable.
        # basically, if the first index is zero, then it's editable
        # if the weight column for the assignment type item is selected,
        # then it's editable. if the grade column for the assignment item
        #  is selected, it's editable in all other cases, it's not editable.
        if index.column() == 0:
            return QtWidgets.QItemDelegate.createEditor(self, parent,
                                                        option, index)
        elif (
                index.column() == 1 and not isinstance(
                    self.treeWidget.itemFromIndex(index), Course)) or (
                index.column() == 2 and isinstance(
                    self.treeWidget.itemFromIndex(index), Assignment)):

            return ValidWeightGradeInput.createEditor(self, parent,
                                                      option, index)
        else:
            return None

    def paint(self, painter, option, index):
        item = self.treeWidget.itemFromIndex(index)
        if index.column() != 0:
            cg = QtGui.QPalette.Normal if option.state \
                & QtWidgets.QStyle.State_Enabled else QtGui.QPalette.Disabled
            option.palette.setColor(cg, QtGui.QPalette.Text, item.get_color(
                self.treeWidget.get_theme_num()))
            option.font = item.font(0)
            option.displayAlignment = QtCore.Qt.AlignCenter

        super(FloatDelegate, self).paint(painter, option, index)

    def drawDisplay(self, painter, option, rect, text):
        if "/" not in text:
            try:
                text = "{:.{}f}".format(float(text) * 100, self.nDecimals)
            except ValueError:
                pass
        super(FloatDelegate, self).drawDisplay(painter, option, rect, text)
