import json
import logging
'''
Created on Apr 4, 2016

@author: petterwildhagen
'''
#from distutils.sysconfig

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
Function to get the ID from all projects or suites in Testrail
Parameters:
project: a JSON object of all projects or suites
name: the name of the project to get the ID for
Returns:
The project/suite id of the project/suite with parameter name. If the project/suite is not found 0 is returned.
'''
def getID(project,name):
    myid = 0
    for p in project:
        if p['name'] == name:
            myid = p['id']
    return myid
'''
Function to compare sections of two suites.
The comparison is done by comparing titles and descriptions and parent child relations ships as well
as depth.
Parameters:
srcSections: the source of comparison
tarSections: the target of comparison
Returns:
None
Throws:
testrailError if structures have different length, if name or description or depth do not match
or if parent child relation ships do not match
'''
def compareSections(srcSections,tarSections):
    logger.info("Called compareSections")
    if srcSections.__len__() != tarSections.__len__():
        raise testrailError("Section count mismatch in source and target: " + str(srcSections.__len__()) +' != ' + str(tarSections.__len__()))
    errorText = ''
    errorFound = False
    refDict = {}
    for src,tar in zip(srcSections,tarSections):
        if src['name'] != tar['name']:
            eT = src['name'] + ' != ' + tar['name']
            errorText = errorText + eT
            errorFound = True
        if src['description'] != tar['description']:
            eT = src['description'] + ' != ' +tar['description']
            errorText = errorText + eT
            errorFound = True
        if src['depth'] != tar['depth']:
            eT = str(src['depth']) + ' != ' + str(tar['depth'])
            errorText = errorText + eT
            errorFound = True
        if src['id'] != None and tar['id'] != None:
            refDict[src['id']] = tar['id']
    for src,tar in zip(srcSections,tarSections):
        if src['parent_id'] != None and tar['parent_id'] != None:
            if refDict[src['parent_id']] != tar['parent_id']:
                errorText = errorText + "Parent reference error: " + str(refDict[src['parent_id']]) + ' != ' + str(tar(['parent_id']))
                errorFound = True
    if errorFound:
        raise testrailError(errorText)   
    logger.info('Sections match')
'''
Function to populate custom field testkey in master project with test id.
This function is hardcoded to only do this population on the master project with
project_id = 11
Parameters:
None
Returns:
Nothing
'''   
def populateTestkey(client):
    logger.info('Starting populateTestkey in project 11')
    suites = client.send_get('get_suites/11')
    counter = 0
    for s in suites:
        cases = client.send_get('get_cases/11/&suite_id=' + str(s['id']))
        for c in cases:
            if c['custom_testkey'] == None or (str(c['custom_testkey']) != 'C' + str(c['id'])):
                uri = 'update_case/' + str(c['id'])
                request = {}
                request['custom_testkey'] = 'C' + str(c['id'])
                #json_request = json.dumps(request)
                result = client.send_post(uri,request)
                logger.info("Updating master test custom_testkey " + str(c['id']) + ' ' + str(result))
                counter = counter +1
    logger.info('Updated ' + str(counter) + ' custom_testkey entries')

'''
Function to check that tests in two projects match. Comparison is done per suite.
Parameters:
client: an instance of Testrail APIClient class to connect to Testrails database
project: the name of the project to run the comparison for
srcID: the project ID of the source to run the comparison for
Returns:
Nothing
'''
def checkTests(client,project,srcID):
    logger.info('Called checkTests for project ' + project )
    projects = client.send_get('get_projects')
    tarProjectID = getID(projects,project)
    tarSuites = client.send_get('get_suites/' + str(tarProjectID))
    srcSuites = client.send_get('get_suites/' + str(srcID))
    for s in srcSuites:
        srcInTarget = False
        for t in tarSuites:
            if s['name'] == t['name']:
                srcInTarget = True
                sSec = client.send_get('get_sections/' + str(srcID) + '&suite_id=' + str(s['id']))
                tSec = client.send_get('get_sections/' + str(tarProjectID) + '&suite_id=' + str(t['id']))
                logger.info('Comparing sections for suite ' + s['name'])    
                try:
                    compareSections(sSec,tSec)
                except testrailError as e:
                    logger.error("Fatal error " + e.value )
                try:
                    logger.info('Comparing tests in suite ' + s['name'])
                    tarTests = client.send_get('get_cases/' + str(tarProjectID) + '/&suite_id=' + str(t['id']))
                    srcTests = client.send_get('get_cases/' + str(srcID) + '/&suite_id=' + str(s['id']))
                    compareTests(srcTests,tarTests)
                except testrailError as e:
                    logger.error("Fatal error " + e.value )
        if not srcInTarget:
            logger.warning('Suite ' + s['name']+ ' not found in project ' + project)
        
'''
Function to compare tests in a particular suite. The comparison is done using 
custom field custom_testkey
'''                
def compareTests(srcTests,tarTests):
    if srcTests.__len__() > tarTests.__len__(): 
        logger.warning("Warning: Tests from master missing in target suite: " + str(srcTests.__len__()) + ' > ' + str(tarTests.__len__())) 
        #print "Warning: Tests from master missing in target suite: " + str(srcTests.__len__()) + ' > ' + str(tarTests.__len__())
    if tarTests.__len__() > srcTests.__len__():
        logger.warning("Warning: Target suite has more tests that master suite: " + str(tarTests.__len__()) + ' > '+ str(srcTests.__len__()))
        #print "Warning: Target suite has more tests that master suite: " + str(tarTests.__len__()) + ' > '+ str(srcTests.__len__())
    for s in srcTests:
        tarInSrc = False
        for t in tarTests:
            if t['custom_testkey'] == s['custom_testkey']:
                compareTest(s,t)
                tarInSrc = True
        if not tarInSrc:
            logger.warning('Warning: Test ' + str(s['id']) + ' ' + str(s['title']) + " not found in target suite")
    logger.info("Test comparison done")
'''
Function to compare two individual tests
Parameter
srcTest: The source of comparison
tarTest: The target for comparison
Returns:
Nothing
'''
def compareTest(srcTest,tarTest):
    
    if srcTest['title'] != tarTest['title']:
        logger.warning("Testname not equal: " + tarTest['title'] + ',' + srcTest['title'])
    for sk in srcTest.keys():
        skFound = True
        if "custom" in sk:
            skFound = False
        for tk in tarTest.keys():
            if "custom" in tk:
                if sk == tk:
                    skFound = True
                    if srcTest[sk] != tarTest[tk]:
                        logger.warning("Warning: " + str(srcTest[sk]) + '\n DOES NOT MATCH\n ' + str(tarTest[tk]))
        if not skFound:
            logger.warning("Warning: key " + sk + " not found in target object")
             