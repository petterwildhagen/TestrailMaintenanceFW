import json

import logging
'''
Created on Apr 4, 2016

@author: petterwildhagen
'''

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
