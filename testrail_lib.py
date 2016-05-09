import json

import logging
'''
Created on Apr 4, 2016

@author: petterwildhagen
'''
#from distutils.sysconfig
#from PyQtTestII import TestrailAPIClient
import testrail
from _ctypes import Structure
from __builtin__ import True
#from getTestPlan import dt

''' 
Class for Testrail exceptions thrown in this library
'''
class testrailError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
'''
Configuration of the logger used in this library
'''
logger = logging.getLogger()
logger.setLevel(10)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
                
'''
Function to check if the a title is in a list of sections
Parameters:
t : the title to look for
sections :  a list of sections to search
Returns:
the index of the title if found, -1 if the title is not found
'''  
def titleInSections(t,sections):
    for i in range(len(sections)):
        if t == sections[i]['name']:
            return i
    return -1




# '''    
# Function to create diff tree between two suites
# Parameters:
# idMaster - the ID of the master suite
# idProject - the ID of the project where the suite is
# suitename - the name of the suite to diff
# client - the client to connect to the testrail DB
# Returns:
# diff tree that describes the differences between the suites
# Throws:
# testrailError if the master suite or project ID cannot be found
# '''
# def createDiffTree(idMaster,idProject,suitename,client):
# 
#     mT = sections_JSON_tree(idMaster,suitename,client) #sections_JSONflat2tree(masterSections,suitename)
#     pT = sections_JSON_tree(idProject,suitename,client) #sections_JSONflat2tree(projectSections,suitename)
#     tree = createSectionsDiffTree(mT, pT,suitename)
#     testsM = tests_JSON_tree(idMaster, suitename, mT, client)
#     testsP = tests_JSON_tree(idProject, suitename, pT, client)
#     tree = createTestDiffTree(testsM, testsP, tree)
#     return tree
# ''' 
# Function to create a diff tree of tests in two suites
# Parameters:
# idMaster - the ID of the master suite
# idProject - the ID of the project
# suitename - the name of the suite to diff the tests
# client - the client to connect to the Testrail DB
# Returns:
# diff tree that describes the differences between the tests
# Throws:
# testrailError if the master suite or project ID cannot be found
# '''
# def createSuiteDiffTree(idMaster,idProject,suitename,client):
#     mT = sections_JSON_tree(idMaster,suitename,client) #sections_JSONflat2tree(masterSections,suitename)
#     pT = sections_JSON_tree(idProject,suitename,client) #sections_JSONflat2tree(projectSections,suitename)
#     tree = createSectionsDiffTree(mT, pT,suitename)
#    
#     return tree
# '''
# Function to create a JSON tree from a suite name in a project
# '''
# def sections_JSON_tree(projectid,suitename,client):
#     suites = client.send_get('get_suites/' + str(projectid))
# 
#     projectSuiteID = None
#     for i in range(0,len(suites)):
#         if suites[i]['name'] == suitename:
#             projectSuiteID = suites[i]['id']
#     if projectSuiteID == None:
#         raise testrailError("Cannot find suite in project " + str(projectid) + " with name " + suitename) 
#     sections = client.send_get('get_sections/' + str(projectid) + '&suite_id=' + str(projectSuiteID))
#     sT = sections_JSONflat2tree(sections,suitename)
#     return sT
# ''' 
# Function to get all tests for a particular suite 
# '''
# def tests_JSON_tree(projectid,suitename,sectiontree,client):
#     suites = client.send_get('get_suites/' + str(projectid))
#     projectSuiteID = None
#     for i in range(0,len(suites)):
#         if suites[i]['name'] == suitename:
#             projectSuiteID = suites[i]['id']
#     if projectSuiteID == None:
#         raise testrailError("Cannot find suite in project " + str(projectid) + " with name " + suitename) 
#     tests = client.send_get('get_cases/' + str(projectid) + '&suite_id=' + str(projectSuiteID))
#     sT = tests_JSONflat2tree(sectiontree,tests)
#     return sT
# '''
# Function to create a diff tree in JSON format between two input trees
# Parameters:
# input1 - the first tree which is the source in the comparison
# input2 - the second tree which is the target in the comparison
# Returns:
# the diff tree describing the differences between the two input trees
# '''
# def createSectionsDiffTree(input1,input2,name):
#     diffTree = {'parent' : 'None',
#               'parents' : '',
#               'name' : name,
#               'id' : 1,
#               'sections': []}
#     return compareSectionTrees(input1,input2,diffTree)
# ''' 
# Function to create test diff tree
# Parameters:
# input1 - first JSON test tree
# input2 - second JSON test tree
# Returns:
# the diff tree describing differences between two input trees
# '''
# def createTestDiffTree(input1,input2,diffTree):
#     logger.info("Called creatTestDIffTree")
#     return compareTestTrees(input1,input2,diffTree)
# '''
# Function to compare two section trees
# Parameters:
# input1 - the first tree
# input2 - the second tree
# Returns:
# A JSON object that displays differences between the trees
# '''
# def compareSectionTrees(srcTree,tarTree,diffTree):
#     for a in range(0,len(srcTree['sections'])):
#         parents = getParents(diffTree, srcTree['id'],srcTree['name'])
#         dt = {'parent' : srcTree['name'],
#               'parents' : parents,
#                 'name' : srcTree['sections'][a]['name'],
#                 'parent_id' : srcTree['id'],
#                 'id' : srcTree['sections'][a]['id'],
#                 'sections' : []}
#         if a < len(tarTree['sections']):
#             if srcTree['sections'][a]['name'] == tarTree['sections'][a]['name']:  
#                 diffTree = append2DiffTree(diffTree,dt)        
#                 compareSectionTrees(srcTree['sections'][a],tarTree['sections'][a],diffTree)
#             else: 
#                 k = titleInSections(srcTree['sections'][a]['name'], tarTree['sections'])
#                 if k > -1:        
#                     dt['action'] = 'moved'
#                     diffTree = append2DiffTree(diffTree,dt)
#                     compareSectionTrees(srcTree['sections'][a],tarTree['sections'][k],diffTree)
#                 else:  
#                     dt['action'] = 'missing'
#                     diffTree = append2DiffTree(diffTree,dt)
#         else:
#             k = titleInSections(srcTree['sections'][a]['name'], tarTree['sections'])
#             if k >-1:
#                 dt['action'] = 'moved'
#                 diffTree = append2DiffTree(diffTree,dt)
#                 compareSectionTrees(srcTree['sections'][a],tarTree['sections'][k],diffTree)
#             else:           
#                 dt['action'] = 'missing'
#                 diffTree = append2DiffTree(diffTree,dt) 
#     return diffTree   
# 
# def compareTestTrees(srcTree,tarTree,diffTree):
#     for a in range(0,len(srcTree['sections'])):
#         if a < len(tarTree['sections']):
#             if srcTree['sections'][a]['name'] == tarTree['sections'][a]['name']:  
#                 # node names match- compare the tests
#                 diffTree = compareTests(srcTree['sections'][a],tarTree['sections'][a],diffTree)
#                 compareTestTrees(srcTree['sections'][a],tarTree['sections'][a],diffTree)
#             else: 
#                 k = titleInSections(srcTree['sections'][a]['name'], tarTree['sections'])
#                 if k > -1:       
#                     # nodes moved - compare tests in moved nodes 
#                     diffTree = compareTests(srcTree['sections'][a],tarTree['sections'][k],diffTree)
#                     compareTestTrees(srcTree['sections'][a],tarTree['sections'][k],diffTree)
#                 else:  
#                     # node missing - mark all tests as missing - if any
#                     diffTree = setTestsToMissing(srcTree['sections'][a],diffTree)
#         else:
#             k = titleInSections(srcTree['sections'][a]['name'], tarTree['sections'])
#             if k >-1:
#                 # node moved - compare tests in moved nodes
#                 diffTree = compareTests(srcTree['sections'][a],tarTree['sections'][k],diffTree)
#                 compareTestTrees(srcTree['sections'][a],tarTree['sections'][k],diffTree)
#             else:      
#                 # node missing - mark all tests as missing     
#                 diffTree = setTestsToMissing(srcTree['sections'][a],diffTree)
#     return diffTree    
# def compareTests(src,tar,diffTree):
#     if 'tests' in src.keys():
#         if 'tests' in tar.keys():
#             for i in range(0,len(src['tests'])):
#                 if i < len(tar['tests']):
#                     if src['tests'][i]['title'] != tar['tests'][i]['title']:
#                         ct = {'title' : src['tests'][i]['title'],
#                               'parent' : src['name']}
#                         if testInSection(src['tests'][i]['title'],tar['tests']) > -1:
#                             # test is moved, still in section
#                             ct['action'] = 'moved'
#                         else:
#                             # test is missing, mark as such
#                             ct['action'] = 'missing'
#                         diffTree = appendTest2DiffTree(diffTree, ct)
#                         
#                 else:
#                     ct = {'title' : src['tests'][i]['title'],
#                           'parent' : src['name']}
#                     if testInSection(src['tests'][i]['title'],tar['tests']) > -1:
#                         # test is moved, still in section
#                         ct['action'] = 'moved'
#                     else:
#                         # test is missing, mark as such
#                         ct['action'] = 'missing'
#                     diffTree = appendTest2DiffTree(diffTree, ct)
#     return diffTree  
# def setTestsToMissing(src,diffTree):
#     if len(src) > 0:
#         if 'tests' in src.keys():
#             for i in range(0,len(src['tests'])):
#                 ct = {'title' : src['tests'][i]['title'],
#                   'parent' : src['name'],
#                   'action' : 'missing'}
# 
#                 diffTree = appendTest2DiffTree(diffTree, ct)       
#     return diffTree                     
'''
Function that returns parent names of a node in a diffTree
Parameters:
diffTree: The diffTree to look for the parents in
id : the id of the node to look for
name : the name of the parent to look for
Returns:
A '/' separated parent sequence of the element
'''    
def getParents(diffTree,id,name):    
    p = getParent(diffTree, id,name)
    if p == None:
        return name
    ps = name
    while p != None:
        if p[1] != "None" and p != None:
            ps = p[1] + str('/') + ps
            #print p , " ** " , ps
            p = getParent(diffTree,p[0],p[1])
    return ps       
'''
Function that returns a list with the parent id and the parent name of a node
Parameters:
diffTree : the tree to look for the parent in
id : id of the node to look for
name : the name of the node to get the parent for
'''
def getParent(diffTree,id,name):
    for a in range(0,len(diffTree['sections'])):
        if diffTree['sections'][a]['id'] == id:   
            return [diffTree['id'],diffTree['sections'][a]['parent']]
    res = None
    for a in range(0,len(diffTree['sections'])):
        res = getParent(diffTree['sections'][a],id,name)
    return res
# '''
# Function that appends a section to a diff tree.
# The location where the node is appended is determined by matching the parent of the 
# node with the name of the node it will be appended to
# Parameters:
# diffTree - the diff tree to append the node to
# dt - the node to append to the diff tree
# Returns:
# the diff tree with the node appended to it
# '''        
# def append2DiffTree(diffTree,dt):
#     if dt['parent'] == diffTree['name']:
#         diffTree['sections'].append(dt)
#         return diffTree
#     for a in range(0,len(diffTree['sections'])):
#         append2DiffTree(diffTree['sections'][a],dt)
#     return diffTree  
# '''
# Function that appends test to diff tree
# The location where the node is appended is determined by matching the parent of the 
# the node with the name of the node it will be appended to
# Parameters:
# diffTree - the diff tree to append the node to
# dt - the node to append to the diff tree
# Returns:
# the diff tree with the node appended to it
# '''
# def appendTest2DiffTree(diffTree,dt):
#     if dt['parent'] == diffTree['name']:
#         if 'tests' not in diffTree.keys():
#             diffTree['tests'] = []
#         diffTree['tests'].append(dt)
#         return diffTree
#     for a in range(0,len(diffTree['sections'])):
#         appendTest2DiffTree(diffTree['sections'][a],dt)
#     return diffTree  

# '''
# Function to check if the a test is in a section
# Parameters:
# t : the test to look for
# section :  the section to search
# Returns:
# the index of the title if found, -1 if the title is not found
# '''  
# def testInSection(t,section):
#     for i in range(len(section)):
#         if t == section[i]['title']:
#             return i
#     return -1
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
                result.append(diffTree['sections'][a]['parents'] 
                              +'/'+diffTree['sections'][a]['name'] 
                              + diffTree['sections'][a]['tests'][k]['title'] 
                              + " was " + diffTree['sections'][a]['tests'][k]['action']) 
        if 'sections' in diffTree['sections'][a].keys():
            getTestDiffFromDiffTree(diffTree['sections'][a],result)
    return result

# '''
# Function to create a tree structured JSON object from the flat structure returned from Testrail
# Parameters:
# json_in : the flat json object from testrail
# name : the name of the tree
# Returns:
# A JSON object with a tree Structure
# '''
# def sections_JSONflat2tree(inp,name):
#     output = {'sections' : [],
#               'id' : 1,
#               'parent_id' : None,
#               'name' : name}
# 
#     for l in inp:
#         if l['depth'] == 0:
#             output['sections'].append({'name' : l['name'],
#                                     'id' : l['id'],
#                                     'sections' : [],
#                                     'parent_id' : 1,
#                                     'parent_name' : None
#                                     })      
#         else:
#             append_section(output['sections'],l)
#     # append paren relation names        
#     return output
# '''
# Function to append a JSON object to the sections in a JSON tree
# Parameters:
# obj: the JSON tree to append the object to
# io : the object to append to the tree
# '''  
# def append_section(obj,io):
#     for a in range(0,len(obj)):
#         if obj[a]['id'] == io['parent_id']:
#             obj[a]['sections'].append({'name' : io['name'],
#                                        'id' : io['id'],
#                                        'parent_id' : io['parent_id'],
#                                        'parent_name' : io['name'],
#                                        'sections' : []})
#             return 
#     for a in range(0,len(obj)):
#         if len(obj[a]['sections']) > 0:
#             append_section(obj[a]['sections'],io)
# '''
# Function to create a tree structure of tests from a suite
# Parameters:
# sectionTree : tree structure of sections in the suite
# flatJSONtests : flat JSON object with tests for the 
# '''            
# def tests_JSONflat2tree(sectionTree,flatJSONtests):
#     for a in range(0,len(flatJSONtests)):
#         test = flatJSONtests[a]
#         append_test_2_tree(sectionTree['sections'],test)
#     return sectionTree
# '''
# Function to append test to a sectionTree
# Parameters:
# sectionTree : the tree to append the test to
# test : the test to append to the section tree
# '''
# def append_test_2_tree(sectionTree,test):
# 
#     sid = test['section_id']
#     found = False
#     for a in range(0,len(sectionTree)):
#         if sid == sectionTree[a]['id']:
#             if 'tests' not in sectionTree[a].keys():
#                 sectionTree[a]['tests'] = []
#             sectionTree[a]['tests'].append(test)
#             found = True
#     if not found:
#         for a in range(0,len(sectionTree)):
#             if 'sections' in sectionTree[a].keys():
#                 append_test_2_tree(sectionTree[a]['sections'],test)
        
    