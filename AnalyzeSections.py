'''
Created on May 18, 2016

@author: petterwildhagen
'''
'''
Class to display differences in sections in a QWidget
'''
class AnalyzeSections(QWidget):
    '''
    init method.
    Parameters:
    inp - the diff tree to display
    name - name of the project
    '''
    def __init__(self,inp,name):
        QWidget.__init__(self)
        self.layout = QtGui.QVBoxLayout(self)
        self.DiffTree = inp
        self.pname = name
        self.initUI()
    '''
    method to display section differences in the widget
    '''
    def initUI(self):
        self.setWindowTitle(self.pname + " - " + self.DiffTree['name'])
        # display differences in sections
        la = QtGui.QLabel("Sections in suite " + self.DiffTree['name'])
        hbox = QtGui.QHBoxLayout()          
        hbox.addWidget(la)
        self.layout.addLayout(hbox)
  
        diff = self.DiffTree['diffStr']
        for i in range(0,len(diff)):
            hbox = QtGui.QHBoxLayout()
            l = QtGui.QLabel(str(diff[i]))
            hbox.addWidget(l)
            self.layout.addLayout(hbox)
            
        ebox = QtGui.QHBoxLayout()
        button = QtGui.QPushButton('Quit')
        button.clicked.connect(self.quit)
        ebox.addStretch(1)   
        ebox.addWidget(button)
        self.layout.addLayout(ebox)

    def quit(self):
        print "Quitting!"
        self.close()