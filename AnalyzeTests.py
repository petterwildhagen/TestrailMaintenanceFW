'''
Created on May 23, 2016

@author: petterwildhagen
'''

from testrail import *
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import *
from DisplayContent import DisplayContent
'''
Class to display test differences in a single suite in a QWidget
'''
class AnalyzeTests(DisplayContent):
    '''
    init method.
    Parameters:
    inp - the diff tree to display
    name - name of the project
    '''
    def __init__(self,inp,name):
        DisplayContent.__init__(self)
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
        self.displayContent(diff)
