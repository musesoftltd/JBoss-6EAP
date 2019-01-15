'''
Created on 11 Oct 2016

@author: ...
'''

import datetime
import os

from library.jboss.jbossLibrary import setParameterValue, getParameterValue, \
    isServerRunning, getBindAddressManagement, getBindAddressPublic, \
    getLoggingCustomHandler, connectSilent, getMessageDrivenBeanStrictMaxPool, \
    getMessagingProvider, getHornetQRedeliveryDelay, \
    getHornetQMaxdeliveryAttempts
from library.pega.pegaLibrary import getJdbcConnectionUrlAllPegaDataSourceSingleServer
from library.util import mkdir_p, stripQuotes, appendToFile


datetimeSuffix = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H.%M.%S')

global auditFileName
global reportFileName
auditFileName =  ''
reportFileName = ''

# Globals
global currentAuditReportServer
currentAuditReportServer = ""

global currentAuditReportEnvironment
currentAuditReportEnvironment = ""

global globalReportsStarted
globalReportsStarted = False

global auditReportPath
auditReportPath = ''

# list of audit objects.
auditObjectAtoms = []
auditObjectMolecules = []

def getReportDirectory():
    global globalReportsStarted
    global auditReportPath

    if not(globalReportsStarted):
        globalReportsStarted = True

        try :
            auditReportPath = os.environ['WORKSPACE']
            print "Jenkins Environment Workspace Path: " + auditReportPath
        except:
            None

        if (auditReportPath == "") :
            auditReportPath = "../reports/"

        mkdir_p(auditReportPath)

    return auditReportPath
 
    print "Generating Reports in: " +  getReportDirectory()
 
def appendToReport(strToAppend):
    global reportFileName
    global strEnvironment
    global strTechnologyType

    if (reportFileName == '') :
        reportFilename = getReportDirectory() + 'managerial' + '-' + strTechnologyType + '-' + strEnvironment + '-' + datetimeSuffix  + '.csv'
 
    appendToFile(strToAppend, reportFilename)

def appendToAudit(strToAppend):
    global auditFileName
    global strEnvironment
    global strTechnologyType

    if (auditFileName == '') :
        auditFileName = getReportDirectory() + 'technical' + '-' + strTechnologyType + '-' + strEnvironment + '-' + datetimeSuffix  + '.csv'
 
    appendToFile(strToAppend, auditFileName)

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
        global strEnvironment
        global strTechnologyType

        if not(self.reportedAlready) :
            for auditObjectAtom in self.auditObjectAtoms:
                if (auditObjectAtom.auditPassed == False):
                    self.allPassed = False
                else:
                    self.somePassed = True

            if (self.somePassed == False) :
                self.allPassed = False

            if (self.allPassed):
                appendToReport('...' + ',')
            elif ( (self.somePassed) & (self.allMustPass == False)) :
                appendToReport('...' + ',')
            elif (self.auditResult != ""):
                appendToReport(self.auditResult + ',')
            else:
                appendToReport('ToDo' + ',')

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

        self.returnResult = self.audit(servername, username, password)
        if ((self.auditPassed == False) & (bApplyTargetValue)):
            self.applyTargetValue()
            self.audit(servername, username, password)

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

        appendToAudit('Env:' + strEnvironment + ' : ' + self.servername + ',' + passFailRecord + ',' + self.auditTitle + ',current:"' + currentValue + '",target:"' + targetValue + '"\n')

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

    def audit(self, servername, username, password):
        print 'On Server: ' + servername + ' Auditing : ' + self.auditTitle + '...'
        self.currentValue = getParameterValue(servername, username, password, self.cliVector, self.cliProperty)
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

        print 'On Server: ' + servername + ' Auditing : ' + self.auditTitle + '...end.'

        print '\n'

    def renderIntoReport(self):
        if not(self.reportedAlready) :
            if (self.auditPassed) :
                appendToReport('...' + ',')
            elif (self.auditResult == 'False') :
                appendToReport(str('ToDo') + ',')
            elif (str(self.auditResult) == 'Unknown') :
                appendToReport("ToDo" + ',')
            else :
                appendToReport('ToDo' + ',')

        self.reportedAlready = True;

def auditInitAudit(environment, technologyType):
    global strEnvironment
    global strTechnologyType

    strEnvironment = environment
    strTechnologyType = technologyType

    appendToAudit('Server, Test Result, Test' + '\n')

    appendToReport('Muse,https://sourceforge.net/projects/museproject/ ' + '\n')
    appendToReport('Middleware Audit' + '\n')

def auditWriteAudit(server, auditText, bAuditPassed):
    passFailRecord = ""

    if (bAuditPassed == True):
        passFailRecord = 'Pass'
    else :
        passFailRecord = 'Fail *'

    appendToAudit(server + ',' + passFailRecord + ',' + auditText + '\n')

def auditReport(environment, currentServerName):
    global currentAuditReportServer
    global currentAuditReportEnvironment
    global reportFirstRow
    global strEnvironment
    global strTechnologyType

    print 'auditReport for server : ' + currentServerName + ' in environment : ' + environment + '...'

    ############################################################################
    # HEADING of Report...
    ############################################################################
    if (currentAuditReportEnvironment != environment) :
        currentAuditReportEnvironment = environment

        appendToReport("\nEnv: " + environment + "\n")

        appendToReport('Server' + ',')

        for auditObjectAtom in auditObjectAtoms :
            if not(auditObjectAtom.titledAlready):
                if (auditObjectAtom.servername == currentServerName) :
                    appendToReport(auditObjectAtom.auditTitle + ',')
                    auditObjectAtom.titledAlready = True

        for auditObjectMolecule in auditObjectMolecules:
            if not(auditObjectMolecule.titledAlready):
                if (auditObjectMolecule.servername == currentServerName) :
                    appendToReport('\"' + auditObjectMolecule.auditTitle + '\"' + ',')
                    auditObjectMolecule.titledAlready = True

                # only update the environemnt has changed on successful reporting of something
                # from at leaat one server.

        appendToReport('\n')

    ############################################################################

    ############################################################################
    # Data ROW of Report...
    ############################################################################
    appendToReport(currentServerName + ',')

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

    appendToReport('\n')
 
    currentAuditReportServer = currentServerName
    currentAuditReportEnvironment = environment
 
    print 'auditReport for server : ' + currentServerName + ' in environment : ' + environment + '...end.'
