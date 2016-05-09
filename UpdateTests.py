'''
Created on May 6, 2016

Class to update all tests in a list of sections.

@author: petterwildhagen
'''

class UpdateTests():
    '''
    init method: extracts all projects in test rail, checks if these projects has the mentioned suite.
    Then - creates a diff tree on 
    '''
    def __init__(self,sections,masterID,suite_name,client):