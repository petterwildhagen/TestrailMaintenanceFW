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
from RunUpdateTests import *
from DiffTestrailProjects import *
from TestsAndSuitesToUpdate import *
from IterableUpdateTests import *
from AnalyzeSections import *
from AnalyzeTests import *
from QSectionTreeWidget import *
from CentralWidget import *
from Login import *

'''
Class that defines the main window
Includes methods to navigate between cental widgets
'''        
class MainWindow(QtGui.QMainWindow):
    '''
    Init method.
    The method sets the main layout and the central widget to class ProjectWidget
    Parameters:
    username - the username to log into Testrail
    password - the password to log into Testrail
    '''
    def __init__(self, username,password,parent=None):
        super(MainWindow, self).__init__(parent)
        self.username = username
        self.password = password
        self.client = APIClient('https://getipn.testrail.net/')
        self.client.user = username
        self.client.password = password
        self.CPEMasterProject = 11
        self.layout = QVBoxLayout()
        self.centralWidget = CentralWidget(self.client,self.CPEMasterProject,self)
        self.central_widget = self.centralWidget
        self.subwindows = []
        self.setCentralWidget(self.central_widget)
        self.initUI()
    def initUI(self):      
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Testrail analysis tool - main window')       
        self.statusBar()
        self.show()
    '''
    Method to quit the main application
    '''
    def quit(self):
        print 'Quitting!!'
        self.close()
    '''
    Method to remove all widgets from the central_widget
    '''
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
    '''
    Method invoked when a project is selected. 
    Invokes method to display all suites in the project.
    The method relies on the sender object to pass attributes from the caller
    '''
    def projectClk(self):
        sender = self.sender()
        self.statusBar().showMessage('Project ' + sender.text() + ' selected')
        self.setWindowTitle('Testrail analysis tool - ' + str(sender.text()))
        self.show()  
        self.removeWidgets()
        self.centralWidget.displaySuitesInProject(sender.ID,sender.text())
    '''
    Method that is invoked when a suite is selected (clicked) to update tests from.
    Invokes method suiteClk of central_widget to display a section tree of the suite.
    The method relies on the sender object to pass attributes from the caller.
    '''
    def suiteClk(self):
        sender = self.sender()
        suiteName = sender.name
        suiteID = sender.ID
        self.removeWidgets()
        self.centralWidget.suiteClk(suiteName,suiteID)
        self.statusBar().showMessage('Please select sections to update from')
    '''
    Method invoked to go to the 'display all projects' page.
    Invokes metho of central widget placeProject to display all projects.
    '''
    def goBackToProjects(self):     
        self.statusBar().showMessage('Returning to project overview')
        self.setWindowTitle('Testrail analysis tool - Main Window')
        self.removeWidgets()
        self.centralWidget.placeProjects()
    '''
    Method invoked when 'analyze sections' is pressed.
    An instance of 'AnalyzeSections' is added to subwindows and displays the result
    '''        
    def analyzeSections(self):   
        sender = self.sender()
        inp = sender.difftree
        name = sender.pname
        lw = AnalyzeSections(inp,name)
        lw.setGeometry(QRect(100, 100, 400, 200))
        lw.show()
        self.subwindows.append(lw)
    '''
    Method invoked when 'analyze tests' is pressed.
    An instance of 'AnalyzeTests' is added to subwindows and displays the result
    '''    
    def analyzeTests(self):
        sender = self.sender()
        name = sender.pname
        inp = sender.difftree
        lw = AnalyzeTests(inp,name)
        lw.setGeometry(QRect(150,150,500,300))
        lw.show()
        self.subwindows.append(lw)
    '''
    Method invoked when Master Suite is selected.
    Invokes masterSuites of central_widget
    '''
    def masterSuites(self):
        self.removeWidgets()
        self.centralWidget.masterSuites()
        self.statusBar().showMessage('Please select a suite to update from')
        print "Master selected"
    '''
    Method invoked when Master Suite is selected.
    Invokes placeProjects of central_widget
    '''
    def placeProjects(self):
        self.removeWidgets()
        self.centralWidget.placeProjects()
    '''
    Method to select mode
    Invokes selectMode in central_widget
    '''
    def selectMode(self):
        self.removeWidgets()
        self.centralWidget.selectMode()
        self.statusBar().showMessage('Please select to update from master or verify projects')
    '''
    Method called to update tests.
    Creates instance of TestsAndSuitesToUpdate which provides data to 
    an instance of class IterableUpdateTests. If there are any tests to 
    update then this class will provide them in a list.
    Method relies on object from self.sender() to propagate name and if of suite.
    If any projects have suites matching suite name, then method updateAllTests is 
    invoked to update tests in all projects where present.
    '''
    def updateTests(self):
        sender = self.sender()
        name = sender.name
        suiteId = sender.id
        sections = self.centralWidget.treeWidget.getSec()
        self.statusBar().showMessage('Retrieving sections and test - please wait')
        u = TestsAndSuitesToUpdate(sections,self.CPEMasterProject,name,suiteId,self.client)
        iu = IterableUpdateTests(u.getSuites(),u.getTests())
        lst = iu.getIterableTestsToUpdate()
        ns = u.getSuites()
        if len(ns) > 0 and len(lst) > 0:
            self.statusBar().showMessage('Sections retrieved - starting update')
            for a in lst:
                print a
            rut = RunUpdateTests(lst,name,self.client)
            rut.setGeometry(QRect(250,250,700,500))
            rut.show()
            self.subwindows.append(rut)
            self.statusBar().showMessage('Running update')
            rut.runUpdates()
            self.statusBar().showMessage('Please select a suite to update from')
        else:
            if ns == 0:
                self.statusBar().showMessage('No projects have this suite ' + name)
            else:
                self.statusBar().showMessage('No projects have tests from master in suite ' + name)




if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    
    login = Login()

    if login.exec_() == QtGui.QDialog.Accepted:
        window = MainWindow(login.getUsername(),login.getPassword())
        window.show()
        sys.exit(app.exec_())