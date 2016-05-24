'''
Created on May 23, 2016

@author: petterwildhagen
'''
from testrail import *
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import *
from TestSectionTree import *
from DiffTestrailProjects import *
from QSectionTreeWidget import *
'''
Class to display sections in a QWidget
'''
class CentralWidget(QWidget):
    def __init__(self,client,CPI_mID,parent):
        super(CentralWidget, self).__init__(parent)
        self.client = client
        self.CPEMasterID = CPI_mID
        self.layout = QtGui.QVBoxLayout(self)
        self.selectMode()
    def masterSuites(self):
        suites = self.client.send_get('get_suites/' + str(self.CPEMasterID))
        buttons = []
        for p in suites:
            buttons.append(QtGui.QPushButton(p['name']))
            self.layout.addWidget(buttons[-1])
            setattr(buttons[-1], 'ID', p['id'])
            setattr(buttons[-1],'name',p['name'])
            buttons[-1].clicked.connect(self.parent().suiteClk)
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        bbutton = QtGui.QPushButton('<< Back')
        quitb = QtGui.QPushButton('Quit')
        bbutton.clicked.connect(self.parent().selectMode)
        quitb.clicked.connect(self.parent().quit)
        hbox.addWidget(bbutton)
        hbox.addWidget(quitb)
        self.layout.addLayout(hbox)

    def selectMode(self): 
        mp = self.client.send_get('get_project/' + str(self.CPEMasterID))
        label = QtGui.QLabel("Master project is " + str(mp['name']))
        self.layout.addWidget(label)
        ml = QtGui.QLabel("Press 'Projects' to see difference to master\nPress 'Master' to maintain tests from master to projects")
        self.layout.addWidget(ml)
        mbutton = QtGui.QPushButton("Master")
        pbutton = QtGui.QPushButton("Projects")
        mbutton.clicked.connect(self.parent().masterSuites)
        pbutton.clicked.connect(self.parent().placeProjects)
 
        self.layout.addWidget(pbutton)
        self.layout.addWidget(mbutton)
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        quitb = QtGui.QPushButton('Quit')
        quitb.clicked.connect(self.parent().quit)
        hbox.addWidget(quitb)
        self.layout.addLayout(hbox)
    def suiteClk(self,suiteName,suiteId):
        # get the tree
        testTreeObj = TestTree(self.CPEMasterID,suiteName,self.client)
        testTree = testTreeObj.getTree()
        # display suite as a tree
        self.treeWidget = QSectionTreeWidget(testTree)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.treeWidget)
        self.layout.addLayout(layout)
        # quit button at the bottom
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        bbutton = QtGui.QPushButton('<< Back')
        quitb = QtGui.QPushButton('Quit')
        abutton = QtGui.QPushButton('Update tests to projects')
        abutton.clicked.connect(self.parent().updateTests)
        setattr(abutton,'name',suiteName)
        setattr(abutton,'id',suiteId)
        bbutton.clicked.connect(self.parent().masterSuites)
        quitb.clicked.connect(self.parent().quit)
        hbox.addWidget(abutton)
        hbox.addWidget(bbutton)
        hbox.addWidget(quitb)
        self.layout.addLayout(hbox)

    def placeProjects(self):
        mp = self.client.send_get('get_project/' + str(self.CPEMasterID))
        label = QtGui.QLabel("Click on one of the projects\nMaster CPE project is " + str(mp['name']))  
        self.layout.addWidget(label)
        project = self.client.send_get('get_projects')
        buttons = []
        for p in project:
            buttons.append(QtGui.QPushButton(p['name']))
            self.layout.addWidget(buttons[-1])
            setattr(buttons[-1], 'ID', p['id'])
            buttons[-1].clicked.connect(self.parent().projectClk)
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        bbutton = QtGui.QPushButton('<< Back')
        quitb = QtGui.QPushButton('Quit')
        bbutton.clicked.connect(self.parent().selectMode)
        quitb.clicked.connect(self.parent().quit)
        hbox.addWidget(bbutton)
        hbox.addWidget(quitb)
        self.layout.addLayout(hbox)
    
    def displaySuitesInProject(self,ID,name):
        plabel = QtGui.QLabel('Suites for project ' + name )
        slabel = QtGui.QLabel('Sections match\n master project?')
        tlabel = QtGui.QLabel('Tests match\n in master project?')
        hbox = QtGui.QHBoxLayout()      
        hbox.addWidget(plabel)
        hbox.addWidget(slabel)
        hbox.addWidget(tlabel)
        self.layout.addLayout(hbox)
    
        suiteDiffTree = compareSuites(self.CPEMasterID,ID,self.client)
        for i in range(0,len(suiteDiffTree)):
            print suiteDiffTree[i]
            hbox = QtGui.QHBoxLayout()
            self.layout.addLayout(hbox)
            slabel = QtGui.QLabel(suiteDiffTree[i]['name'])
            hbox.addWidget(slabel)
            foundTxt = "not found"
            if not suiteDiffTree[i]['found']:
                foundTxt = "not found"          
                flabel = QtGui.QLabel(foundTxt)
                hbox.addWidget(flabel)
            else:
                if not suiteDiffTree[i]['match']:
                    button = QtGui.QPushButton('Analyze sections')
                    button.clicked.connect(self.parent().analyzeSections)
                    setattr(button, 'sid', suiteDiffTree[i]['psid']) # attribute for suite id
                    setattr(button, 'mid', suiteDiffTree[i]['msid']) # attribute for suite id in master project
                    setattr(button, 'suitename' , suiteDiffTree[i]['name']) # attribute for suite name
                    setattr(button,'difftree',suiteDiffTree[i])
                    setattr(button,'pname',name)
                    button.setToolTip(str(suiteDiffTree[i]['diffStr']))
                    hbox.addWidget(button)
                else:
                    flabel = QtGui.QLabel('sections match')
                    hbox.addWidget(flabel)
                if not suiteDiffTree[i]['testMatch']:
                    button = QtGui.QPushButton('Analyze tests')
                    button.clicked.connect(self.parent().analyzeTests)
                    button.setToolTip(str(suiteDiffTree[i]['testDiffStr']))
                    setattr(button,'difftree',suiteDiffTree[i])
                    setattr(button,'pname',name)
                    hbox.addWidget(button)
                else:
                    tlabel = QtGui.QLabel('tests match')
                    hbox.addWidget(tlabel)
        ebox = QtGui.QHBoxLayout()
        self.layout.addLayout(ebox)
        button = QtGui.QPushButton('<< Back')
        qbutton = QtGui.QPushButton('Quit')
        button.clicked.connect(self.parent().goBackToProjects)  
        qbutton.clicked.connect(self.parent().quit)
        ebox.addStretch(1)   
        ebox.addWidget(button)
        ebox.addWidget(qbutton)        