'''
Created on May 4, 2016
Class to represent a tree of tests organized in sections
@author: petterwildhagen
'''
from testrail_lib import testrailError
class SectionTree:
    def __init__(self,projectID,suiteName,client):
        self.projectID = projectID
        self.suiteName = suiteName
        self.client = client
        self.suiteID = self.getSuiteID(self.projectID)
        self.sectionTree = self.sections_JSON_tree(self.projectID, self.suiteID)
    '''
    Method to return section tree
    '''
    def getTree(self):
        return self.sectionTree 
    
    '''
    Method to get ID of the suite based on name
    Parameters:
    projectId - Id of the project to look for the suite ID
    Throws:
    testrailError if the suite cannot be found
    '''
    def getSuiteID(self,projectID):
        suites = self.client.send_get('get_suites/' + str(projectID))
        for i in range(0,len(suites)):
            if suites[i]['name'] == self.suiteName:
                return suites[i]['id']
        raise testrailError("Cannot find suite in project " + str(projectID) + " with name " + self.suiteName) 
    '''
    Function to create a JSON tree from a suite name in a project
    '''
    def sections_JSON_tree(self,projectID,suiteID):
        sections = self.client.send_get('get_sections/' + str(projectID) + '&suite_id=' + str(suiteID))
        sT = self.sections_JSONflat2tree(sections)
        return sT
    '''
    Method to create a tree structured JSON object from the flat structure returned from Testrail
    Parameters:
    json_in : the flat json object from testrail
    name : the name of the tree
    Returns:
    A JSON object with a tree Structure
    '''
    def sections_JSONflat2tree(self,inp):
        output = {'sections' : [],
              'id' : 1,
              'parent_id' : None,
              'name' : self.suiteName}

        for l in inp:
            if l['depth'] == 0:
                output['sections'].append({'name' : l['name'],
                                           'id' : l['id'],
                                           'sections' : [],
                                           'parent_id' : 1,
                                           'parent_name' : None
                                           })      
            else:
                self.append_section(output['sections'],l)
                # append paren relation names        
        return output
    '''
    Function to append a JSON object to the sections in a JSON tree
    Parameters:
    obj: the JSON tree to append the object to
    io : the object to append to the tree
    '''  
    def append_section(self,obj,io):
        for a in range(0,len(obj)):
            if obj[a]['id'] == io['parent_id']:
                obj[a]['sections'].append({'name' : io['name'],
                                           'id' : io['id'],
                                           'parent_id' : io['parent_id'],
                                           'parent_name' : io['name'],
                                           'sections' : []})
                return 
        for a in range(0,len(obj)):
            if len(obj[a]['sections']) > 0:
                self.append_section(obj[a]['sections'],io)
class TestTree:
    def __init__(self,projectID,suiteName,client):
        self.projectID = projectID
        self.suiteName = suiteName
        self.client = client
        self.suiteID = self.getSuiteID(self.projectID)
        st = SectionTree(self.projectID,self.suiteName,self.client)
        self.sectionTree = st.getTree()
        self.testTree = self.tests_JSON_tree(self.projectID, self.suiteID, self.sectionTree)
    '''
    Method to get the test tree
    '''
    def getTree(self):
        return self.testTree
    '''
    Method to get ID of the suite based on name
    Parameters:
    projectId - Id of the project to look for the suite ID
    Throws:
    testrailError if the suite cannot be found
    '''
    def getSuiteID(self,projectID):
        suites = self.client.send_get('get_suites/' + str(projectID))
        for i in range(0,len(suites)):
            if suites[i]['name'] == self.suiteName:
                return suites[i]['id']
        raise testrailError("Cannot find suite in project " + str(projectID) + " with name " + self.suiteName) 
    ''' 
    Method to get all tests for a particular suite 
    '''
    def tests_JSON_tree(self,projectId,suiteId,sectionTree):
        tests = self.client.send_get('get_cases/' + str(projectId) + '&suite_id=' + str(suiteId))
        sT = self.tests_JSONflat2tree(sectionTree,tests)
        return sT
    '''
    Function to create a tree structure of tests from a suite
    Parameters:
    sectionTree : tree structure of sections in the suite
    flatJSONtests : flat JSON object with tests for the 
    '''            
    def tests_JSONflat2tree(self,sectionTree,flatJSONtests):
        for a in range(0,len(flatJSONtests)):
            test = flatJSONtests[a]
            self.append_test_2_tree(sectionTree['sections'],test)
        return sectionTree
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
            return diffTree
        for a in range(0,len(diffTree['sections'])):
            self.appendTest2DiffTree(diffTree['sections'][a],dt)
        return diffTree  
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