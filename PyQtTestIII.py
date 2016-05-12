'''
Created on Apr 13, 2016

@author: petterwildhagen
'''

'''
Created on Apr 8, 2016

@author: petterwildhagen
'''
import sys
from testrail import *
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import *
#from testrail_lib import *
from DiffTestrailProjects import *
from UpdateTests import *

'''
Class to handle login to Testrail
'''
class Login(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setWindowTitle('Testrail analysis tool - Login')
        self.setGeometry(300, 300, 350, 150)
        self.nameLabel = QtGui.QLabel("Username:")
        self.textName = QtGui.QLineEdit(self)
        self.passwdLabel = QtGui.QLabel("Password:")
        self.textPass = QtGui.QLineEdit(self)
        self.textPass.setEchoMode(QtGui.QLineEdit.Password)
        self.buttonLogin = QtGui.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.textName)
        layout.addWidget(self.passwdLabel)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        try:
            client = APIClient('https://getipn.testrail.net/')
            client.user = self.textName.text()
            client.password = self.textPass.text()
            client.send_get('get_projects')
            self.username = self.textName.text()
            self.password = self.textPass.text()
            self.accept()
        except APIError as e:
            QtGui.QMessageBox.warning(self, 'Error',str(e))
    def getUsername(self):
        return self.username
    def getPassword(self):
        return self.password
'''
Class to define Testrail API Client login credentials
'''   
class TestrailAPIClient(APIClient):
    def __init__(self,username,password,host):
        print 'Instansiating APIClient ' + host + ' ' + username + ' ' + password
        APIClient.__init__(self, host)
        self.user = username
        self.password = password
'''
Class that defines the main window
Includes methods to navigate between cental widgets
'''        
class MainWindow(QtGui.QMainWindow):
    def __init__(self, username,password,parent=None):
        super(MainWindow, self).__init__(parent)
        self.username = username
        self.password = password
        self.client = APIClient('https://getipn.testrail.net/')
        self.client.user = username
        self.client.password = password
        self.CPEMasterProject = 11
        self.layout = QVBoxLayout()
        self.allProjects = ProjectWidget(self.client,self.CPEMasterProject,self)
        self.central_widget = self.allProjects
        self.subwindows = []
        self.setCentralWidget(self.central_widget)
        self.initUI()
    def initUI(self):
        
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Testrail analysis tool - main window')   
    
        self.statusBar()
        self.show()
    def quit(self):
        print 'Quitting!!'
        #QtGui.QApplication.instance().quit
        self.close()
    def removeWidgets(self):
        for c in self.central_widget.layout.children():          
            for w in reversed(range(c.count())):
                try:
                    c.itemAt(w).widget().setParent(None)
                except AttributeError:
                    print 'caught exception for widget in child layout', c ,'\n',w
            c.setParent(None)
        for i in reversed(range(self.central_widget.layout.count())): 
            try:
                self.central_widget.layout.itemAt(i).widget().setParent(None)
            except AttributeError:
                print 'caught exception for widget on main layout'
        print "Widgets removed"
    def projectClk(self):
        sender = self.sender()
        self.statusBar().showMessage('Project ' + sender.text() + ' selected')
        self.setWindowTitle('Testrail analysis tool - ' + str(sender.text()))
        self.show()  
        sender = self.sender()
        print "Project" , sender.ID , sender.text() , " was selected "
        self.removeWidgets()
        self.allProjects.displaySuitesInProject(sender.ID,sender.text())
    def suiteClk(self):
        sender = self.sender()
        suiteName = sender.name
        suiteID = sender.ID
        print "suiteClk " , sender.name , " pressed"
        self.removeWidgets()
        self.allProjects.suiteClk(suiteName,suiteID)
        self.statusBar().showMessage('Please select sections to update from')
    def goBackToProjects(self):     
        self.statusBar().showMessage('Returning to project overview')
        self.setWindowTitle('Testrail analysis tool - Main Window')
        self.removeWidgets()
        self.allProjects.placeProjects()
            
    def analyzeSections(self):   
        sender = self.sender()
        inp = sender.difftree
        name = sender.pname
        print 'Analyze suites ' , sender.sid , ' and suite ', sender.mid , ' name : ' ,sender.suitename
        # open a new window
        lw = AnalyzeSections(inp,name)
        lw.setGeometry(QRect(100, 100, 400, 200))
        lw.show()
        self.subwindows.append(lw)
    def analyzeTests(self):
        sender = self.sender()
        name = sender.pname
        inp = sender.difftree
        lw = AnalyzeTests(inp,name)
        lw.setGeometry(QRect(150,150,500,300))
        lw.show()
        self.subwindows.append(lw)
    def masterSuites(self):
        self.removeWidgets()
        self.allProjects.masterSuites()
        self.statusBar().showMessage('Please select a suite to update from')
        print "Master selected"
    def placeProjects(self):
        self.removeWidgets()
        self.allProjects.placeProjects()
        print "placeProjects selected"
    def selectMode(self):
        self.removeWidgets()
        self.allProjects.selectMode()
        self.statusBar().showMessage('Please select to update from master or verify projects')
    def updateTests(self):
        print "update sec called"
        sender = self.sender()
        #sections = sender.sections
        name = sender.name
        suiteId = sender.id
        sections = self.allProjects.treeWidget.getSec()
        print name, " " , sections
        self.statusBar().showMessage('Retrieving sections and test - please wait')
        u = UpdateTests(sections,self.CPEMasterProject,name,suiteId,self.client)
        #sections2update = u.getAllSections()
        ns = u.getSuites()
        if len(ns) > 0:
            self.statusBar().showMessage('Sections retrieved - starting update')
            u.updateAllTests()
            self.statusBar().showMessage('Update done')
        else:
            self.statusBar().showMessage('No projects have this suite ' + name)
              
'''
Class to display tests in a single suite in a QWidget
'''
class AnalyzeTests(QWidget):
    def __init__(self,inp,name):
        QWidget.__init__(self)
        self.layout = QtGui.QVBoxLayout(self)
        self.DiffTree = inp
        self.pname = name
        self.initUI()
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
    def quit(self):
        print "Quitting!"
        self.close()

'''
Class that handles selection tree to copy tests
'''
class SectionTree(QTreeWidget):
    def __init__(self,tree):
        QTreeWidget.__init__(self)
        self.tree = tree
        self.selected_sections = {}
        self.setHeaderHidden(True)
        self.itemChanged.connect (self.handleChangedTree)
        self.addItems(self.invisibleRootItem(),self.tree)
    '''
    Method to add sections to the QTreeWidget recursively
    '''
    def addItems(self,parent,tree):
        for a in range(0,len(tree['sections'])):
            sname = tree['sections'][a]['name']
            Id = tree['sections'][a]['id']
            item = QtGui.QTreeWidgetItem(parent, [sname])
            item.Id = Id
            item.title = sname
            item.setData(0,QtCore.Qt.UserRole,Id)
            if 'sections' in tree['sections'][a]:
                item.setFlags(item.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            else:
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(0, Qt.Unchecked)
            item.setExpanded (True)
            if 'sections' in tree['sections'][a].keys():
                self.addItems(item,tree['sections'][a])
    '''
    Method invoked when tree is changed - that is a checkbox is ticked/unticked
    '''
    def handleChangedTree(self,item,column):
        if item.checkState(column) == QtCore.Qt.Checked:
            self.selected_sections[item.Id] = item.title
        if item.checkState(column) == QtCore.Qt.Unchecked:
            if item.Id in self.selected_sections.keys():
                del self.selected_sections[item.Id]
        self.printSec
    def printSec(self):
        for a in self.selected_sections.keys():
            print self.selected_sections[a] , " " , a
    '''
    Method to get the selected sections
    Returns:
    dictionary object where the keys are the section ids and the values are the titles
    '''
    def getSec(self):
        return self.selected_sections
'''
Class to display sections in a QWidget
'''
class AnalyzeSections(QWidget):
    def __init__(self,inp,name):
        QWidget.__init__(self)
        self.layout = QtGui.QVBoxLayout(self)
        self.DiffTree = inp
        self.pname = name
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.pname + " - " + self.DiffTree['name'])
        # display differences in sections
        la = QtGui.QLabel("Sections in suite " + self.DiffTree['name'])
        hbox = QtGui.QHBoxLayout()          
        hbox.addWidget(la)
        self.layout.addLayout(hbox)
  
        diff = self.DiffTree['diffStr']
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

    def quit(self):
        print "Quitting!"
        self.close()
'''
Class to display sections in a QWidget
'''
class ProjectWidget(QWidget):
    def __init__(self,client,CPI_mID,parent):
        super(ProjectWidget, self).__init__(parent)
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
        self.treeWidget = SectionTree(testTree)
       
        #self.treeWidget.itemChanged.connect (self.handleChanged)
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
        #label = QtGui.QLabel("Click on one of the projects")  
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

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    '''
    login = Login()

    if login.exec_() == QtGui.QDialog.Accepted:
        window = MainWindow(login.getUsername(),login.getPassword())
        window.show()
        sys.exit(app.exec_())
    '''
    window = MainWindow('petter.wildhagen@testify.no','Passord01')
    window.show()
    sys.exit(app.exec_())   
    