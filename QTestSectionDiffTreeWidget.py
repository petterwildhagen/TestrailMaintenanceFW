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
class QTestSectionDiffTreeWidget(QTreeWidget):
    '''
    init method.
    The method calls method addItems to build the tree to display in the GUI.
    Parameters:
    tree - the diff tree of a suite as returned from class DiffTestTrees
    '''
    def __init__(self,tree):
        QTreeWidget.__init__(self)
        self.tree = tree
        self.setHeaderHidden(True)
        #self.itemChanged.connect (self.handleChangedTree)
        self.addItems(self.invisibleRootItem(),self.tree)
    '''
    Method to add sections to the QTreeWidget recursively
    Parameters 
    parent - the element to add subsequent elements to
    tree - the section tree to traverse.
    '''
    def addItems(self,parent,tree):
        # add elements to tree