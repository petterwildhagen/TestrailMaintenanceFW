'''
Created on May 23, 2016

@author: petterwildhagen
'''

from testrail import *
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import *
'''
Class to display test differences in a single suite in a QWidget
'''
class AnalyzeTests(QWidget):
    '''
    init method.
    Parameters:
    inp - the diff tree to display
    name - name of the project
    '''
    def __init__(self,inp,name):
        QWidget.__init__(self)
        self.layout = QtGui.QVBoxLayout(self)
        self.DiffTree = inp
        self.pname = name
        self.initUI()
    '''
    method to display test differences in the widget
    '''
    def initUI(self):
        self.setWindowTitle(self.pname + " - " + self.DiffTree['name'])
        # display differences in sections
        la = QtGui.QLabel("Tests in suite " + self.DiffTree['name'])
        hbox = QtGui.QHBoxLayout()          
        hbox.addWidget(la)
        self.layout.addLayout(hbox)
  
        diff = self.DiffTree['testDiffStr']
        for i in range(0,len(diff)):
            hbox = QtGui.QHBoxLayout()
            l = QtGui.QLabel(str(diff[i]))
            hbox.addWidget(l)
            self.layout.addLayout(hbox)
            
        ebox = QtGui.QHBoxLayout()
        button = QtGui.QPushButton('Quit')
        button.clicked.connect(self.quit)
        ebox.addStretch(1)   
        ebox.addWidget(button)
        self.layout.addLayout(ebox)
    '''
    method to close the widget
    '''
    def quit(self):
        self.close()