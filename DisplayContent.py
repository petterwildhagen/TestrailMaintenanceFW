'''
Created on May 24, 2016

@author: petterwildhagen
'''
'''
Class to display which tests are updated in which projects
'''    
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import *
class DisplayContent(QWidget):
    '''
    init method that creates widget
    '''
    def __init__(self):
        QWidget.__init__(self)

        self.layout = QtGui.QVBoxLayout(self)
        self.textField = QTextEdit()
        self.layout.addWidget(self.textField)
        ebox = QtGui.QHBoxLayout()
        button = QtGui.QPushButton('Quit')
        button.clicked.connect(self.quit)
        ebox.addStretch(1)   
        ebox.addWidget(button)
        self.layout.addLayout(ebox) 
    '''
    Method to display content in Window
    '''
    def displayContent(self,content):     
        for line in content:
            print line
            self.textField.append(line)
        self.textField.append('------')
    '''
    method to close the widget
    '''
    def quit(self):
        self.close()