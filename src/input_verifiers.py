"""
Author: Jacob Rodal
Email: jr6ff@virginia.edu
Code repository: https://github.com/jrodal98/Grade_Manager
"""

from PyQt5 import QtWidgets, QtCore, QtGui
from widgets import KeyPressedTree, Assignment, AssignmentType


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
        # if the weight column for the assignment type item is selected,
        # then it's editable. if the grade column for the assignment item
        #  is selected, it's editable in all other cases, it's not editable.
        if index.column() == 0:
            return QtWidgets.QItemDelegate.createEditor(self, parent,
                                                        option, index)
        elif (
                index.column() == 1 and isinstance(
                    self.treeWidget.itemFromIndex(index), AssignmentType)) or (
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
