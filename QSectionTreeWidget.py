'''
Created on May 23, 2016

@author: petterwildhagen
'''
from testrail import *
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import *
'''
Class that handles selection tree to copy tests.
The class displays all sections in a suite in a tree structure.
The class allows to select sections and access the selected sections
in a get method
'''
class QSectionTreeWidget(QTreeWidget):
    '''
    init method.
    The method calls method addItems to build the tree to display in the GUI.
    Parameters:
    tree - section tree of a suite
    '''
    def __init__(self,tree):
        QTreeWidget.__init__(self)
        self.tree = tree
        self.selected_sections = {}
        self.setHeaderHidden(True)
        self.itemChanged.connect (self.handleChangedTree)
        self.addItems(self.invisibleRootItem(),self.tree)
    '''
    Method to add sections to the QTreeWidget recursively
    Parameters 
    parent - the element to add subsequent elements to
    tree - the section tree to traverse.
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
    The method updates member selected_sections accordingly.
    '''
    def handleChangedTree(self,item,column):
        if item.checkState(column) == QtCore.Qt.Checked:
            self.selected_sections[item.Id] = item.title
        if item.checkState(column) == QtCore.Qt.Unchecked:
            if item.Id in self.selected_sections.keys():
                del self.selected_sections[item.Id]
    '''
    Method to get the selected sections
    Returns:
    dictionary object where the keys are the section ids and the values are the titles
    '''
    def getSec(self):
        return self.selected_sections

    '''
    method to close the widget
    '''
    def quit(self):
        self.close()
