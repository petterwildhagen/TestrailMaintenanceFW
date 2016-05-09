import sys
from testrail import *
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import QWidget, QVBoxLayout, QRect
from testrail_lib import *

class MainWindow(QtGui.QMainWindow):
    def __init__(self, username,password,parent=None):
        super(MainWindow, self).__init__(parent)
        self.username = username
        self.password = password
        #self.client = APIClient('https://getipn.testrail.net/')
        #self.client.user = username
        #self.client.password = password
        self.CPEMasterProject = 11
        self.layout = QVBoxLayout()
        self.allProjects = ProjectWidget(self)
        self.central_widget = self.allProjects

        self.setCentralWidget(self.central_widget)
        self.initUI()
        # sub windows
        self.lw = []
    def initUI(self):
        
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Testrail analysis tool - main window')   
    
        self.statusBar()
        self.show()


class ProjectWidget(QWidget):
    def __init__(self,parent):
        super(ProjectWidget, self).__init__(parent)
  
        self.layout = QtGui.QVBoxLayout(self)
        # add tree to window to display
        self.tree = QtGui.QTreeWidget()
        #tabWidget.addTab(self.tree, "Tree View")
        #self.connect(self.tree, QtCore.SIGNAL("itemDoubleClicked (QTreeWidgetItem *,int)"), self.on_tree_double_clicked)
        #self.connect(self.tree, QtCore.SIGNAL("itemClicked (QTreeWidgetItem *,int)"), self.on_tree_clicked)

        self.tree.setAnimated(True)
        self.tree.setRootIsDecorated(True)
        self.tree.setAlternatingRowColors(False)
        self.tree.header().setStretchLastSection(True)
        self.tree.headerItem().setText(0, "")
        self.tree.headerItem().setText(1, "Property")
        self.tree.headerItem().setText(2, "Value")
        self.tree.setColumnWidth(0, 100)
        self.tree.setColumnWidth(1, 150)
        
        self.layout.addWidget(self.tree)
 
        self.show()
        
if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
  
    window = MainWindow('petter.wildhagen@testify.no','Passord01')
    window.show()
    sys.exit(app.exec_())     
    