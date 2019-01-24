'''
@author:
'''

# The 'as' error in the margin is caused by 'as' being a reserved word
# It can be safely ignored
from __builtin__ import None
from java.util import Date
from sre_parse import isdigit
from string import find
import sys
from time import sleep
import traceback

from library.util import regularExpressionSearch, sanitizeJDBCCliVector, \
    extractDatasourceName, extractXADatasourceName, stripQuotes
from org.jboss.as.cli.scriptsupport import CLI

def connectSilent(servername, username, password):
    connected = False
    
    retries = 1
    attempts = 0
    while (attempts <= retries) :
        cli = CLI.newInstance()
        
        attempts += 1  
        try:
            cli.connect(servername, 9999, username, password)

            if (cli.getCommandContext()) :
                if cli.getCommandContext().isDomainMode():
                    cli.cmd("cd /host=master/core-service=platform-mbean/type=runtime")
                else:
                    cli.cmd("cd /core-service=platform-mbean/type=runtime")
                
                connected = True
                return cli
        except:
            print 'Connecting to Server: ' + servername + ' FAILED.'
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "*** print_tb:"
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print "*** print_exception:"
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
            print "*** format_exc, first and last line:"
            formatted_lines = traceback.format_exc().splitlines()
            print formatted_lines[0]
            print formatted_lines[-1] 
            
        if not(connected) : 
            cli = None
            sleep(0.2)
    
        return None

def connect(servername, username, password):
    cli = None
    
    print 'Connecting to server : ' + servername + '...'
    cli = connectSilent(servername, username, password)    
    print 'Connecting to server : ' + servername + '...end.'
    
    return cli

def restartServerConnected(cliConnected):    
    print 'Restarting server...'
    
    try:        
        result = cliConnected.cmd("/:shutdown(restart=true)")
        if result.success == True:
            print 'Server was restarted'
    except:
        print 'Restarting server: FAILED: '

    print 'Restarting server...end.'

def suspendServerConnected(cliConnected):    
    print 'Suspending server...'
    
    try:        
        result = cliConnected.cmd("/:suspend")
        if result.success == True:
            print 'Server was Suspended'
    except:
        print 'Suspending server: FAILED: '

    print 'Suspending server...end.'
    
def resumeServerConnected(cliConnected):    
    print 'Resuming server...'
    
    try:        
        result = cliConnected.cmd("/:resume")
        if result.success == True:
            print 'Server was Resumed'
    except:
        print 'Resuming server: FAILED: '

    print 'Resuming server...end.'    

def restartServer(servername, username, password):    
    print 'Restarting server: ' + servername + '...'
        
    try:        
        cli = connectSilent(servername, username, password)

        restartServerConnected(cli)
        
    except:
        print 'Restarting server: ' + servername + ' FAILED: '
#     finally:
#         cli.disconnect()

    print 'Restarting server: ' + servername + '...end.'

def reloadServerConnected(cliConnected):
    print 'Reloading server...'
    
    try:        
        result = cliConnected.cmd("/:reload(admin-only=false,use-current-server-config=true)")
        if result.success == True:
            print 'Server was Reloaded'
        
    except Exception:
        print 'Reloading server FAILED: '
        print Exception   
    except:        
        print 'Reloading server FAILED: '

    print 'Reloading server...end.'

def reloadServer(servername, username, password): 
    print 'Reloading server: ' + servername + '...'
    
    try:        
        cli = connectSilent(servername, username, password)

        result = cli.cmd("/:reload(admin-only=false,use-current-server-config=true)")
        if result.success == True:
            print 'Server was Reloaded'
        
    except Exception:
        print 'Reloading server: ' + servername + ' FAILED: '
        print Exception   
    except :        
        print 'Reloading server: ' + servername + ' FAILED: '
    finally:
        if result.success == True:
            cli.disconnect()

    print 'Reloading server: ' + servername + '...end.'

def isServerRunning(servername, username, password):
    print 'isServerRunning() ' + servername + '...' 
    
    serverstate = ""
    returnResult = False
    
    cliConnected = connectSilent(servername, username, password)
    
    if (cliConnected != None) :
        result = cliConnected.cmd("/:read-attribute(name=server-state)")
        if (result.success) : 
            response = result.getResponse() 
            serverstate = response.get("result").asString()
            print 'Server: ' + servername + 'is Running.'
            print "Current server state: " + serverstate
            
            nonUnicodeServerState = str(serverstate)
            if (nonUnicodeServerState == "running"):
                print 'isServerRunning()... YES'
                returnResult = True            
    else :
        print 'isServerRunning()... NO'
        returnResult = False
        
    if (cliConnected != None) : cliConnected.disconnect()
                           
    print 'isServerRunning() ' + servername + '...end.'
    
    return returnResult 

def isServerRestartRequired(servername, username, password):
    returnResult = False
    
    print 'isServerRestartRequired() ' + servername + '...' 

    serverstate = ""
    
    cliConnected = connectSilent(servername, username, password)
    if (cliConnected != None) :
        result = cliConnected.cmd(":read-attribute(name=server-state)")
        if (result.success) : 
            response = result.getResponse() 
            serverstate = response.get("result").asString()
            print "Current server state: " + serverstate
            nonUnicodeServerState = str(serverstate)
            if (nonUnicodeServerState == "restart-required"):
                returnResult = True
        else :
            returnResult = False
    else :
        returnResult = False

    if (cliConnected != None) : cliConnected.disconnect()
    
    print 'isServerRestartRequired() ' + servername + '...end.'
    
    return returnResult 
           
def isServerReloadRequired(servername, username, password):
    returnResult = False
    
    print 'isServerReloadRequired() ' + servername + '...' 

    serverstate = ""
    
    cliConnected = connectSilent(servername, username, password)
    if (cliConnected != None) :
        result = cliConnected.cmd("/:read-attribute(name=server-state)")
        if (result.success) : 
            response = result.getResponse() 
            serverstate = response.get("result").asString()
            print "Current server state: " + serverstate
            nonUnicodeServerState = str(serverstate)
            if (nonUnicodeServerState == "reload-required"):
                print 'isServerReloadRequired() ' + servername + '...RELOAD REQUIRED' 
                returnResult = True
        else :
            returnResult = True
    else :
        returnResult = False

    if (cliConnected != None) : cliConnected.disconnect()
    
    print 'isServerReloadRequired() ' + servername + '...end.'
    
    return returnResult 
           
def restartServerThenWait(servername, username, password, timeoutMinutes=5):        
    print 'Restarting server: ' + servername + '...'
        
    try:        
        cli = connectSilent(servername, username, password)
        restartServerConnected(cli)
        
    except:
        print 'Restarting server: ' + servername + ' FAILED: '
    finally:
        if (cli != None) : cli.disconnect()

    print 'Restarting server: ' + servername + '...end.'
    
    print 'Waiting for server ready...' + servername + '...'
    # loop 4 times 15 sec x 10 is 10 minutes
    loopRange = 4 * timeoutMinutes;
    for n in range(0, loopRange) :
        try:
            result = isServerRunning(servername, username, password)
            if (result == True) :
                break
            else :
                sleep(15)
        except:
            continue
                    
        if n == loopRange:
            print 'Waiting for server TIMEOUT !!!'
    
    print 'Waiting for server ready...' + servername + '...end.'

def reloadServerThenWait(servername, username, password):    
    try:       
        cliConnected = connectSilent(servername, username, password)              
        reloadServerConnected(cliConnected)
        cliConnected.disconnect()
    
        print 'Waiting for server readiness... on server: ' + servername + '...'
        # loop loopRange times at sleep secs(30) is 5 minutes
        loopRange = 60;
        for n in range(0, loopRange) :
            try:
                result = isServerRunning(servername, username, password)
                if (result == True) :
                    break
            except:
                continue
                        
            if n == loopRange:
                print 'Waiting for server has hit the TIMEOUT !!!'
            
            sleep(10)
    except:
        print "Waiting for server readiness...FAILED"
    
    print 'Waiting for server readiness... on server: ' + servername + '...end.'
    
def stopServer(serverName, username, password):

    connected = False;
    
    print 'Stopping server: ' + serverName + '...'
    
    try:        
        cliConnected = connectSilent(serverName, username, password)
        if (cliConnected): connected = True;
        
        stopServerConnected(cliConnected)
        
    except Exception, e:
        print 'Stopping server: ' + serverName + ' failed: '
        print e   
    except:        
        print 'Stopping server: ' + serverName + ' failed: '

    finally:
        if (connected): cliConnected.disconnect()

    print 'Stopping server: ' + serverName + '...end.'

def stopServerConnected(cliConnected):

    connected = False;
    
    print 'Stopping server...'
    
    try:        
        result = cliConnected.cmd("/:shutdown")
        if result.success == True:
            print 'Server was Stopped'
        
    except Exception, e:
        print 'Stopping server failed: '
        print e   
    except:        
        print 'Stopping server failed: '

    finally:
        if (connected): cliConnected.disconnect()

    print 'Stopping server ...end.'

def issueCliCommandConnected(cli, command):
    try :
        print ' issuing cli commmand ->' + command + '<- ...'
        cli.cmd(command)
        cmdResult = True
        print ' issuing cli commmand ->' + command + '<- ...end'
    except :
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print "*** print_exception:"
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
        print "*** format_exc, first and last line:"
        formatted_lines = traceback.format_exc().splitlines()
        print formatted_lines[0]
        print formatted_lines[-1]
        cmdResult = False
    
    return cmdResult

def issueCliCommand(servername, username, password, command):
    cliConnected = connectSilent(servername, username, password)

    cmdResult = None
    
    print 'On Server :' + servername + ' issuing ->' + command + '<- ...' 
    issueCliCommandConnected(cliConnected, command)
    print 'On Server :' + servername + ' issuing ->' + command + '<- ...end.' 
               
    return cmdResult
 
def getParameterValue(servername, username, password, cliVector, cliProperty, reloadServerIfRequired=False):
    retries = 1
    attempts = 0
    
    cliConnected = None
    currentValue = ''
    cliResult = None
    cliCmd = ''

    if (reloadServerIfRequired) :    
        if isServerReloadRequired(servername, username, password):
            reloadServerThenWait(servername, username, password)

    while (attempts <= retries) :
        try:
            attempts += 1
            print ''
            print 'On Server :' + servername + ' retrieving ->' + cliProperty + '<- from CLI Vector ->' + cliVector + '<- ...'
            cliConnected = connectSilent(servername, username, password)
            if (cliConnected != None):
                    dealingWithADatasource = False
                    dealingWithAnXaDatasource = False
                    # check for regular datasource...
                    datasourceName = regularExpressionSearch("/subsystem=datasources/data-source=(.*)", cliVector)
                    xaDatasourceName = regularExpressionSearch("/subsystem=datasources/xa-data-source=(.*)", cliVector)
                                
                    if (datasourceName != '') :
                        # then we are dealing with a datsource.
                        # better stop then start it.
                        dealingWithADatasource = True
    
                        # if the datasource contains '/' we MUST escape it to work... 
                        cliVector = sanitizeJDBCCliVector(cliVector)
                    elif (xaDatasourceName != '') :
                        dealingWithAnXaDatasource = True
    
                        # if the datasource contains '/' we MUST escape it to work... 
                        cliVector = sanitizeJDBCCliVector(cliVector)
                                    
                    cliCmd = str(cliVector) + ':read-attribute(name=' + str(cliProperty) + ')'
                    
                    print 'Issuing Server Command ->' + cliCmd + '<-'
                    
                    cliResult = cliConnected.cmd(cliCmd)
                    
                    if cliResult.success:
                        appliedOk = True
                        response = cliResult.getResponse()
                        currentValue = response.get("result").asString()
                        print 'On Server :' + servername + ' retrieved :' + currentValue
                    else:
                        appliedOk = False
                        print 'Command Issue Failure ->' + cliCmd + '<-'
                        print 'On Server :' + servername + ' retrieving :' + cliProperty + ' from CLI Vector :' + cliVector + ' ...FAILED.'                        
                        print cliResult.getResponse().get("failure-description").asString()
                        print cliResult.getResponse().get("response-headers").asString()
                        currentValue = "Unknown"
                                                               
        except :
            print 'Exception Issuing Server Command ->' + cliCmd + '<- caused an exception. FAILED.'

            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "*** print_tb:"
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print "*** print_exception:"
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
            print "*** format_exc, first and last line:"
            formatted_lines = traceback.format_exc().splitlines()
            print formatted_lines[0]
            print formatted_lines[-1] 
            
        finally:
            if (cliConnected != None) : cliConnected.disconnect()
      
        print 'On Server :' + servername + ' retrieving ->' + cliProperty + '<- from CLI Vector ->' + cliVector + '<- ...end.'
        
        if ((cliConnected != None) and (currentValue != "Unknown") and (currentValue != "")):
            break
        else :
            sleep (0.2)
        
    return currentValue 

def setParameterValue(servername, username, password, cliVector, cliProperty, targetValue, reloadServerIfRequired=False):
    cliConnected = None
    appliedOk = False
    cliCmd = ''
    
    print 'On Server :' + servername + ' applying ->' + cliProperty + '<- from CLI Vector ->' + cliVector + '<- ...'
    try:
        if (reloadServerIfRequired) :    
            if isServerReloadRequired(servername, username, password):
                reloadServerThenWait(servername, username, password)
        
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None):
            dealingWithADatasource = False
            dealingWithAnXaDatasource = False
            # check for regular datasource...
            datasourceName = extractDatasourceName(cliVector)
            xaDatasourceName = extractXADatasourceName(cliVector)
                        
            if (datasourceName != '') :
                # then we are dealing with a datasource.
                # better stop then start it.
                dealingWithADatasource = True
                disableDatasource(servername, username, password, datasourceName)
                # if the datasource contains '/' we MUST escape it to work... 
                cliVector = sanitizeJDBCCliVector(cliVector)
            elif (xaDatasourceName != '') :
                dealingWithAnXaDatasource = True
                disableXaDatasource(servername, username, password, xaDatasourceName)
                # if the datasource contains '/' we MUST escape it to work... 
                cliVector = sanitizeJDBCCliVector(cliVector)
  
            if (targetValue.lower() == "undefined".lower()) :
                # We must undefine a value, we cannot use set...
                cliCmd = str(cliVector) + ':undefine-attribute(name=' + str(cliProperty) + ')'
            else:
                if (isinstance (targetValue, int)) :
                    cliCmd = str(cliVector) + ':write-attribute(name=' + str(cliProperty) + ',value=' + targetValue + ')'
                else :    
                    cliCmd = str(cliVector) + ':write-attribute(name=' + str(cliProperty) + ',value=\"' + stripQuotes(targetValue) + '\")'
           
            print 'Issuing Server Command ->' + cliCmd + '<-'
            
            try :
                cliResult = cliConnected.cmd(cliCmd)
                
                if cliResult.success:
                    appliedOk = True
                    print 'On Server :' + servername + ' applied :' + targetValue
                else:
                    appliedOk = False
                    print 'Command Issue Failure ->' + cliCmd + '<-'
                    print cliResult.getResponse().get("failure-description").asString()
                    print cliResult.getResponse().get("response-headers").asString()
                
            except :
                print 'Exception Issuing Server Command ->' + cliCmd + '<- caused an exception. FAILED.'

                exc_type, exc_value, exc_traceback = sys.exc_info()
                print "*** print_tb:"
                traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                print "*** print_exception:"
                traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
                print "*** format_exc, first and last line:"
                formatted_lines = traceback.format_exc().splitlines()
                print formatted_lines[0]
                print formatted_lines[-1]          
    except:
        appliedOk = False        
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print "*** print_exception:"
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
        print "*** format_exc, first and last line:"
        formatted_lines = traceback.format_exc().splitlines()
        print formatted_lines[0]
        print formatted_lines[-1]
        print 'On Server :' + servername + ' applying ->' + cliProperty + '<- from CLI Vector ->' + cliVector + '<- ...FAILED.'
    finally:
        if (dealingWithADatasource) :
            enableDatasource(servername, username, password, datasourceName)
        elif (dealingWithAnXaDatasource) :
            enableXaDatasource(servername, username, password, xaDatasourceName)

        if (cliConnected != None) : cliConnected.disconnect()
    
    if (reloadServerIfRequired) :    
        if isServerReloadRequired(servername, username, password):
            reloadServerThenWait(servername, username, password)
        
    print 'On Server :' + servername + ' applying ->' + cliProperty + '<- from CLI Vector ->' + cliVector + '<- ...end.'
    return appliedOk 

def setBindAddressesToAllInterfaces(servername, username, password):
    cliConnected = None
        
    print 'setBindAddressesToAllInterfaces() for server: ' + servername + '...'
    
    try:      
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :
            result = cliConnected.cmd("/interface=management/:write-attribute(name=inet-address,value=\"$\{jboss.bind.address.management:0.0.0.0\}\")")
            if result.success:
                print 'The server management interface now binds to all addresses'
            else:
                print 'The server management interface now binds to all addresses - FAILED'
            
            result = cliConnected.cmd("/interface=public/:write-attribute(name=inet-address,value=\"$\{jboss.bind.address:0.0.0.0\}\")")
            if result.success:        
                print 'The server public interface now binds to all addresses'
            else:
                print 'setBindAddressesToAllInterfaces() for server: ' + servername + ' FAILED'
        
    except:      
        print 'setBindAddressesToAllInterfaces() for server: ' + servername + ' FAILED'
    
    finally:
        if (cliConnected != None): cliConnected.disconnect()
              
    print 'setBindAddressesToAllInterfaces() for server: ' + servername + '...end.'

def getBindAddressManagement(servername, username, password):
    print 'getBindAddressManagement() for server: ' + servername + '...'
    returnResult = getParameterValue(servername, username, password, "/interface=management/", "inet-address")
    print 'getBindAddressManagement() for server: ' + servername + '...end.'
    return returnResult

def getBindAddressPublic(servername, username, password):
    print 'getBindAddressPublic() for server: ' + servername + '...'
    returnResult = getParameterValue(servername, username, password, "/interface=public/", "inet-address")
    print 'getBindAddressPublic() for server: ' + servername + '...end.'
    return returnResult

def checkUptime(servername, username, password) :
    cliConnected = None
    
    try:        
        print 'Checking uptime for server: ' + servername + '...'
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :            
            if cliConnected.getCommandContext().isDomainMode():
                cliConnected.cmd("cd /host=master/core-service=platform-mbean/type=runtime")
            else:
                cliConnected.cmd("cd /core-service=platform-mbean/type=runtime")
            result = cliConnected.cmd(":read-attribute(name=start-time)")
            response = result.getResponse()
            startTime = response.get("result").asLong()
            result = cliConnected.cmd(":read-attribute(name=uptime)")
            response = result.getResponse()
            serveruptimeMS = response.get("result").asLong()
            serveruptimeS = (serveruptimeMS / 1000)
            
            uptimeDays = 0
            uptimeHours = 0
            uptimeMinutes = 0
            uptimeSeconds = 0
            if (serveruptimeS): uptimeSeconds = int((serveruptimeS) % 60)
            if (serveruptimeS > (60)): uptimeMinutes = int((serveruptimeS / 60) % (60))
            if (serveruptimeS > (60 * 60)): uptimeHours = int((serveruptimeS / (60 * 60)) % 24)
            if (serveruptimeS > (60 * 60 * 24)): uptimeDays = int((serveruptimeS / (60 * 60 * 24)) % 365)
             
            print 'The server was started on ' + Date(startTime).toString() + '. ' + \
            'The server has been running for ' + \
            str(uptimeDays) + 'd ' + \
            str(uptimeHours) + 'h ' + \
            str(uptimeMinutes) + 'm ' + \
            str(uptimeSeconds) + 's '
    
    except:           
        print 'Checking uptime for server : ' + servername + ' FAILED'
    finally :
        if (cliConnected != None) : cliConnected.disconnect()
        
    print 'Checking uptime for server: ' + servername + '...end.'        
        
def applySecurity(servername, username, password, keyStorePassword, keyStoreAlias, keyStoreFile):
    cliConnected = None

    print 'applySecurity for server: ' + servername + '...'
    
    try:        
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :
            print 'Remove Default HTTP/S Connector(s)...'
#             cliConnected.cmd('/subsystem=web/connector=http/:remove')
            cliConnected.cmd('/subsystem=web/connector=https/:remove')
            print 'Remove Default HTTP/S Connector(s)...end.'
                    
            print 'Removing SSL from management realm...'
            cliConnected.cmd('/core-service=management/security-realm=ManagementRealm/server-identity=ssl/:remove')
            print 'Removing SSL from management realm...end.'
    
            print 'Remove Default Management binding...'
            cliConnected.cmd('/core-service=management/management-interface=http-interface/:remove')
            print 'Remove Default Management binding...end.'
              
            print 'Adding SSL to management realm...'
            cliConnected.cmd('/core-service=management/security-realm=ManagementRealm/server-identity=ssl:add(scheme="https", socket-binding="https", keystore-password=' + keyStorePassword + ', keystore-path=' + keyStoreFile + ', alias=' + keyStoreAlias + ', protocol="TLSv1")')
            print 'Adding SSL to management realm...end.'
    
            print 'Add SSL Default Management binding...'
            cliConnected.cmd('/core-service=management/management-interface=http-interface:add(secure-socket-binding=management-https, security-realm=ManagementRealm)')
            print 'Add SSL Default Management binding...end.'
                    
            print 'Adding SSL Connector...'
            cliConnected.cmd('/subsystem=web/connector=https/:add(name=https, protocol=HTTP/1.1, secure=true, enabled=true, socket-binding=https, scheme=https)')
            print 'Adding SSL Connector...end.'
                    
            print 'Adding SSL Connector Detail...'
            cliConnected.cmd('/subsystem=web/connector=https/configuration=ssl/:add(name=SSLConfig)')
            cliConnected.cmd('/subsystem=web/connector=https/configuration=ssl/:write-attribute(name=name,value=SSLConfig)')
            cliConnected.cmd('/subsystem=web/connector=https/configuration=ssl/:write-attribute(name=certificate-key-file,value=' + keyStoreFile + ')')
            cliConnected.cmd('/subsystem=web/connector=https/configuration=ssl/:write-attribute(name=name,value=SSLConfig)')
            cliConnected.cmd('/subsystem=web/connector=https/configuration=ssl/:write-attribute(name=password,value=' + keyStorePassword + ')')
            cliConnected.cmd('/subsystem=web/connector=https/configuration=ssl/:write-attribute(name=protocol,value=TLSv1.1,TLSv1.2)')
            cliConnected.cmd('/subsystem=web/connector=https/configuration=ssl/:write-attribute(name=key-alias,value=' + keyStoreAlias + ')')
            cliConnected.cmd('/subsystem=web/connector=https/configuration=ssl/:write-attribute(name=cipher-suite,value=ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256")')            
            print 'Adding SSL Connector Detail...end.'      
        
    except:
        print 'Operation for server: ' + servername + '...FAILED'   
    finally:
        if (cliConnected != None) : cliConnected.disconnect()
               
    print 'applySecurity for server: ' + servername + '...end.'
        
def createAccessLog(servername, username, password):
    cliConnected = None
        
    print 'Creating Access Log on: ' + servername + '...'
    try:
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :
            cliConnected.cmd("/subsystem=web/virtual-server=default-host/access-log=configuration:add")
            cliConnected.cmd("/subsystem=web/virtual-server=default-host/access-log=configuration:write-attribute(name=pattern, value=\"%h %l %u %t %r %s %b %{Referer}i %{User-Agent}i %S %T %q cookies %{JSESSIONID}c\"")
            cliConnected.cmd("/subsystem=web/virtual-server=default-host/access-log=configuration:write-attribute(name=prefix, value=\"access_log_\"")
            cliConnected.cmd("/subsystem=web/virtual-server=default-host/configuration=access-log/setting=directory:add")
            cliConnected.cmd("/subsystem=web/virtual-server=default-host/configuration=access-log/setting=directory:write-attribute(name=\"path\",value=\"./\"")
            cliConnected.cmd("/subsystem=web/virtual-server=default-host/configuration=access-log/setting=directory:write-attribute(name=\"relative-to\",value=\"jboss.server.log.dir\"")
    except:
        print 'Creating Access Log on: ' + servername + '...FAILED'
    finally:
        if (cliConnected != None) : cliConnected.disconnect()
    print 'Creating Access Log on: ' + servername + '...end.'
    
def applyCustomLogger(servername, username, password):
    cliConnected = None
    
    print 'Adding Logger for server: ' + servername + '...'
    
    try:        
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :
            
            try:
                result = cliConnected.cmd("/subsystem=logging/custom-handler=FILESIZEDATE:add\
                    (\
                        formatter=\"%d{HH:mm:ss,SSS} %-5p [%c] (%t) %s%E%n\",\
                        name=FILESIZEDATE,\
                        class=org.jboss.logmanager.handlers.PeriodicSizeRotatingFileHandler,\
                        module=org.jboss.logmanager,\
                        level=ALL\
                    )\
                    ")
                if result.success == True:
                    print 'custom-handler=FILESIZEDATE added'
    
    #                  (\"formatter\" => \"%d{HH:mm:ss,SSS} %-5p [%c] (%t) %s%E%n\"),\
    
                result = cliConnected.cmd("/subsystem=logging/custom-handler=FILESIZEDATE/:write-attribute\
                    (\
                        name=properties,value=\
                        [\
                          (\"autoFlush\" => \"true\"),\
                          (\"append\" => \"true\"),\
                          (\"rotateSize\" => \"10000000\"),\
                          (\"maxBackupIndex\" => \"20\"),\
                          (\"suffix\" => \".yyyy-MM-dd\"),\
                          (\"fileName\" => \"${jboss.server.log.dir}/server.log\")\
                        ]\
                    )\
                  ")
                if result.success == True:
                    print 'custom-handler=FILESIZEDATE attibutes set'
        
                result = cliConnected.cmd("/subsystem=logging/root-logger=ROOT/:remove-handler(name=FILE)")
                if result.success == True:
                    print 'ROOT Logger, FILE handler removed'

                result = cliConnected.cmd("/subsystem=logging/root-logger=ROOT/:remove-handler(name=ASYNC)")
                if result.success == True:
                    print 'ASYNC Logger, removed'
                    
                result = cliConnected.cmd("/subsystem=logging/root-logger=ROOT/:add-handler(name=FILESIZEDATE)")
                if result.success == True:
                    print 'ROOT Logger, FILESIZEDATE added'
                    
                result = cliConnected.cmd("/subsystem=logging/console-handler=CONSOLE/:write-attribute(name=level,value=WARN)")
                if result.success == True:
                    print 'Console Logger, level to WARN'

                result = cliConnected.cmd("/subsystem=logging/root-logger=ROOT/:write-attribute(name=level,value=WARN)")
                if result.success == True:
                    print 'ROOT Logger, level to WARN'
                    
            except : 
                print 'Adding Logger for server: ' + servername + ' FAILED: '
    except:
        print 'Adding Logger for server: ' + servername + ' FAILED: '
    finally:
        if (cliConnected != None) : cliConnected.disconnect()

    print 'Adding Logger for server: ' + servername + '...end.'

def queryNameBindings(servername, username, password):
    cliConnected = None
    responseResultList = None
    
    print 'Querying Name Bindings for server: ' + servername + '...'
    
    try:        
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :
            result = cliConnected.cmd("/subsystem=naming/:read-children-names(child-type=binding)")
            response = result.getResponse()
            
            responseResultList = response.get("result").asList()
            responseResultListSize = response.get("result").asInt()
            for index in range(responseResultListSize):
                responseResultListEntry = responseResultList[index].asString()
                print 'Found Name Binding: ' + responseResultListEntry
                  
    except:
        print 'Querying Name Bindings for server: ' + servername + ' FAILED: '
    finally:
        if (cliConnected != None) : cliConnected.disconnect()

    print 'Querying Name Bindings for server: ' + servername + '...end.'
    return responseResultList

def deployToServer(servername, username, password, applicationDeploymentSourceFolder, deploymentArtefact):
    cliConnected = None
    
    print 'Deploying ' + applicationDeploymentSourceFolder + '\\' + deploymentArtefact + '...'
    try:
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :
            result = cliConnected.cmd('deploy "' + applicationDeploymentSourceFolder + '\\' + deploymentArtefact + '"')
            if result.success == False:
                print('Deploying: ' + deploymentArtefact + ' FAILED')
                print 'Result: ' + result.getResponse().asString()
            else :
                print('Deploying: ' + deploymentArtefact)
                print 'Result: ' + result.getResponse().asString()

    except :
        print 'Deploying ' + applicationDeploymentSourceFolder + '\\' + deploymentArtefact + '... FAILED.'
    finally:
        if (cliConnected != None) : cliConnected.disconnect()
        
    print 'Deploying ' + applicationDeploymentSourceFolder + '\\' + deploymentArtefact + '...end.'

def upgradeToServer(servername, username, password, applicationDeploymentSourceFolder, deploymentArtefact):
    cliConnected = None
    
    print 'Upgrading ' + applicationDeploymentSourceFolder + '\\' + deploymentArtefact + '...'

    try:
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :
            result = cliConnected.cmd('undeploy ' + deploymentArtefact + '')
            print(deploymentArtefact + ' upgrade result: ' + result.getResponse().asString())
            if (result.success):
                print('Deploying: ' + deploymentArtefact + '...')
                result = cliConnected.cmd('deploy "' + applicationDeploymentSourceFolder + '\\' + deploymentArtefact + '"')
                if result.success == False:
                    print('Deploying: ' + deploymentArtefact + ' FAILED')
                    print 'Result: ' + result.getResponse().asString()
                else :
                    print('Deploying: ' + deploymentArtefact + '...end.')
                    print 'Result: ' + result.getResponse().asString()
    except :
        print 'Upgrading ' + applicationDeploymentSourceFolder + '\\' + deploymentArtefact + '... FAILED.'
    finally:
        if (cliConnected != None) : cliConnected.disconnect()
        
    print 'Upgrading ' + applicationDeploymentSourceFolder + '\\' + deploymentArtefact + '...end.'

def disableDatasource(servername, username, password, dsName):
    cliConnected = None
    
    print 'Disabling Datasource: ' + dsName + '...'
    try:
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None):
            result = cliConnected.cmd(sanitizeJDBCCliVector('/subsystem=datasources/data-source=' + dsName) + ':disable')
            if result.success == True:
                print dsName + ' was stopped on the server'
            else:
                print 'Disabling: ' + dsName + ' for server FAILED.'
    except :
        print 'Disabling: ' + dsName + ' for server FAILED.'
    finally:
        if (cliConnected != None) : cliConnected.disconnect()
        
    print 'Disabling Datasource: ' + dsName + '...end.'

def disableXaDatasource(servername, username, password, dsName):
    cliConnected = None
    
    print 'Disabling xa Datasource: ' + dsName + '...'
    try:
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None):
            result = cliConnected.cmd(sanitizeJDBCCliVector('/subsystem=datasources/xa-data-source=' + dsName) + ':disable')
            if result.success == True:
                print dsName + ' was stopped on the server'
            else:
                print 'Disabling: ' + dsName + ' for server FAILED.'
    except :
        print 'Disabling: ' + dsName + ' for server FAILED.'
    finally:
        if (cliConnected != None) : cliConnected.disconnect()
        
    print 'Disabling xa Datasource: ' + dsName + '...end.'


def enableDatasource(servername, username, password, dsName):
    cliConnected = None
    
    print 'Enabling datasource:' + dsName + '...'
    try:
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :
            result = cliConnected.cmd(sanitizeJDBCCliVector('/subsystem=datasources/data-source=' + dsName) + ':enable')
            if result.success == True:
                print dsName + ' was started on the server'
            else:
                print 'enabling: ' + dsName + ' for server FAILED: '
                
    except:
        print 'enabling: ' + dsName + ' for server FAILED: '
    finally:
        if (cliConnected != None) : cliConnected.disconnect()
            
    print 'Enabling datasource:' + dsName + '...end.'

def enableXaDatasource(servername, username, password, dsName):
    cliConnected = None
    
    print 'Enabling xa datasource:' + dsName + '...'
    try:
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :
            result = cliConnected.cmd(sanitizeJDBCCliVector('/subsystem=datasources/xa-data-source=' + dsName) + ':enable')
            if result.success == True:
                print dsName + ' was started on the server'
            else:
                print 'enabling: ' + dsName + ' for server FAILED: '
    except:
        print 'enabling: ' + dsName + ' for server FAILED: '
    finally:
        if (cliConnected != None) : cliConnected.disconnect()
            
    print 'Enabling xa datasource:' + dsName + '...end.'

def getAllDataSources(servername, username, password):
    responseResultList = None
    responseResultDSNames = []
    cliConnected = None
    
    print 'Querying Data Sources for server: ' + servername + '...'
    
    try:        
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :
            result = cliConnected.cmd("/subsystem=datasources/:read-children-names(child-type=data-source)")
            response = result.getResponse()
            
            responseResultList = response.get("result").asList()
            responseResultListSize = response.get("result").asInt()
            for index in range(responseResultListSize):
                responseResultListEntry = responseResultList[index].asString()
                responseResultDSNames.append(responseResultListEntry)
                print 'Found Non XA Data Source: ' + responseResultListEntry
                      
    except:
        print 'Querying Data Sources for server: ' + servername + ' FAILED: '
    finally:
        if (cliConnected != None) : cliConnected.disconnect()
        
    print 'Querying Data Sources for server: ' + servername + '...end.'
    
    if (len(responseResultDSNames) > 0) :
        return responseResultDSNames
    else :
        return None
    
def getAllXaDataSources(servername, username, password):
    responseResultList = None
    responseResultDSNames = []
    cliConnected = None
    
    print 'Querying XA Data Sources for server: ' + servername + '...'
    
    try:        
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :
            result = cliConnected.cmd("/subsystem=datasources/:read-children-names(child-type=xa-data-source)")
            response = result.getResponse()
            
            responseResultList = response.get("result").asList()
            responseResultListSize = response.get("result").asInt()
            for index in range(responseResultListSize):
                responseResultListEntry = responseResultList[index].asString()
                responseResultDSNames.append(responseResultListEntry)
                print 'Found XA Data Source: ' + responseResultListEntry
                      
    except:
        print 'Querying XA Data Sources for server: ' + servername + ' FAILED: '
    finally:
        if (cliConnected != None) : cliConnected.disconnect()
        
    print 'Querying XA Data Sources for server: ' + servername + '...end.'
    
    if (len(responseResultDSNames) > 0) :
        return responseResultDSNames
    else :
        return None
    
def getDatasourceConnectionURL(servername, username, password, dsName):
    print 'getDatasourceConnectionURL() for server: ' + servername + '...'
    returnResult = getParameterValue(servername, username, password, "/subsystem=datasources/data-source=" + dsName + "/", "connection-url")
    print 'getDatasourceConnectionURL() for server: ' + servername + '...end.'
    return returnResult

def setDatasourceConnectionURL(servername, username, password, dsName, connectionUrl):            
    cliConnected = None
    
    print 'Set Connection URL...'
    
    print 'disable datasource...'
    disableDatasource(servername, username, password, dsName)
    print 'disable datasource...end.'

    try:
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :
            result = cliConnected.cmd("/subsystem=datasources/data-source=" + dsName + "/:write-attribute(name=connection-url,value=\"" + connectionUrl + "\")")
            if result.success == True:
                print 'Set Connection URL to: ' + connectionUrl     
    except:
        print 'Setting connectionUrl for: ' + dsName + ' FAILED: '    
    finally:
        if (cliConnected != None) :  cliConnected.disconnect()
            
    print 'enable datasource...'
    enableDatasource(servername, username, password, dsName)
    print 'enable datasource...end.'

    print 'Set Connection URL...end.'


def setDatasourceCredentialsSingleDS(servername, username, password, dsName, dbusername, dbPassword):
    cliConnected = None
    
    print "setJdbcCredentialsSingleDS..."
    
    disableDatasource(servername, username, password, dsName)
    
    try:
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :        
            print 'Set username...'
            result = cliConnected.cmd("/subsystem=datasources/data-source=" + dsName + "/:write-attribute(name=user-name,value=\"" + dbusername + "\")")
            if result.success == True:
                print 'JDBC Params were modified on the server'
            print 'Set username...end.'
    
            print 'Set password...'
            result = cliConnected.cmd("/subsystem=datasources/data-source=" + dsName + "/:write-attribute(name=password,value=\"" + dbPassword + "\")")
            if result.success == True:
                print 'JDBC Params were modified on the server'      
            print 'Set password...end.'
    except:
        print 'setJdbcCredentialsSingleDS...FAILED'
    finally:
        if (cliConnected != None) : cliConnected.disconnect()
               
    enableDatasource(servername, username, password, dsName)
    
    print "setJdbcCredentialsSingleDS...end."
                      
def setDatasourceExaDataOptionsSingleNonXADataSource(servername, username, password, dsName):
    cliConnected = None
    
    print 'setJdbcExaDataOptionsSingleXADataSource(): ' + dsName + '...'

    disableDatasource(servername, username, password, dsName)
    
    try:
        cliConnected = connectSilent(servername, username, password)

        if (cliConnected != None):            
            print 'Set check validation...'
            result = cliConnected.cmd('/subsystem=datasources/data-source=' + dsName + '/:write-attribute(name=check-valid-connection-sql,value="select 1 from dual")')    
            if result.success == True:
                print 'JDBC Params were modified on the server'      
            else:
                print 'Setting JDBC Params for: ' + dsName + ' FAILED: '    
            print 'Set check validation...end.'

        if (cliConnected != None):            
            print 'Set validate on match...'
            result = cliConnected.cmd('/subsystem=datasources/data-source=' + dsName + '/:write-attribute(name=validate-on-match,value=false)')
            if result.success == True:
                print 'JDBC Params were modified on the server'
            else:
                print 'Set validate on match: ' + dsName + ' FAILED: '    
            print 'Set validate on match...end.'
    
        if (cliConnected != None):            
            print 'Set background validation...'
            result = cliConnected.cmd('/subsystem=datasources/data-source=' + dsName + '/:write-attribute(name=background-validation,value=false)')
            if result.success == True:
                print 'JDBC Params were modified on the server'      
            else:
                print 'Set background validation: ' + dsName + ' FAILED: '    
            print 'Set background validation...end.'
    
        if (cliConnected != None):            
            print 'Set use-fast-fail...'
            result = cliConnected.cmd('/subsystem=datasources/data-source=' + dsName + '/:write-attribute(name=use-fast-fail,value=false)')
            if result.success == True:
                print 'JDBC Params were modified on the server'
            else:      
                print 'Set use-fast-fail: ' + dsName + ' FAILED: '    
            print 'Set use-fast-fail...end'
    
        if (cliConnected != None):            
            print 'Set exception-sorter...'
            result = cliConnected.cmd('/subsystem=datasources/data-source=' + dsName + '/:write-attribute(name=exception-sorter-class-name,value=org.jboss.jca.adapters.jdbc.extensions.oracle.OracleExceptionSorter)')
            if result.success == True:
                print 'JDBC Params were modified on the server'
            else:
                print 'Set exception-sorter: ' + dsName + ' FAILED: '    
            print 'Set exception-sorter...end'
    except:
        print 'setJdbcExaDataOptionsSingleXADataSource()... FAILED.'
    finally:
        if (cliConnected != None) : cliConnected.disconnect()

    enableDatasource(servername, username, password, dsName)
                                  
    print 'setJdbcExaDataOptionsSingleXADataSource(): ' + dsName + '...end.'

def setStatelessSessionBeanStrictMaxPool(servername, username, password, poolSize):
    print 'Setting StatelessSessionBeanStrictMaxPool...'
    setParameterValue(servername, username, password, "/subsystem=ejb3/strict-max-bean-instance-pool=slsb-strict-max-pool/", "max-pool-size", poolSize)    
    print 'Setting StatelessSessionBeanStrictMaxPool...end.'

def setMessageDrivenBeanStrictMaxPool(servername, username, password, poolSize):
    print 'Setting StatelessSessionBeanStrictMaxPool...'
    setParameterValue(servername, username, password, "/subsystem=ejb3/strict-max-bean-instance-pool=mdb-strict-max-pool/", "max-pool-size", poolSize)    
    print 'Setting StatelessSessionBeanStrictMaxPool...end.'


def getMessageDrivenBeanStrictMaxPool(servername, username, password):
    print 'getMessageDrivenBeanStrictMaxPool() for server: ' + servername + '...'
    returnResult = getParameterValue(servername, username, password, "/subsystem=ejb3/strict-max-bean-instance-pool=mdb-strict-max-pool/", "max-pool-size")
    print 'getMessageDrivenBeanStrictMaxPool() for server: ' + servername + '...end.'
    return returnResult
            
def getHttpConnectorMaxConnections(servername, username, password):
    print 'getHttpConnectorMaxConnections() for server: ' + servername + '...'
    returnResult = getParameterValue(servername, username, password, "/subsystem=web/connector=http/", "max-connections")
    print 'getHttpConnectorMaxConnections() for server: ' + servername + '...end.'
    return returnResult

def getHttpsConnectorMaxConnections(servername, username, password):
    print 'getHttpConnectorMaxConnections() for server: ' + servername + '...'
    returnResult = getParameterValue(servername, username, password, "/subsystem=web/connector=https/", "max-connections")
    print 'getHttpConnectorMaxConnections() for server: ' + servername + '...end.'
    return returnResult
    
def setConnectorMaxConnections(servername, username, password, connectionMax):
    print 'setConnectorMaxConnections...'
    try:
        cliConnected = connectSilent(servername, username, password)
        cliConnected.cmd('/subsystem=web/connector=http/:write-attribute(name=max-connections,value=' + str(connectionMax) + ')')
        cliConnected.cmd('/subsystem=web/connector=https/:write-attribute(name=max-connections,value=' + str(connectionMax) + ')')
    except:
        print 'setConnectorMaxConnections...FAILED.'
    finally:
        if (cliConnected != None) : cliConnected.disconnect()
    print 'setConnectorMaxConnections...end.'
    
def setSocketBindingPort(servername, username, password, socketName, newPort):
    print 'setSocketBindingPort...'
    try:
        cliConnected = connectSilent(servername, username, password)
        cliConnected.cmd('/socket-binding-group=standard-sockets/socket-binding=' + socketName + '/:write-attribute(name=port,value=' + str(newPort) + ')')
    except:
        print 'setSocketBindingPort...FAILED.'
    finally:
        if (cliConnected != None) : cliConnected.disconnect()
    print 'setSocketBindingPort...end.'

def addOnAccessLogging(servername, username, password):
    cliConnected = None
    
    print 'Add OnAccess Logging...' 
    
    try:        
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None):
            cliConnected.cmd('/subsystem=web/virtual-server=default-host/access-log=configuration:add')
            cliConnected.cmd('/subsystem=web/virtual-server=default-host/access-log=configuration:write-attribute(name=pattern, value="%h %l %u %t %r %s %b %{Referer}i %{User-Agent}i %S %T %q cookies %{JSESSIONID}c cookies %{Pega-RULES}c")')
            cliConnected.cmd('/subsystem=web/virtual-server=default-host/access-log=configuration:write-attribute(name=prefix, value="access_log_")')
            cliConnected.cmd('/subsystem=web/virtual-server=default-host/configuration=access-log/setting=directory:add')
            cliConnected.cmd('/subsystem=web/virtual-server=default-host/configuration=access-log/setting=directory:write-attribute(name="path",value="./")')
            cliConnected.cmd('/subsystem=web/virtual-server=default-host/configuration=access-log/setting=directory:write-attribute(name="relative-to",value="jboss.server.log.dir")')    
    except:
        print 'Operation for server: ' + servername + '...FAILED'
    finally:
        if (cliConnected != None) : cliConnected.disconnect()   

    print 'Add OnAccess Logging...end.' 

def switchJMSProviderToActiveMQ(servername, username, password, bTransactional):
    cliConnected = None
    foundExistingResourceAdaptor = False
    
    print 'Switching JMS Provider to ActiveMQ...' 
    
    try:        
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :
            print 'Switch JMS to AMQ...'
            cliConnected.cmd('/subsystem=ejb3/:write-attribute(name=default-resource-adapter-name,value=\"org.apache.activemq.ra\")')
            print 'Switch JMS to AMQ...end.'
    
            result = cliConnected.cmd('/subsystem=resource-adapters/:read-children-names(child-type=resource-adapter)')
            if (result.success) :
                response = result.getResponse()
                responseResultList = response.get("result").asList()
                responseResultListSize = response.get("result").asInt()
                for index in range(responseResultListSize):
                    responseResultListEntry = responseResultList[index].asString()
                    if (responseResultListEntry == 'org.apache.activemq.ra') :
                        print 'Found existing Resource Adapter: ' + responseResultListEntry + '...'
                        foundExistingResourceAdaptor = True
                        break
      
            if (foundExistingResourceAdaptor) :                    
                print 'Remove existing Resource Adapter...'
                cliConnected.cmd('/subsystem=resource-adapters/resource-adapter=org.apache.activemq.ra/:remove')
                print 'Remove existing Resource Adapter...end.'
    
            print 'Add AMQ Resource Adapter module...'
            if (bTransactional) : 
                cliConnected.cmd('/subsystem=resource-adapters/resource-adapter=org.apache.activemq.ra/:add(module=org.apache.activemq,transaction-support=XATransaction)')
            else :
                cliConnected.cmd('/subsystem=resource-adapters/resource-adapter=org.apache.activemq.ra/:add(module=org.apache.activemq,transaction-support=NoTransaction)')
            print 'Add AMQ Resource Adapter module...end.'
    
            print 'Add AMQ Server URL...'
            cliConnected.cmd('/subsystem=resource-adapters/resource-adapter=org.apache.activemq.ra/config-properties=ServerUrl/:add(value=vm:localhost)')
            print 'Add AMQ Server URL...end.'                
    
            print 'Add AMQ Adapter module ID...'
            cliConnected.cmd('/subsystem=resource-adapters/resource-adapter=org.apache.activemq.ra/:write-attribute(name=ID,value=org.apache.activemq.ra)')
            print 'Add AMQ Adapter module ID...end.'
    except:
        print 'Operation for server: ' + servername + '...FAILED'
    finally:
        if (cliConnected != None) : cliConnected.disconnect()   
        
    print 'Switching JMS Provider to ActiveMQ...end.' 

def switchJMSProviderToHornetQ(servername, username, password):
    cliConnected = None
    foundExistingAMQResourceAdaptor = False
    
    print 'Switching JMS Provider for server: ' + servername + ' to HornetMQ...' 
    
    try:        
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :
    
            print 'Switch JMS to HornetQ...'
            cliConnected.cmd('/subsystem=ejb3/:write-attribute(name=default-resource-adapter-name,value=\"${ejb.resource-adapter-name:hornetq-ra}\")')
            print 'Switch JMS to HornetQ...end.'
    
            result = cliConnected.cmd('/subsystem=resource-adapters/:read-children-names(child-type=resource-adapter)')
            if (result.success) :
                response = result.getResponse()
                responseResultList = response.get("result").asList()
                responseResultListSize = response.get("result").asInt()
                for index in range(responseResultListSize):
                    responseResultListEntry = responseResultList[index].asString()
                    if (responseResultListEntry == 'org.apache.activemq.ra') :
                        print 'Found existing Resource Adapter: ' + responseResultListEntry + '...'
                        foundExistingAMQResourceAdaptor = True
                        break
      
            if (foundExistingAMQResourceAdaptor) :                    
                print 'Remove existing Resource Adapter...'
                cliConnected.cmd('/subsystem=resource-adapters/resource-adapter=org.apache.activemq.ra/:remove')
                print 'Remove existing Resource Adapter...end.'
    except:
        print 'switchJMSProviderToHornetQ for server: ' + servername + '...FAILED'
    finally:
        if (cliConnected != None) : cliConnected.disconnect()   

    print 'Switching JMS Provider for server: ' + servername + ' to HornetMQ...end.' 

def activeMQAddConnectionFactory(servername, username, password, factoryName, iMinPoolSize, iMaxPoolSize):
    foundExistingConxionFactory = False
    
    print 'ActiveMQ add connection factory...' 
    
    cliConnected = connectSilent(servername, username, password)
    if (cliConnected != None):
        result = cliConnected.cmd('/subsystem=resource-adapters/resource-adapter=org.apache.activemq.ra/:read-children-names(child-type=connection-definitions)')
        if (result.success) :
            response = result.getResponse()
            responseResultList = response.get("result").asList()
            responseResultListSize = response.get("result").asInt()
            for index in range(responseResultListSize):
                responseResultListEntry = responseResultList[index].asString()
                if (responseResultListEntry == factoryName) :
                    print 'Found existing Connection Factory: ' + responseResultListEntry + '...'
                    foundExistingConxionFactory = True
                    break
  
        if (foundExistingConxionFactory) :            
            cliConnected.cmd('/subsystem=resource-adapters/resource-adapter=org.apache.activemq.ra/connection-definitions=' + factoryName + '/:remove')
        cliConnected.cmd('/subsystem=resource-adapters/resource-adapter=org.apache.activemq.ra/connection-definitions=' + factoryName + '/:add(pool-prefill=false,no-tx-separate-pool=false,use-fast-fail=false,flush-strategy=FailingConnectionOnly,background-validation=false,interleaving=false,use-ccm=true,wrap-xa-resource=true,enabled=true,same-rm-override=false,use-java-context=true,pool-use-strict-min=false,security-application=false,min-pool-size=' + str(iMinPoolSize) + ',max-pool-size=' + str(iMaxPoolSize) + ',no-recovery=false,pad-xid=false,jndi-name=java:/jms/' + factoryName + ',class-name=org.apache.activemq.ra.ActiveMQManagedConnectionFactory)')    
    else :
        print 'activeMQAddConnectionFactory for server: ' + servername + '...FAILED'
        
    if (cliConnected != None) : cliConnected.disconnect()   

    print 'ActiveMQ add connection factory...end.' 

def activeMQAddTopic(servername, username, password, topicName, topicJNDI):    
    foundExistingTopic = False
    
    print 'ActiveMQ add topic...' 
    
    cliConnected = connectSilent(servername, username, password)
    if (cliConnected != None):
 
        result = cliConnected.cmd('/subsystem=resource-adapters/resource-adapter=org.apache.activemq.ra/:read-children-names(child-type=admin-objects)')
        if (result.success) :
            response = result.getResponse()
            responseResultList = response.get("result").asList()
            responseResultListSize = response.get("result").asInt()
            for index in range(responseResultListSize):
                responseResultListEntry = responseResultList[index].asString()
                if (responseResultListEntry == topicName) :
                    print 'Found existing Topic: ' + responseResultListEntry + '...'
                    foundExistingTopic = True
                    break
  
        if (foundExistingTopic) :
            cliConnected.cmd('/subsystem=resource-adapters/resource-adapter=org.apache.activemq.ra/admin-objects=' + topicName + '/:remove')
            
        cliConnected.cmd('/subsystem=resource-adapters/resource-adapter=org.apache.activemq.ra/admin-objects=' + topicName + '/config-properties=PhysicalName/:write-attribute(name=value,value=java:/topic/jms/' + topicName + ')')    
        cliConnected.cmd('/subsystem=resource-adapters/resource-adapter=org.apache.activemq.ra/admin-objects=' + topicName + '/:add(class-name=org.apache.activemq.command.ActiveMQTopic,jndi-name=' + topicJNDI + ',use-java-context=true,enabled=true)')
        cliConnected.cmd('/subsystem=resource-adapters/resource-adapter=org.apache.activemq.ra/admin-objects=' + topicName + '/config-properties=PhysicalName/:add(value=' + topicJNDI + ')')
    else :
        print 'activeMQAddTopic for server: ' + servername + '...FAILED'

    if (cliConnected != None) : cliConnected.disconnect()   

    print 'ActiveMQ add topic...end.' 

def availableProcessors(servername, username, password):    
    print 'availableProcessors()...'
    returnResult = getParameterValue(servername, username, password, "/core-service=platform-mbean/type=operating-system/", "available-processors,include-defaults=true") 
    print 'availableProcessors()...end.'
    return returnResult

def getMessagingProvider(servername, username, password):    
    print 'getMessagingProvider()...'
    returnResult = getParameterValue(servername, username, password, "/subsystem=ejb3/", "default-resource-adapter-name") 
    print 'getMessagingProvider()...end.'
    return returnResult

def getHornetQRedeliveryDelay(servername, username, password):
    print 'getHornetQRedeliveryDelay()...'
    returnResult = getParameterValue(servername, username, password, "/subsystem=messaging/hornetq-server=default/address-setting=#/", "redelivery-delay") 
    print 'getHornetQRedeliveryDelay()...end.'
    return returnResult

def getHornetQMaxdeliveryAttempts(servername, username, password):
    print 'getHornetQMaxdeliveryAttempts()...'
    returnResult = getParameterValue(servername, username, password, "/subsystem=messaging/hornetq-server=default/address-setting=#/", "max-delivery-attempts") 
    print 'getHornetQMaxdeliveryAttempts()...end.'
    return returnResult

def getLoggingCustomHandler(servername, username, password):
    print 'getLoggingCustomHandler() for server: ' + servername + '...'

    returnResult = ""
    cliConnected = None
    
    try :
        cliConnected = connectSilent(servername, username, password)
        if (cliConnected != None) :
            result = cliConnected.cmd('/subsystem=logging/:read-children-names(child-type=custom-handler)')
            if (result.success) :
                response = result.getResponse()
                returnResult = str(response.get("result").asString())
                print "getLoggingCustomHandler() for server, found : " + servername + " :" + returnResult
            else :
                returnResult = ""
                print 'getLoggingCustomHandler() for server: ' + servername + '...FAILED'
            
            cliConnected.disconnect()
        else:
            print 'getLoggingCustomHandler() for server: ' + servername + '...FAILED'
    
    except :
        if (cliConnected != None) : cliConnected.disconnect()
        returnResult = ""
        
    print 'getLoggingCustomHandler() for server: ' + servername + '...end.'
    
    return returnResult

def disableWelcomePage(servername, username, password):
    print 'Disable JBoss Welcome Page on: ' + servername + '...'
    cli = connect(servername, username, password)
    if (cli != None) :
        cli.cmd("/subsystem=web/virtual-server=default-host:write-attribute(name=enable-welcome-root,value=false)")
    else :
        print 'Disable JBoss Welcome Page on: ' + servername + '...FAILED.'
        
    if (cli != None) : cli.disconnect()
    print 'Disable JBoss Welcome Page on: ' + servername + '...end.'

def removeSampleWebAlias(servername, username, password):
    print 'Remove Default Example.com Alias on: ' + servername + '...'
    cli = connect(servername, username, password)
    if (cli != None) :
        cli.cmd("/subsystem=web/virtual-server=default-host/:write-attribute(name=alias,value=[\"localhost\"])")
    else :
        print 'Remove Default Example.com Alias on: ' + servername + '...FAILED.'
        
    if (cli != None) : cli.disconnect()
    print 'Remove Default Example.com Alias on: ' + servername + '...end.'
    
def setCustomServerHeader(servername, username, password):
    print 'Set Custom Server Header on: ' + servername + '...'
    cli = connect(servername, username, password)
    if (cli != None) :
        cli.cmd("/system-property=org.apache.coyote.http11.Http11Protocol.SERVER:add(value=NotAvailable)")
    else :
        print 'Set Custom Server Header on: ' + servername + '...FAILED.'
    if (cli != None) : cli.disconnect()
    print 'Set Custom Server Header on: ' + servername + '...end.'

def removeXpoweredBy(servername, username, password):
    print 'Remove X-Powered-By Flag on: ' + servername + '...'
    cli = connect(servername, username, password)
    if (cli != None) :
        cli.cmd("/subsystem=web/configuration=jsp-configuration/:write-attribute(name=X_POWERED_BY,value=false)")
        cli.cmd("/system-property=org.apache.catalina.connector.X_POWERED_BY:add(value=false)")
    else:
        print 'Remove X-Powered-By Flag on: ' + servername + '...FAILED.'
    if (cli != None) : cli.disconnect()
    print 'Remove X-Powered-By Flag on: ' + servername + '...end.'

def restrictHttpMethods(servername, username, password):
    print 'Restrict HTTP Methods on: ' + servername + '...'
    cli = connect(servername, username, password)
    if (cli != None) :
        cli.cmd("/subsystem=web/virtual-server=default-host/rewrite=httpmethods:add(flags=F,pattern=.*,substitution=-)")
        cli.cmd("/subsystem=web/virtual-server=default-host/rewrite=httpmethods/condition=condition-0:add(test=%{REQUEST_METHOD},pattern=^(PUT|HEAD|DELETE|TRACE|TRACK|OPTIONS)$,flags=NC)")
    else :
        print 'Restrict HTTP Methods on: ' + servername + '...FAILED.'
    if (cli != None) : cli.disconnect()
    print 'Restrict HTTP Methods on: ' + servername + '...end.'

def setUtf8Encoding(servername, username, password):
    print 'Setting UTF-8 Encoding on: ' + servername + '...'
    cli = connect(servername, username, password)
    if (cli != None) :
        cli.cmd("/system-property=org.apache.catalina.connector.URI_ENCODING:add(value=\"UTF-8\")")
        cli.cmd("/system-property=org.apache.catalina.connector.USE_BODY_ENCODING_FOR_QUERY_STRING:add(value=true)")

    if (cli != None) : cli.disconnect()
            
    print 'Setting UTF-8 Encoding on: ' + servername + '...end.'

def securityHardenJBoss(servername, username, password):    
    disableWelcomePage(servername, username, password)
    removeSampleWebAlias(servername, username, password)
    setCustomServerHeader(servername, username, password)
    removeXpoweredBy(servername, username, password)
    setUtf8Encoding(servername, username, password)
    restrictHttpMethods(servername, username, password)
    
def setAsyncConnectionFactoryPoolSize(servername, username, password, poolSizeMin, poolSizeMax):
    print 'setting AsyncConnectionFactoryPoolSize...'
    setParameterValue(servername, username, password, "/subsystem=messaging/hornetq-server=default/pooled-connection-factory=AsyncConnectionFactory/", "min-pool-size", poolSizeMin)
    setParameterValue(servername, username, password, "/subsystem=messaging/hornetq-server=default/pooled-connection-factory=AsyncConnectionFactory/", "max-pool-size", poolSizeMax)
    print 'setting AsyncConnectionFactoryPoolSize...end.'
    
def convertSha1SumToJbossCliHash(sha1sum):
    index = 0
    strLenSha1sum = len(sha1sum)
    cliHash = ''
    
    cliHash = cliHash + '[{\"hash\" => bytes {'
    while index < strLenSha1sum :
        if (index) % 2 == 0 :
            cliHash = cliHash + ' 0x' + sha1sum[index]
        else :
            cliHash = cliHash + sha1sum[index]
            if not(index + 1 == strLenSha1sum) :
                cliHash = cliHash + ','

        index = index + 1            
        
    cliHash = cliHash + ' }}]'
    
    return cliHash

def perfEnrichXAOracleDatasource(servername, username, password):
    print 'perfEnrichXADatasource...'
    
    dsList=getAllXaDataSources(servername, username, password)
    if (dsList) :
        for dsName in dsList:
            if (isServerReloadRequired(servername, username, password)) :
                reloadServerThenWait(servername, username, password)
                
            cliVector = sanitizeJDBCCliVector("/subsystem=datasources/xa-data-source=" + dsName)
            
            issueCliCommand(servername, username, password, cliVector + ':disable')

            dsUsername = getParameterValue(servername, username, password, cliVector, "user-name")
            dsPassword = getParameterValue(servername, username, password, cliVector, "password")
            dsURL = getParameterValue(servername, username, password, cliVector + "xa-datasource-properties=URL/", "value")
            
            disableXaDatasource(servername, username, password, dsName)
            issueCliCommand(servername, username, password, cliVector + ':remove')
            
            if (isServerReloadRequired(servername, username, password)) :
                reloadServerThenWait(servername, username, password)

            issueCliCommand(servername, username, password, cliVector +
                ":add(user-name=" + dsUsername + '),'
                "password=" + dsPassword + ',' +
                "spy=false, \
                wrap-xa-resource=true, \
                set-tx-query-timeout=false, \
                enabled=false, \
                same-rm-override=false, \
                statistics-enabled=true, \
                pool-use-strict-min=false, \
                validate-on-match=false, \
                no-recovery=false, \
                track-statements=NOWARN, \
                no-tx-separate-pool=false, \
                use-fast-fail=false, \
                flush-strategy=FailingConnectionOnly, \
                interleaving=false, \
                allow-multiple-users=false, \
                background-validation=true, \
                BackgroundValidationMillis=60000, \
                use-ccm=true, \
                use-java-context=true, \
                use-fast-fail=true, \
                min-pool-size=5, \
                max-pool-size=100, \
                pad-xid=false, \
                pool-prefill=false, \
                share-prepared-statements=false, \
                exception-sorter-class-name=\"org.jboss.jca.adapters.jdbc.extensions.oracle.OracleExceptionSorter\", \
                TrackStatements=NOWARN, \
                check-valid-connection-sql=\"select 1 from dual\", \
                valid-connection-checker-class-name=\"org.jboss.jca.adapters.jdbc.extensions.oracle.OracleValidConnectionChecker\", \
                flush-strategy=FailingConnectionOnly, \
                idle-timeout-minutes=5, \
                blocking-timeout-wait-millis=90000, \
                pool-prefill=false, \
                jndi-name=java:jboss/datasources/" + dsName + ',' +
                "driver-name=\"com.informatica.mdm.jdbc\")")
 
            issueCliCommand(servername, username, password, sanitizeJDBCCliVector("/subsystem=datasources/xa-data-source=" + dsName + "/xa-datasource-properties=URL/") + ":add(value=" + dsURL + ')')
            issueCliCommand(servername, username, password, sanitizeJDBCCliVector("/subsystem=datasources/xa-data-source=" + dsName + "/xa-datasource-properties=ConnectionProperties/") + ':add(value=\"oracle.jdbc.J2EE13Compliant=true\")')

            if (isServerReloadRequired(servername, username, password)) :
                reloadServerThenWait(servername, username, password)
            
            enableXaDatasource(servername, username, password, dsName)                

            if (isServerReloadRequired(servername, username, password)) :
                reloadServerThenWait(servername, username, password)
    else :
        print '    no xa datasources found...'
        
    print 'perfEnrichXADatasource...end.'

def perfEnrichOracleDatasource(servername, username, password):
    print 'perfEnrichDatasource...'
    
    dsList=getAllDataSources(servername, username, password)
    if (dsList) :
        for dsName in dsList:
            if (isServerReloadRequired(servername, username, password)) :
                reloadServerThenWait(servername, username, password)
                
            cliVector = sanitizeJDBCCliVector("/subsystem=datasources/data-source=" + dsName)
            
            issueCliCommand(servername, username, password, cliVector + ':disable')

            dsUsername = getParameterValue(servername, username, password, cliVector, "user-name")
            dsPassword = getParameterValue(servername, username, password, cliVector, "password")
            dsURL = getParameterValue(servername, username, password, cliVector + "datasource-properties=URL/", "value")
            
            disableDatasource(servername, username, password, dsName)
            issueCliCommand(servername, username, password, cliVector + ':remove')
            
            if (isServerReloadRequired(servername, username, password)) :
                reloadServerThenWait(servername, username, password)

            issueCliCommand(servername, username, password, cliVector +
                ":add(user-name=" + dsUsername + ',' +
                "password=" + dsPassword + ',' +
                "spy=false, \
                set-tx-query-timeout=false, \
                enabled=false, \
                same-rm-override=false, \
                statistics-enabled=true, \
                pool-use-strict-min=false, \
                validate-on-match=false, \
                no-recovery=false, \
                track-statements=NOWARN, \
                no-tx-separate-pool=false, \
                use-fast-fail=false, \
                flush-strategy=FailingConnectionOnly, \
                interleaving=false, \
                allow-multiple-users=false, \
                background-validation=true, \
                BackgroundValidationMillis=60000, \
                use-ccm=true, \
                use-java-context=true, \
                use-fast-fail=true, \
                min-pool-size=5, \
                max-pool-size=100, \
                pad-xid=false, \
                pool-prefill=false, \
                share-prepared-statements=false, \
                exception-sorter-class-name=\"org.jboss.jca.adapters.jdbc.extensions.oracle.OracleExceptionSorter\", \
                TrackStatements=NOWARN, \
                check-valid-connection-sql=\"select 1 from dual\", \
                valid-connection-checker-class-name=\"org.jboss.jca.adapters.jdbc.extensions.oracle.OracleValidConnectionChecker\", \
                flush-strategy=FailingConnectionOnly, \
                idle-timeout-minutes=5, \
                blocking-timeout-wait-millis=90000, \
                pool-prefill=false, \
                jndi-name=java:jboss/datasources/" + dsName + ',' +
                "driver-name=\"oracle.jdbc.OracleDriver\")")
 
            issueCliCommand(servername, username, password, sanitizeJDBCCliVector("/subsystem=datasources/data-source=" + dsName + "/xa-datasource-properties=URL/") + ":add(value=" + dsURL + ')')
            issueCliCommand(servername, username, password, sanitizeJDBCCliVector("/subsystem=datasources/data-source=" + dsName + "/xa-datasource-properties=ConnectionProperties/") + ':add(value=\"oracle.jdbc.J2EE13Compliant=true\")')

            if (isServerReloadRequired(servername, username, password)) :
                reloadServerThenWait(servername, username, password)
            
            enableDatasource(servername, username, password, dsName)                

            if (isServerReloadRequired(servername, username, password)) :
                reloadServerThenWait(servername, username, password)
    else :
        print '    no datasources found...'
        
    print 'perfEnrichDatasource...end.'

def perfEnrichDatasource(servername, username, password):
    print 'perfEnrichDatasource...'
    
    dsList=getAllDataSources(servername, username, password)
    if (dsList) :
        for dsName in dsList:
            if (isServerReloadRequired(servername, username, password)) :
                reloadServerThenWait(servername, username, password)
                
            cliVector = sanitizeJDBCCliVector("/subsystem=datasources/data-source=" + dsName)
            
            issueCliCommand(servername, username, password, cliVector + ':disable')

            dsUsername = getParameterValue(servername, username, password, cliVector, "user-name")
            dsPassword = getParameterValue(servername, username, password, cliVector, "password")
            dsURL = getParameterValue(servername, username, password, cliVector + "datasource-properties=URL/", "value")
            
            disableDatasource(servername, username, password, dsName)
            issueCliCommand(servername, username, password, cliVector + ':remove')
            
            if (isServerReloadRequired(servername, username, password)) :
                reloadServerThenWait(servername, username, password)

            issueCliCommand(servername, username, password, cliVector +
                ":add(user-name=" + dsUsername + ',' +
                "password=" + dsPassword + ',' +
                "spy=false, \
                set-tx-query-timeout=false, \
                enabled=false, \
                same-rm-override=false, \
                statistics-enabled=true, \
                pool-use-strict-min=false, \
                validate-on-match=false, \
                no-recovery=false, \
                track-statements=NOWARN, \
                no-tx-separate-pool=false, \
                use-fast-fail=false, \
                flush-strategy=FailingConnectionOnly, \
                interleaving=false, \
                allow-multiple-users=false, \
                background-validation=true, \
                BackgroundValidationMillis=60000, \
                use-ccm=true, \
                use-java-context=true, \
                use-fast-fail=true, \
                min-pool-size=5, \
                max-pool-size=100, \
                pad-xid=false, \
                pool-prefill=false, \
                share-prepared-statements=false, \
                exception-sorter-class-name=\"org.jboss.jca.adapters.jdbc.extensions.oracle.OracleExceptionSorter\", \
                TrackStatements=NOWARN, \
                check-valid-connection-sql=\"select 1 from dual\", \
                valid-connection-checker-class-name=\"org.jboss.jca.adapters.jdbc.extensions.oracle.OracleValidConnectionChecker\", \
                flush-strategy=FailingConnectionOnly, \
                idle-timeout-minutes=5, \
                blocking-timeout-wait-millis=90000, \
                pool-prefill=false, \
                jndi-name=java:jboss/datasources/" + dsName + ',' +
                "driver-name=\"com.informatica.mdm.jdbc\")")
 
            issueCliCommand(servername, username, password, sanitizeJDBCCliVector("/subsystem=datasources/data-source=" + dsName + "/xa-datasource-properties=URL/") + ":add(value=" + dsURL + ')')

            if (isServerReloadRequired(servername, username, password)) :
                reloadServerThenWait(servername, username, password)
            
            enableDatasource(servername, username, password, dsName)                

            if (isServerReloadRequired(servername, username, password)) :
                reloadServerThenWait(servername, username, password)
    else :
        print '    no datasources found...'
        
    print 'perfEnrichDatasource...end.'

def addDBDriver(servername, username, password, driverName, moduleName, driverClass):
    print 'addDriver...'
    issueCliCommand(servername, username, password, '/subsystem=datasources/jdbc-driver=' + driverName + '/:'
        'add(driver-name=' + driverName +
        ',driver-module-name=' + moduleName + 
        ',driver-class-name=' + driverClass + ')')
    print 'addDriver...end.'


def addModule(servername, username, password,moduleName, resourceJars, dependancies):
    print 'addModule...'
    issueCliCommand(servername, username, password, 
         "module add --name=" + moduleName +
         " --resources=" + resourceJars +
         " --dependencies=" + dependancies)
    print 'addModule...end.'
    
def createDatasource(servername, username, password, jndiName, poolname, connectionUrl, drivername, driverClassName, dsUsername, dsPassword):        
    print 'createDatasource...'
        
    issueCliCommand(servername, username, password, 
        "/subsystem=datasources/data-source=" + poolname + "/:add(" + 
        "jndi-name=" + jndiName + 
        ",driver-name=" + drivername +
        ',connection-url=\"' + connectionUrl + '\"' +
        ",driver-class=" + driverClassName +
        ",max-pool-size=20" +
        ",min-pool-size=0" +
        ",track-statements=NOWARN" +
        ",flush-strategy=FailingConnectionOnly" +
        ",statistics-enabled=true" +  
        ",user-name=\"" + dsUsername + "\""
        ",password=\"" + dsPassword + '\"' +  
        ")")

    print 'createDatasource...end.'

