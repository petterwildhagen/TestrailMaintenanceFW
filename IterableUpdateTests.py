'''
Created on May 13, 2016

Class to provide a list if tests to be updated.
Data input to members suites and tests are obtained
from class TestsAndSuitesToUpdate

@author: petterwildhagen
'''

class IterableUpdateTests():
    def __init__(self,suites,tests):
        self.suites = suites
        self.tests = tests    
    '''
    Method to find if a test in a suite has a test in member tests by comparing titles and section source id's
    Returns:
    A dictionary with one element id that is the ID of the test to update and test which is the source to update from
    '''
    def find_test(self,test,src_id):
        for i in range(0,len(self.tests)):
            for ts in range(0,len(self.tests[i]['tests'])):
                if src_id == self.tests[i]['section_id'] and test['title'] == self.tests[i]['tests'][ts]['title']: 
                    el = {'id' : test['id'],
                          'test' : self.tests[i]['tests'][ts]}
                    return el
        return None        
    '''
    Method to return iterable tests to update
    Returns:
    A list of dictionary elements obtained from method 'find_test'
    '''
    def getIterableTestsToUpdate(self):
        return_value = []
        for i in range(0,len(self.suites)):
            for s in range(0,len(self.suites[i]['sections'])):
                for t in range(0,len(self.suites[i]['sections'][s]['tests'])):
                    el = self.find_test(self.suites[i]['sections'][s]['tests'][t],self.suites[i]['sections'][s]['src_id'])
                    if el != None:
                        el['project_name'] = self.suites[i]['project_name']
                        el['project_id'] = self.suites[i]['project_id']
                        return_value.append(el)
        return return_value      