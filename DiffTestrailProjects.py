'''
Created on May 2, 2016

@author: petterwildhagen
'''
from DiffSectionTree import *
from DiffTestTrees import *

'''
Class that presents differences between tests
in one suite (in one diffTree)
'''

class PresentTestDifferences:
    def __init__(self,diffTree):
        self.diffTree = diffTree
        self.changedTests = []
        self.missingTests = []
        self.movedTests = []
        self.initChangedTests(self.diffTree)
    def initChangedTests(self,diffTree):
        for a in range(0,len(diffTree['sections'])):
            if 'tests' in diffTree['sections'][a].keys():
                for b in range(0,len(diffTree['sections'][a]['tests'])):
                    if 'change' in diffTree['sections'][a]['tests'][b].keys():
                        self.changedTests.append(diffTree['sections'][a]['tests'][b])
                    if 'action' in diffTree['sections'][a]['tests'][b].keys() and diffTree['sections'][a]['tests'][b]['action'] == "missing":
                        self.missingTests.append(diffTree['sections'][a]['tests'][b])
                    if 'action' in diffTree['sections'][a]['tests'][b].keys() and diffTree['sections'][a]['tests'][b]['action'] == "moved":
                        self.movedTests.append(diffTree['sections'][a]['tests'][b])
            if 'sections' in diffTree['sections'][a].keys():
                self.initChangedTests(diffTree['sections'][a])
    def getChangedTests(self):
        return self.changedTests
    def getMissingTests(self):
        return self.missingTests
    def getMovedTests(self):
        return self.movedTests
        
'''
Function to compare all suites between two projects.
Parameters:
masterID - the ID of the master project
projectID - the ID of the project to compare to the master
Returns:
a JSON object that describes the differences between the projects
''' 
def compareSuites(masterID,projectID,client):
    suites = client.send_get('get_suites/' + str(projectID))
    master_suites = client.send_get('get_suites/' + str(masterID))
    result = []
    for a in range(0,len(master_suites)):
        v = {'name' : master_suites[a]['name'],
             'found' : False,
             'match' : False,
             'testMatch' : False,
             'msid' : master_suites[a]['id']}
        for i in range(0,len(suites)):
            if master_suites[a]['name'] == suites[i]['name']:
                v['found'] = True
                v['psid'] = suites[i]['id']
                e = DiffSectionTrees(masterID,projectID,master_suites[a]['name'],client)
                t = DiffTestTrees(e,masterID,projectID,master_suites[a]['name'],client)
                diffTree = t.getDiffTree() 
                diffStr = []
                diffStr = getDiffFromDiffTree(diffTree,diffStr)
                if len(diffStr) == 0:
                    v['match'] = True
                else:
                    v['diffStr'] = diffStr
                    v['diffTree'] = diffTree
                testDiffStr = []
                testDiffStr = getTestDiffFromDiffTree(diffTree, testDiffStr)
                if len(testDiffStr) == 0:
                    v['testMatch'] = True
                else:
                    v['testDiffStr'] = testDiffStr
                    if 'diffTree' not in v.keys():
                        v['diffTree'] = diffTree
        result.append(v)
    return result

'''
Function to print a diff tree
Parameters:
diffTree - the diff tree to print
'''
def printDiffTree(diffTree):
    for a in range(0,len(diffTree['sections'])):
        if 'action' in diffTree['sections'][a].keys():
        
            print '**', ' ' , diffTree['sections'][a]['parents'],'/',diffTree['sections'][a]['name'] , '  was ' ,diffTree['sections'][a]['action']
            if 'tests' in diffTree['sections'][a].keys():
                for b in range(0,len(diffTree['sections'][a]['tests'])):
                    print ' --', ' ', diffTree['sections'][a]['tests'][b]['title'] , ' was ' , diffTree['sections'][a]['tests'][b]['action']
        if 'sections' in diffTree['sections'][a].keys():
            printDiffTree(diffTree['sections'][a])
'''
Function to print tree to flat format
Parameters:
tree- tree structure to print 
'''
def printTests(tree):
    for a in range(0,len(tree['sections'])):
        print 'section ' , tree['sections'][a]['name']
        if 'tests' in tree['sections'][a].keys():   
            for t in range(0,len(tree['sections'][a]['tests'])):                 
                print 'test, ' , tree['sections'][a]['tests'][t]['title']
        if 'sections' in tree['sections'][a].keys(): 
            printTests(tree['sections'][a])
'''
Function to extract differences from a diff tree
Parameters:
diffTree - the difftree to extract differences from
Returns:
differences found in diff tree
'''    
def getDiffFromDiffTree(diffTree,result):
    for a in range(0,len(diffTree['sections'])):
        if 'action' in diffTree['sections'][a].keys():
            result.append(diffTree['sections'][a]['parents'] +'/'+diffTree['sections'][a]['name'] + '  was ' +diffTree['sections'][a]['action'])
        if 'sections' in diffTree['sections'][a].keys():
            getDiffFromDiffTree(diffTree['sections'][a],result)
    return result
'''
Function to extract differences in tests from the diff tree
Parameters:
diffTree - the diff tree
'''
def getTestDiffFromDiffTree(diffTree,result):
    for a in range(0,len(diffTree['sections'])):
        if 'tests' in diffTree['sections'][a].keys():
            for k in range(0,len(diffTree['sections'][a]['tests'])):
                if 'action' in diffTree['sections'][a]['tests'][k].keys():
                    result.append(diffTree['sections'][a]['parents'] 
                              +'/'+diffTree['sections'][a]['name'] 
                              + '/'+diffTree['sections'][a]['tests'][k]['title'] 
                              + " was " + diffTree['sections'][a]['tests'][k]['action']) 
                if 'change' in diffTree['sections'][a]['tests'][k].keys():
                    summary = printTestDiff(diffTree['sections'][a]['tests'][k]['change'])
                    
                    result.append(diffTree['sections'][a]['parents'] 
                              +'/'+diffTree['sections'][a]['name'] 
                              + '/'+diffTree['sections'][a]['tests'][k]['title'] 
                              + summary)
        if 'sections' in diffTree['sections'][a].keys():
            getTestDiffFromDiffTree(diffTree['sections'][a],result)
    return result

'''
Function that returns printable string from dictionary that describes difference between tests
Parameter:
inDic - dictionary that describes difference between tests
'''
def printTestDiff(inDic): 
    rStr = ""
    if inDic['diffCode'] == "CONTENT_MISMATCH":
        rStr = " different in these fields: "
        for a in range(len(inDic['fields'])):
            rStr = rStr + ","+ inDic['fields'][a]['fieldName']
    elif inDic['diffCode'] == "FIELD_MISMATCH":
        rStr = " have different fields"
    elif inDic['diffCode'] == "FIELD_COUNT_MISMATCH":
        rStr = " have different number of fields"
    else:
        rStr = "Unknown deviation"
    return rStr