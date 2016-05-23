'''
Created on May 18, 2016

@author: petterwildhagen
'''
'''
Class to display which tests are updated in which projects
'''    
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import *
class RunUpdateTests(QWidget):
    def __init__(self,tests,name,client):
        QWidget.__init__(self)
        self.tests = tests
        self.name = name
        self.client = client
        self.layout = QtGui.QVBoxLayout(self)
    
        self.setWindowTitle('Updating tests in suite ' + name)
        self.textField = QTextEdit()
        self.textField.append('Updating tests in ...')
        self.layout.addWidget(self.textField)
        ebox = QtGui.QHBoxLayout()
        button = QtGui.QPushButton('Quit')
        button.clicked.connect(self.quit)
        ebox.addStretch(1)   
        ebox.addWidget(button)
        self.layout.addLayout(ebox) 
    def runUpdates(self):     
        for test in self.tests:
            print test['test']['title']
            self.updateTest(test['id'], test['test'])
            self.textField.append('project: ' +  test['project_name'] + '\t id:' + str(test['id'])+ '\t title:' + test['test']['title'] )
        self.textField.append('\nUpdate done.')
    def updateTest(self,id,test):
        self.client.send_post('update_case/' + str(id),test)  