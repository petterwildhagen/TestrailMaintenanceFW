'''
Created on Apr 7, 2016

@author: petterwildhagen
'''
from testrail_lib import logger
from testrail_lib import getID
'''
Function to migrate tests in a project by adding custom_testkey to them.
This function retrieves all the sections from the target project,
extracts all the tests from them and runs the migration for the tests
per suite.
The function compares tests based on title and all other custom attributes and
adds custom_testkey from master project if there is a match
Parameters:
client: instance of APIClient in Testrail to connect to Testrail
project: name of project to be migrated
'''
def migrateTestsInProject(client,project):
    projects = client.send_get('get_projects')
    tarID = getID(projects,project)  
    suites = client.send_get('get_suites/' + str(tarID))
    srcSuites = client.send_get('get_suites/11')
    for s in suites:
        foundS = False
        for srcS in srcSuites:
            if s['name'] == srcS['name']:
                logger.info('found suite ' + s['name'])
                foundS = True
                tarTests = client.send_get('get_cases/' + str(tarID) + '/&suite_id=' + str(s['id']))
                srcTests = client.send_get('get_cases/11/&suite_id=' + str(srcS['id']))
                migrateTests(client,tarTests,srcTests)
        if not foundS:
            logger.info('Suite ' + s['name'] + ' not found')
'''
Function to migrate a set of tests from a single suite by populating 
custom_testkey from the source to a target
Parameters:
client: instance of APIClient in Testrail to connect to Testrail
tarTests: the target (tests to be populated
srcTests: the source, where the custome_testkey is retrieved from
Returns:
Nothing
'''
def migrateTests(client,tarTests,srcTests):
    for tar in tarTests:
        foundTest = False
        matchCnt = True
        custom_testkey =''
        for src in srcTests:
            if tar['title'] == src['title']:
                foundTest = True
                for tk in tar.keys():
                    foundKey = False
                    if 'custom' not in tk:
                        foundKey = True
                    for sk in src.keys():
                        if 'custom' in sk and 'custom' in tk:
                            if sk == tk:
                                foundKey = True
                                if tar[tk] != src[sk] and sk != "custom_testkey":
                                    matchCnt = False
                                    logger.warning('matching keys ' + sk + ' but non matching content ' + str(tar[tk]) + '\nNOT EQUAL TO\n' + str(src[sk]))
                    if not foundKey:
                        logger.warning('Key ' + tk + ' not found')
                    else:
                        custom_testkey = 'C' + str(src['id'])
        if not foundTest:
            logger.warning('Test ' + tar['title'] + ' not found')    
        if matchCnt and foundTest and custom_testkey != '':
            logger.debug('Test ' + tar['title'] + ' ready for migration to ' + custom_testkey)  
            uri = 'update_case/' + str(tar['id'])
            request = {}
            request['custom_testkey'] = custom_testkey
            result = client.send_post(uri,request)
            logger.info('Updating test ' + str(tar['id']) + ' custom_testkey ' + custom_testkey + ' ' + str(result))
        
            
