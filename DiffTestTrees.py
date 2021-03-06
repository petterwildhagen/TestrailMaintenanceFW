'''
Created on Apr 29, 2016

@author: petterwildhagen
'''

from testrail_lib import titleInSections
#from testrail_lib import testrailError
from TestSectionTree import TestTree

class DiffTestTrees:
    def __init__(self,sectionDiffTree,masterId,projectId,suitename,client):
        self.sectionDiffTree = sectionDiffTree
        self.projectID = projectId
        self.masterID = masterId
        self.suiteName = suitename
        self.client = client
        self.masterTree = TestTree(self.masterID,self.suiteName,self.client).getTree()
        self.projectTree = TestTree(self.projectID,self.suiteName,self.client).getTree()
        self.diffTree = self.sectionDiffTree.getDiffTree()
        self.createTree()
    ''' 
    Method to create a diff tree that contains tests that are moved or that are missing
    or where the content is changed
    '''
    def createTree(self):

        self.compareTestTrees(self.masterTree,self.projectTree) #,self.sectionDiffTree.getDiffTree())
    def getDiffTree(self):
        return self.diffTree
    '''
    Method to compare two test trees
    Parameters:
    srcTree - the source of the comparison
    tarTree - the target for the comparison
    diffTree - the diff tree to generate
    '''
    def compareTestTrees(self,srcTree,tarTree): #,diffTree):
        for a in range(0,len(srcTree['sections'])):
            if a < len(tarTree['sections']):
                if srcTree['sections'][a]['name'] == tarTree['sections'][a]['name']:  
                    # node names match- compare the tests
                    self.compareTests(srcTree['sections'][a],tarTree['sections'][a]) #,diffTree)
                    self.compareTestTrees(srcTree['sections'][a],tarTree['sections'][a]) #,diffTree)
                else: 
                    k = titleInSections(srcTree['sections'][a]['name'], tarTree['sections'])
                    if k > -1:       
                        # nodes moved - compare tests in moved nodes 
                        self.compareTests(srcTree['sections'][a],tarTree['sections'][k]) #,diffTree)
                        self.compareTestTrees(srcTree['sections'][a],tarTree['sections'][k]) #,diffTree)
                    else:  
                        # node missing - mark all tests as missing - if any
                        self.setTestsToMissing(srcTree['sections'][a])
            else:
                k = titleInSections(srcTree['sections'][a]['name'], tarTree['sections'])
                if k >-1:
                    # node moved - compare tests in moved nodes
                    self.compareTests(srcTree['sections'][a],tarTree['sections'][k]) #,diffTree)
                    self.compareTestTrees(srcTree['sections'][a],tarTree['sections'][k]) #,diffTree)
                else:      
                    # node missing - mark all tests as missing   
                    self.setTestsToMissing(srcTree['sections'][a]) #,diffTree)
           
    '''
    Method to compare tests in a section. Differences can be that a test is 'moved' or 'missing'.
    Parameters:
    src - src sectionof comparison
    tar - tar section of comparison
    '''
    def compareTests(self,src,tar):
        if 'tests' in src.keys():
            if 'tests' in tar.keys():
                for i in range(0,len(src['tests'])):
                    if i < len(tar['tests']):
                        if src['tests'][i]['title'] != tar['tests'][i]['title']:
                            ct = {'title' : src['tests'][i]['title'],
                                  'parent' : src['name']}
                            k = self.testInSection(src['tests'][i]['title'],tar['tests'])
                            if k > -1:
                                # test is moved, still in section
                                ct['action'] = 'moved'
                                change = self.compare2tests(src['tests'][i],tar['tests'][k])
                                if change != None:
                                    ct['change'] = change
                            else:
                                # test is missing, mark as such
                                ct['action'] = 'missing'
                            #diffTree = 
                            self.appendTest2DiffTree(self.diffTree, ct)
                        else:     
                            change = self.compare2tests(src['tests'][i],tar['tests'][i])  
                            if change != None:
                                ct = {}
                                ct['title'] = src['tests'][i]['title']
                                ct['parent'] = src['name']
                                ct['change'] = change
                                self.appendTest2DiffTree(self.diffTree, ct)
                    else:
                        ct = {'title' : src['tests'][i]['title'],
                              'parent' : src['name']}
                        k = self.testInSection(src['tests'][i]['title'],tar['tests'])
                        if k > -1:
                            # test is moved, still in section
                            ct['action'] = 'moved'
                            change = self.compare2tests(src['tests'][i],tar['tests'][k])
                            if change != None:
                                ct['change'] = change
                        else:
                            # test is missing, mark as such
                            ct['action'] = 'missing'
                        #diffTree = 
                        self.appendTest2DiffTree(self.diffTree, ct)
            else:   
                self.setTestsToMissing(src)
        #return diffTree  
    '''
    Method to set all tests in a section to missing
    Parameters:
    src - the section were all tests should be set to missing
    diffTree - the diff tree to append the missing tests to
    '''
    def setTestsToMissing(self,src):
        if len(src) > 0:
            if 'tests' in src.keys():
                for i in range(0,len(src['tests'])):
                    ct = {'title' : src['tests'][i]['title'],
                      'parent' : src['name'],
                      'action' : 'missing'}
    
                    self.appendTest2DiffTree(self.diffTree, ct)       
        #return diffTree      

    '''
    Method that appends test to diff tree
    The location where the node is appended is determined by matching the parent of the 
    the node with the name of the node it will be appended to
    Parameters:
    diffTree - the diff tree to append the node to
    dt - the node to append to the diff tree
    Returns:
    the diff tree with the node appended to it
    '''
    def appendTest2DiffTree(self,diffTree,dt):
        if dt['parent'] == diffTree['name']:
            if 'tests' not in diffTree.keys():
                diffTree['tests'] = []
            diffTree['tests'].append(dt)
            return #diffTree
        for a in range(0,len(diffTree['sections'])):
            self.appendTest2DiffTree(diffTree['sections'][a],dt)
        return #diffTree  
    '''
    Function to append test to a sectionTree
    Parameters:
    sectionTree : the tree to append the test to
    test : the test to append to the section tree
    '''
    def append_test_2_tree(self,sectionTree,test):
        sid = test['section_id']
        found = False
        for a in range(0,len(sectionTree)):
            if sid == sectionTree[a]['id']:
                if 'tests' not in sectionTree[a].keys():
                    sectionTree[a]['tests'] = []
                sectionTree[a]['tests'].append(test)
                found = True
        if not found:
            for a in range(0,len(sectionTree)):
                if 'sections' in sectionTree[a].keys():
                    self.append_test_2_tree(sectionTree[a]['sections'],test)
                    
    '''
    Method to check if the a test is in a section
    Parameters:
    t : the test to look for
    section :  the section to search
    Returns:
    the index of the title if found, -1 if the title is not found
    '''  
    def testInSection(self,t,section):
        for i in range(len(section)):
            if t == section[i]['title']:
                return i
        return -1
    '''
    Method to check for difference between two tests
    Parameters:
    srcTest - the source for comparison
    tarTest - the target for comparison
    Returns:
    a JSON object describing the differences between the two tests
    '''
    def compare2tests(self,srcTest,tarTest):
        a = sorted(srcTest.keys())
        b = sorted(tarTest.keys())
        d = None
        # compare keys, if different check type
        if len(a) != len(b):        
            d = {
                 'diffCode' : 'FIELD_COUNT_MISMATCH'
            }
        elif a == b:
            # same length, same keys, check fields
            d = self.compareTestFields(srcTest,tarTest)
        else: 
            # same length, different fields
            d = {'diffCode' : 'FIELD_MISMATCH',
                 #'diffTxt' : 'Tests do not have the same fields'
                 }
        return d   
    '''
    Method that compares the values of two dictionaries that have identical keys
    Parameteres:
    srcFields - the src for comparison
    tarFields - the target for comparison
    Returns:
    A dictionary object that describes the differences between the src and the tar input arguments
    '''
    def compareTestFields(self,srcFields,tarFields):
        blackList = ['id','section_id','milestone_id','refs','created_by','created_on','updated_on',
                     'updated_by','estimate','suite_id','estimate_forecast']
        sk = srcFields.keys()
        d = None
        for i in sk:
            if i not in blackList:
                if srcFields[i] != tarFields[i]:
                    if d == None:
                        d = {}
                    if 'fields' not in d.keys():
                        d['fields'] = []
                    d['fields'].append({'fieldName' : i, 'diff' : str(srcFields[i]) + " <> " + str(tarFields[i])})             
        if d != None:
            d['diffCode'] = 'CONTENT_MISMATCH'
        return d