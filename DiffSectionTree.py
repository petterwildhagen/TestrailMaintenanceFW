'''
Created on Apr 29, 2016

@author: petterwildhagen
'''
from testrail_lib import getParents
from testrail_lib import testrailError
from testrail_lib import titleInSections

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
            
        self.masterTree = None
        self.projectTree = None
        self.createTree()
 
    def createTree(self):
        masterSuiteID = self.getSuiteID(self.masterID)
        projectSuiteID = self.getSuiteID(self.projectID)
        self.masterTree = self.sections_JSON_tree(self.masterID, masterSuiteID)
        self.projectTree = self.sections_JSON_tree(self.projectID, projectSuiteID)
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
