"""
Author: Jacob Rodal
Email: jr6ff@virginia.edu
Code repository: https://github.com/jrodal98/Grade_Manager
"""

from PyQt5 import QtGui

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
