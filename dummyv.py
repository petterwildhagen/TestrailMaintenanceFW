'''
Created on May 4, 2016

@author: petterwildhagen
'''

'''
Created on May 4, 2016

@author: petterwildhagen
'''
import sys
from PyQt4 import QtCore, QtGui
from TestSectionTree import *
from testrail_lib import *
from testrail import *
class Window(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setHeaderHidden(False)
        client = APIClient('https://getipn.testrail.net/')
        client.user = 'petter.wildhagen@testify.no'
        client.password = 'Passord01'
        tree = TestTree(11,"WiFi",client)
        header = QtGui.QTreeWidgetItem(self.treeWidget.invisibleRootItem(), ["Section","Tests"])
        self.treeWidget.setHeaderItem(header)
        self.addItems2(self.treeWidget.invisibleRootItem(),tree.getTree())
        self.treeWidget.itemChanged.connect (self.handleChanged)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.treeWidget)
        self.setLayout(layout)
        
    def addItems2(self,parent,tree):
        for a in range(0,len(tree['sections'])):
            sname = tree['sections'][a]['name']
            item = QtGui.QTreeWidgetItem(parent, [sname])
            item.setData(0, QtCore.Qt.UserRole, "DAAATA")
            item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
            item.setExpanded (True)
            if 'sections' in tree['sections'][a].keys():
                self.addItems2(item,tree['sections'][a])
                
    def addItems(self, parent):
        column = 0
        clients_item = self.addParent(parent, column, 'Clients', 'data Clients')
        vendors_item = self.addParent(parent, column, 'Vendors', 'data Vendors')
        time_period_item = self.addParent(parent, column, 'Time Period', 'data Time Period')

        ch = self.addChild(clients_item, 1, 'Type A', 'data Type A')
        ch2 = self.addChild(ch, 0, 'TITLE', 'the data')
        self.addChild(ch2, 0, 'ANOTHER TITLE', 'SOME DATA')
        self.addChild(clients_item, column, 'Type B', 'data Type B')

        self.addChild(vendors_item, column, 'Mary', 'data Mary')
        self.addChild(vendors_item, column, 'Arnold', 'data Arnold')

        self.addChild(time_period_item, column, 'Init', 'data Init')
        self.addChild(time_period_item, column, 'End', 'data End')

    def addParent(self, parent, column, title, data):
        item = QtGui.QTreeWidgetItem(parent, [title])
        item.setData(column, QtCore.Qt.UserRole, data)
        item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
        item.setExpanded (True)
        return item

    def addChild(self, parent, column, title, data):
        item = QtGui.QTreeWidgetItem(parent, [title])
        item.setData(column, QtCore.Qt.UserRole, data)
        item.setCheckState (column, QtCore.Qt.Unchecked)
        return item

    def handleChanged(self, item, column):
        if item.checkState(column) == QtCore.Qt.Checked:
            print "checked", item, item.text(column)
        if item.checkState(column) == QtCore.Qt.Unchecked:
            print "unchecked", item, item.text(column)

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())