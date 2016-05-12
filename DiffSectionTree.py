'''
Created on Apr 29, 2016

@author: petterwildhagen
'''
from testrail_lib import getParents
from testrail_lib import testrailError
from testrail_lib import titleInSections
from TestSectionTree import SectionTree

'''
Class to create a diff tree for sections
'''
class DiffSectionTrees:
    def __init__(self,masterID,projectID,suiteName,client):
        self.masterID = masterID
        self.projectID = projectID
        self.suiteName = suiteName
        self.diffTree = None
        self.client = client  
        self.masterTree = SectionTree(self.masterID,self.suiteName,self.client).getTree()
        self.projectTree = SectionTree(self.projectID,self.suiteName,self.client).getTree()
        self.createTree()
 
    def createTree(self):
       
     
        self.diffTree = self.createSectionsDiffTree()
    def getDiffTree(self):
        return self.diffTree
    def getMasterTree(self):
        return self.masterTree
    def getProjectTree(self):
        return self.projectTree
    '''
    Method to create a diff tree in JSON format between two input trees
    Parameters:
    input1 - the first tree which is the source in the comparison
    input2 - the second tree which is the target in the comparison
    Returns:
    the diff tree describing the differences between the two input trees
    '''
    def createSectionsDiffTree(self):
        self.diffTree = {'parent' : 'None',
                  'parents' : '',
                  'name' : self.suiteName,
                  'id' : 1,
                  'sections': []}
        return self.compareSectionTrees(self.masterTree,self.projectTree,self.diffTree)
    '''
    Function to compare two section trees
    Parameters:
    input1 - the first tree
    input2 - the second tree
    Returns:
    A JSON object that displays differences between the trees
    '''
    def compareSectionTrees(self,srcTree,tarTree,diffTree):
        for a in range(0,len(srcTree['sections'])):
            parents = getParents(diffTree, srcTree['id'],srcTree['name'])
            dt = {'parent' : srcTree['name'],
                  'parents' : parents,
                    'name' : srcTree['sections'][a]['name'],
                    'parent_id' : srcTree['id'],
                    'id' : srcTree['sections'][a]['id'],
                    'sections' : []}
            if a < len(tarTree['sections']):
                if srcTree['sections'][a]['name'] == tarTree['sections'][a]['name']:  
                    diffTree = self.append2DiffTree(diffTree,dt)        
                    self.compareSectionTrees(srcTree['sections'][a],tarTree['sections'][a],diffTree)
                else: 
                    k = titleInSections(srcTree['sections'][a]['name'], tarTree['sections'])
                    if k > -1:        
                        dt['action'] = 'moved'
                        diffTree = self.append2DiffTree(diffTree,dt)
                        self.compareSectionTrees(srcTree['sections'][a],tarTree['sections'][k],diffTree)
                    else:  
                        dt['action'] = 'missing'
                        diffTree = self.append2DiffTree(diffTree,dt)
            else:
                k = titleInSections(srcTree['sections'][a]['name'], tarTree['sections'])
                if k >-1:
                    dt['action'] = 'moved'
                    diffTree = self.append2DiffTree(diffTree,dt)
                    self.compareSectionTrees(srcTree['sections'][a],tarTree['sections'][k],diffTree)
                else:           
                    dt['action'] = 'missing'
                    diffTree = self.append2DiffTree(diffTree,dt) 
        return diffTree   
    '''
    Method that appends a section to a diff tree.
    The location where the node is appended is determined by matching the parent of the 
    node with the name of the node it will be appended to
    Parameters:
    diffTree - the diff tree to append the node to
    dt - the node to append to the diff tree
    Returns:
    the diff tree with the node appended to it
    '''        
    def append2DiffTree(self,diffTree,dt):
        if dt['parent'] == diffTree['name']:
            diffTree['sections'].append(dt)
            return diffTree
        for a in range(0,len(diffTree['sections'])):
            self.append2DiffTree(diffTree['sections'][a],dt)
        return diffTree  
