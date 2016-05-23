'''
Created on May 23, 2016

@author: petterwildhagen
'''
from testrail import *
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.Qt import *
'''
Class to handle login to Testrail
'''
class Login(QtGui.QDialog):
    ''' 
    Constructor method
    Parameters: None
    '''
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setWindowTitle('Testrail analysis tool - Login')
        self.setGeometry(300, 300, 350, 150)
        self.nameLabel = QtGui.QLabel("Username:")
        self.textName = QtGui.QLineEdit(self)
        self.passwdLabel = QtGui.QLabel("Password:")
        self.textPass = QtGui.QLineEdit(self)
        self.textPass.setEchoMode(QtGui.QLineEdit.Password)
        self.buttonLogin = QtGui.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.textName)
        layout.addWidget(self.passwdLabel)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)
    
    '''
    Method to handle login to Testrail. 
    The method sets private members user and password
    Parameters:
    None
    '''
    def handleLogin(self):
        try:
            client = APIClient('https://getipn.testrail.net/')
            client.user = self.textName.text()
            client.password = self.textPass.text()
            client.send_get('get_projects')
            self.username = self.textName.text()
            self.password = self.textPass.text()
            self.accept()
        except APIError as e:
            QtGui.QMessageBox.warning(self, 'Error',str(e))
    '''
    Method to get username
    '''
    def getUsername(self):
        return self.username
    '''
    Method to get password
    '''
    def getPassword(self):
        return self.password
'''
Class to define Testrail API Client login credentials
'''   
class TestrailAPIClient(APIClient):
    def __init__(self,username,password,host):
        print 'Instansiating APIClient ' + host + ' ' + username + ' ' + password
        APIClient.__init__(self, host)
        self.user = username
        self.password = password