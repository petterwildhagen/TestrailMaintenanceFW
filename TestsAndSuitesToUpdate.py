'''
Created on May 6, 2016

Class to extract a list of tests to be updated from sections
as well as a list of suites in project where these updates are to be run
This class provides input data to class IterableUpdateTests

@author: petterwildhagen
'''

class TestsAndSuitesToUpdate():
    '''
    init method: 
    Initializes class by extracting all tests in master project to use as source for update
    by calling self.getTests() and then extracting for each project if suite exists all sections
    that can be updated by calling self.addAllSections() 
    Parameters:
    sections: dictionary with sections (id,name) in master project to use as source in update
    masterID: the ID of the master project
    suite_name: the name of suite to update
    suiteID: the ID of the suite in the master project
    client: client to connect to the Testrail DB
    '''
    def __init__(self,sections,masterID,suite_name,suiteId,client):
        self.suiteName = suite_name
        self.suiteId = suiteId
        self.masterID = masterID
        self.client = client
        self.sections = sections
        self.tests = []
        self.extractTests()
        self.suites = self.getAllSuites()
        self.addAllSections()
    '''
    Method that adds tests to member test which is a list of sections that has objects 
    that contain tests
    '''
    def extractTests(self):
        #self.tests = {'sections' : []}
        for s in self.sections.keys():
            tests = self.client.send_get('get_cases/' + str(self.masterID) + '&suite_id=' + str(self.suiteId) + 
                                         '&section_id=' + str(s))
            tests = self.removeFields(tests)
            obj = {'section_id' : s,
                   'title' : self.sections[s],
                   'tests' : tests}    
            self.tests.append(obj)
        
    '''
    Method to remove fields that are not to be part of update
    '''
    def removeFields(self,tests):
        black_list=  ["id","section_id", "milestone_id", "refs","suite_id","estimate_forecast"]
        for i in range(0,len(tests)):
            for k in tests[i].keys():
                if k in black_list:
                    del tests[i][k] 
        return tests        
    ''' 
    Method that gets all suites in the testrail DB for a particulare suitename
    Returns
    All suites found in the testrail DB for all projects
    '''
    def getAllSuites(self):
        suites = []
        projects = self.client.send_get('get_projects')
        for i in range(0,len(projects)):
            if projects[i]['id'] == self.masterID:
                continue
            sts = self.client.send_get('get_suites/' + str(projects[i]['id']))
            for s in sts:
                if s['name'] == self.suiteName:
                    s['project_id'] = projects[i]['id']
                    s['project_name'] = projects[i]['name']
                    suites.append(s)
        return suites
    '''
    Method that looks up a section id based on a title, the project and suite id.
    Parameters
    suite: dictionary object that describes the suite to look in
    secName : the name of the section to extract the ID for
    Returns:
    the ID if found, None otherwise
    '''
    def getSection(self,suite,secName):
        sections = self.client.send_get('get_sections/' + str(suite['project_id']) + "&suite_id=" + str(suite['id']))
        for i in range(0,len(sections)):
            if sections[i]['name'] == secName:
                return sections[i]
        return None
    '''
    Method that adds sections with tests to update in the suites for the projects
    The method add sections with tests to member self.suites
    '''
    def addAllSections(self):
        for i in range(0,len(self.suites)):
            self.suites[i]['sections'] = []
            for s in self.sections.keys():
                tmp = self.getSection(self.suites[i], self.sections[s])
                if tmp != None:
                    if 'sections' not in self.suites[i].keys():
                        self.suites[i]['sections'] = []
                    tests = self.client.send_get('get_cases/' + str(self.suites[i]['project_id']) + 
                                                 '&suite_id=' + str(self.suites[i]['id']) + 
                                                 '&section_id=' + str(tmp['id']))
                    if len(tests) > 0 :
                        tmp['src_id'] = s
                        tmp['tests'] = tests
                        self.suites[i]['sections'].append(tmp)
    '''
    Method to get suites
    '''                    
    def getSuites(self):
        return self.suites
    '''
    Method to get all tests
    '''
    def getTests(self):
        return self.tests
  
    '''
    Method to update all tests in a section.
    Missing tests in the source are not flagged.
    Mismatch in categories is flagged
    '''
    def updateAllTests(self):
        for i in range(0,len(self.suites)):
            for s in range(0,len(self.suites[i]['sections'])):
                for t in range(0,len(self.suites[i]['sections'][s]['tests'])):
                    self.updateTest(self.suites[i]['sections'][s]['tests'][t],self.suites[i]['sections'][s]['src_id'])       
    '''
    Method to update individual test.
    The method looks for the test based on the title - if found it checks the type
    and runs an update
    '''
    def updateTest(self,test,src_id):
        for i in range(0,len(self.tests)):
            for ts in range(0,len(self.tests[i]['tests'])):
                if src_id == self.tests[i]['section_id'] and test['title'] == self.tests[i]['tests'][ts]['title']:         
                    self.client.send_post('update_case/' + str(test['id']),self.tests[i]['tests'][ts])                  