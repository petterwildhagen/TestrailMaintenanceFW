'''
Created on Mar 29, 2016

@author: petterwildhagen
'''
from testrail import *
#from testrail_lib import *
from DiffSectionTree import *
from DiffTestTrees import *
#from testrailKeyMigration import migrateTestsInProject
import logging

from DiffTestrailProjects import *
from TestSectionTree import *
client = APIClient('https://getipn.testrail.net/')
client.user = 'petter.wildhagen@testify.no'
client.password = 'Passord01'
try:
    projects = client.send_get('get_projects')

except APIError as e:
    print  e

e = DiffSectionTrees(11,13,"SIP VOIP",client)
et = e.getDiffTree()
t = DiffTestTrees(e,11,13,"SIP VOIP",client)
tt = t.getDiffTree()
print tt
a = []
a = getTestDiffFromDiffTree(tt,a)
print a
for i in range(0,len(a)):
    print a[i]
# print tt
# a = []
# a = getTestDiffFromDiffTree(tt,a)
# for i in range(0,len(a)):
#     print a[i]
# b = PresentTestDifferences(tt)
# bt = b.getChangedTests()
# mt = b.getMissingTests()
# mot = b.getMovedTests()
# print str(bt)
# for c in mt:
#     print c['title']
   # print c['change']['diffCode']
#diff = compareSuites(11, 10, client)
#print diff
#for i in range(0,len(diff)):
#    print diff[i]
#    if 'diffStr' in diff[i].keys():
#        print diff[i]['diffStr']
#printDiffTree(diff)
#inp = client.send_get('get_sections/11&suite_id=46')
#tests = client.send_get('get_cases/11&suite_id=40')
#inputP = client.send_get('get_sections/4&suite_id=21')
#testsP = client.send_get('get_cases/4&suite_id=31')
#ms = sections_JSONflat2tree(inp,'WiFi')
#mt = tests_JSONflat2tree(ms, tests)
#ps = sections_JSONflat2tree(inputP, 'WiFi')

#pt = tests_JSONflat2tree(ps, testsP)
#ttr = createSuiteDiffTree(11, 4, "WiFi", client)
#print ttr
#dtr = createTestDiffTree(mt,pt,ttr)

#printDiffTree(dtr)

    


