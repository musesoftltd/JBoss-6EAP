'''
Created on 11 Oct 2016

@author: ...
'''
from library.jboss.jbossLibrary import setParameterValue, getParameterValue
from library.util import mkdir_p, stripQuotes, appendToFile
import datetime
import os

# list of audit objects.
global auditObjectAtoms 
auditObjectAtoms = []
global auditObjectMolecules
auditObjectMolecules = []


class ReportingObject:
        
    datetimeSuffix = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H.%M.%S')
    
    auditFileName = ''
    reportFileName = ''
    auditFileName =  ''
    reportFileName = ''
    strEnvironment = ''
    strTechnologyType = ''
    
    # Globals
    currentAuditReportServer = ""
    
    currentAuditReportEnvironment = ""
    
    globalReportsStarted = False
    
    auditReportPath = ''
    
    reportFirstRow = ''
    
    def __init__(self):
        auditReportPath = self.getReportDirectory()   
        print "Generating Reports in: " + auditReportPath 
        
    def getReportDirectory(self):
    
        if not self.globalReportsStarted :
            self.globalReportsStarted = True
            
        if len(self.auditReportPath) > 0 :
            return self.auditReportPath         
        
        self.auditReportPath = '../reports/'
        try:                        
          if len(os.environ['WORKSPACE']) > 0 :
              workspaceReportPath = os.environ['WORKSPACE']
              
              self.auditReportPath = workspaceReportPath + '/reports/'
              print "---> Jenkins Environment Workspace Path: " + self.auditReportPath
        except:
            None

        mkdir_p(self.auditReportPath)

        print "Report Path: " + self.auditReportPath
            
        return self.auditReportPath

    def appendToReport(self, strToAppend):
    
        if (self.reportFileName == '') :
            self.reportFilename = self.getReportDirectory() + 'managerial' + '-' + self.strTechnologyType + '-' + self.strEnvironment + '-' + self.datetimeSuffix  + '.csv'
     
        appendToFile(strToAppend, self.reportFilename)
    
    def appendToAudit(self, strToAppend):  
        if (self.auditFileName == '') :
            self.auditFileName = self.getReportDirectory() + 'technical' + '-' + self.strTechnologyType + '-' + self.strEnvironment + '-' + self.datetimeSuffix  + '.csv'
     
        appendToFile(strToAppend, self.auditFileName)

    def auditReport(self, environment, currentServerName):
        print 'auditReport for server : ' + currentServerName + ' in environment : ' + environment + '...'
    
        ############################################################################
        # HEADING of Report...
        ############################################################################
        if (ReportingObject.currentAuditReportEnvironment != environment) :
            self.currentAuditReportEnvironment = environment
    
            self.appendToReport("\nEnv: " + environment + "\n")
    
            self.appendToReport('Server' + ',')
    
            for auditObjectAtom in auditObjectAtoms :
                if not(auditObjectAtom.titledAlready):
                    if (auditObjectAtom.servername == currentServerName) :
                        self.appendToReport(auditObjectAtom.auditTitle + ',')
                        auditObjectAtom.titledAlready = True
    
            for auditObjectMolecule in auditObjectMolecules:
                if not(auditObjectMolecule.titledAlready):
                    if (auditObjectMolecule.servername == currentServerName) :
                        self.appendToReport('\"' + auditObjectMolecule.auditTitle + '\"' + ',')
                        auditObjectMolecule.titledAlready = True
    
                    # only update the environemnt has changed on successful reporting of something
                    # from at leaat one server.
    
            self.appendToReport('\n')
    
        ############################################################################
    
        ############################################################################
        # Data ROW of Report...
        ############################################################################
        self.appendToReport(currentServerName + ',')
    
        for auditObjectAtom in auditObjectAtoms:
            if not(auditObjectAtom.reportedAlready):
                if (auditObjectAtom.servername == currentServerName):
                    auditObjectAtom.renderIntoReport()
                    auditObjectAtom.reportedAlready = True;
    
        for auditObjectMolecule in auditObjectMolecules:
            if not(auditObjectMolecule.reportedAlready):
                if (auditObjectMolecule.servername == currentServerName):
                    auditObjectMolecule.renderIntoReport()
                    auditObjectMolecule.reportedAlready = True;
    
        self.appendToReport('\n')
     
        self.currentAuditReportServer = currentServerName
        self.currentAuditReportEnvironment = environment
     
        print 'auditReport for server : ' + currentServerName + ' in environment : ' + environment + '...end.'

    def reportInitReport(self, environment, technologyType):   
        self.strEnvironment = environment
        self.strTechnologyType = technologyType
        
        print 'init Reporting for Technology Type : ' + self.strTechnologyType + ' in Environment : ' + self.strEnvironment + '.'        

        self.appendToAudit('Server, Test Result, Test' + '\n')
            
        self.appendToReport('Muse,https://sourceforge.net/projects/museproject/ ' + '\n')
        self.appendToReport('Middleware Audit' + '\n')
            
    def auditWriteAudit(self, server, auditText, bAuditPassed):
        passFailRecord = ""
    
        if (bAuditPassed == True):
            passFailRecord = 'Pass'
        else :
            passFailRecord = 'Fail *'
    
        self.appendToAudit(server + ',' + passFailRecord + ',' + auditText + '\n')


reportingObject = ReportingObject()

# enables the user to group atoms together as one
class auditObjectMolecule:
    auditTitle = ""
    servername = ''
    auditObjectAtoms = []
    allPassed = True # Assume true and try to disprove
    somePassed = False

    allMustPass = True
    auditResult = ""

    titledAlready = False
    reportedAlready = False

    def __init__(self, auditTitle, servername, bAllMustPass):
        self.auditObjectAtoms = []
        self.allPassed = True # Assume true and try to disprove
        self.auditTitle = auditTitle
        self.servername = servername
        self.allMustPass = bAllMustPass

        # register with the list of molecules
        auditObjectMolecules.append(self)

    def renderIntoReport(self):
        if not(self.reportedAlready) :
            for auditObjectAtom in self.auditObjectAtoms:
                if (auditObjectAtom.auditPassed == False):
                    self.allPassed = False
                else:
                    self.somePassed = True

            if (self.somePassed == False) :
                self.allPassed = False

            if (self.allPassed):
                print 'On Server: ' + self.servername + ' AuditMolecule : ' + self.auditTitle + ' PASSED'
                reportingObject.appendToReport('...' + ',')
            elif ( (self.somePassed) & (self.allMustPass == False)) :
                reportingObject.appendToReport('...' + ',')
            elif (self.auditResult != ""):
                reportingObject.appendToReport(self.auditResult + ',')
            else:
                print 'On Server: ' + self.servername + ' AuditMolecule : ' + self.auditTitle + ' FAILED'
                reportingObject.appendToReport('ToDo' + ',')

        self.reportedAlready = True

# OO based auditing atom - automatically reported on
class auditObjectAtom():
    servername = ""
    username = ""
    password = ""
 
    auditTitle = ""

    cliVector = ""
    cliProperty = ""
 
    currentValue = ""
    targetValue = ""

    auditPassed = False
    auditResult = ""

    titledAlready = False
    reportedAlready = False

    def __init__(self, servername, username, password, auditTitle, cliVector, cliProperty, targetValue, bApplyTargetValue):
        self.servername = servername
        self.username = username
        self.password = password
        self.auditTitle = auditTitle
        self.cliVector = cliVector
        self.cliProperty = cliProperty
        self.targetValue = str(targetValue)

        self.auditPassed = False

        self.returnResult = self.audit()
        if ((self.auditPassed == False) & (bApplyTargetValue)):
            self.applyTargetValue()
            self.audit()

    def auditWriteAudit(self):
        targetValue = ""
        currentValue = ""

        if (self.auditPassed == True):
            passFailRecord = 'Pass'
        else :
            passFailRecord = 'Fail *'

        if (self.targetValue == "") :
            targetValue = "NotSpecified"
        else :
            targetValue = self.targetValue

        if (self.currentValue == "") :
            currentValue = "Unknown"
        else :
            currentValue = self.currentValue

        reportingObject.appendToAudit('Env:' + ReportingObject.strEnvironment + ' : ' + self.servername + ',' + passFailRecord + ',' + self.auditTitle + ',current:"' + currentValue + '",target:"' + targetValue + '"\n')

    def applyTargetValue(self):
        print 'On Server: ' + self.servername + ' Applying : ' + self.auditTitle + '...'
        result = setParameterValue(self.servername, self.username, self.password, self.cliVector, self.cliProperty, self.targetValue)
        if (result == True) :
            self.auditPassed = result
        else:
            self.auditPassed = False
            self.auditResult = "Unknown"
            print 'Setting value: ' + self.targetValue + ' ' + self.auditTitle + ' for server: ' + self.servername + '...FAILED'

        print 'On Server: ' + self.servername + ' Applying : ' + self.auditTitle + '...end.'

        return self.auditResult

    def audit(self):
        print 'On Server: ' + self.servername + ' Auditing : ' + self.auditTitle + '...'
        self.currentValue = getParameterValue(self.servername, self.username, self.password, self.cliVector, self.cliProperty)
        self.auditResult = self.currentValue
        print 'Target Value: ' + self.targetValue
        print 'Actual Value: ' + self.currentValue
        # This is a hack because we use \" to set some values
        # But they will come back on read without \", so the compare fails
        # although the values are the same
        if (self.targetValue.isdigit()) :
            if (self.targetValue == self.currentValue):
                print 'Auditing: ' + self.auditTitle + '...Passed.'
                self.auditPassed = True
            else:
                print 'Auditing: ' + self.auditTitle + '...FAILED.'
                self.auditPassed = False
        else :
            if (stripQuotes(self.targetValue) in self.currentValue):
                print 'Auditing: ' + self.auditTitle + '...Passed.'
                self.auditPassed = True
            else:
                print 'Auditing: ' + self.auditTitle + '...FAILED.'
                self.auditPassed = False

        self.auditWriteAudit()

        print 'On Server: ' + self.servername + ' Auditing : ' + self.auditTitle + '...end.'

        print '\n'

    def renderIntoReport(self):
        if not(self.reportedAlready) :
            if (self.auditPassed) :
                reportingObject.appendToReport('...' + ',')
            elif (self.auditResult == 'False') :
                reportingObject.appendToReport(str('ToDo') + ',')
            elif (str(self.auditResult) == 'Unknown') :
                reportingObject.appendToReport("ToDo" + ',')
            else :
                reportingObject.appendToReport('ToDo' + ',')

        self.reportedAlready = True;
        

reportingObject = ReportingObject()
        