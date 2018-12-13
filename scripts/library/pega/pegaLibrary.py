'''
Created on 15 Jul 2016

@author:
'''
from library.jboss.jbossLibrary import connectSilent, \
    deployToServer, upgradeToServer, \
    setStatelessSessionBeanStrictMaxPool, setMessageDrivenBeanStrictMaxPool, \
    setAsyncConnectionFactoryPoolSize, \
    getDatasourceConnectionURL, disableWelcomePage, \
    removeSampleWebAlias, setCustomServerHeader, removeXpoweredBy, \
    restrictHttpMethods, setUtf8Encoding, setDatasourceCredentialsSingleDS, \
    setDatasourceConnectionURL


# Assumes all Pega DS use the same password scheme. You ought to copy this method
# and use it more locally to specify the credentials.
def setJdbcCredentialsAllPegaDS(servername, username, password):
    print "Setting Pega Datasources Credentials and URL..."
    setDatasourceCredentialsSingleDS(servername, username, password, "AdminPegaRULES", "username", "password")
    setDatasourceCredentialsSingleDS(servername, username, password, "PegaRULES", "username", "password")
    setDatasourceCredentialsSingleDS(servername, username, password, "adm7DataSource", "username", "password")
    setDatasourceCredentialsSingleDS(servername, username, password, "ihDataSource", "username", "password")
    setDatasourceCredentialsSingleDS(servername, username, password, "vbdDataSource", "username", "password")
    setDatasourceCredentialsSingleDS(servername, username, password, "padDataSource", "username", "password")
    setDatasourceCredentialsSingleDS(servername, username, password, "nbamDataSource", "username", "password")
    print "Setting Pega Datasources Credentials and URL...end."
    

def createCTIBoundedQueueThreadPool(servername, username, password):
    cli = None
    connected = False
    
    print 'createCTIBoundedQueueThreadPool for server: ' + servername + '...'

    try:        
        cli = connectSilent(servername, username, password)
        if (cli) :
            connected = True
                
        print 'createCTIBoundedQueueThreadPool...'
        cli.cmd('/subsystem=threads/thread-factory=ctiThreadFactory/:add')
        cli.cmd('/subsystem=threads/bounded-queue-thread-pool=ctiThreadPool/:add(queue-length=500,max-threads=200,core-threads=8,thread-factory=ctiThreadFactory,allow-core-timeout=false)')
        print 'createCTIBoundedQueueThreadPool...end.'

    except :
        print 'createCTIBoundedQueueThreadPool for server: ' + servername + ' failed: '
        
    finally:
        if (connected): cli.disconnect()

    print 'createCTIBoundedQueueThreadPool for server: ' + servername + '...end.'
    
def setPegaJdbcExaDataOptionsNonXADataSources(servername, username, password):

    cli = None
    connected = False
    
    print 'setPegaJdbcExaDataOptionsNonXADataSources for server: ' + servername + '...'

    try:        
        cli = connectSilent(servername, username, password)
        if (cli) :
            connected = True
                
        setDatasourceCredentialsSingleDS(servername, username, password, 'AdminPegaRULES');
        setDatasourceCredentialsSingleDS(servername, username, password, 'PegaRULES');
        setDatasourceCredentialsSingleDS(servername, username, password, 'adm7DataSource');
        setDatasourceCredentialsSingleDS(servername, username, password, 'ihDataSource');
        setDatasourceCredentialsSingleDS(servername, username, password, 'nbamDataSource');
        setDatasourceCredentialsSingleDS(servername, username, password, 'padDataSource');
        setDatasourceCredentialsSingleDS(servername, username, password, 'vbdDataSource');
   
    except:
        print 'setPegaJdbcExaDataOptionsNonXADataSources for server: ' + servername + ' failed: '
        
    finally:
        if (connected): cli.disconnect()

    print 'setPegaJdbcExaDataOptionsNonXADataSources for server: ' + servername + '...end.'
  
def deployPegaMS(servername, username, password, applicationDeploymentSourceFolder):
    print 'Deploying MS for server: ' + servername + '...'
    
    cli = None

    try:        
        cli = connectSilent(servername, username, password)
        if cli.getCommandContext().isDomainMode():
            cli.cmd("cd /host=master/core-service=platform-mbean/type=runtime")
        else:
            cli.cmd("cd /core-service=platform-mbean/type=runtime")
        
        deploymentArtefact = 'MS.war'
        deployToServer(servername, username, password, applicationDeploymentSourceFolder, deploymentArtefact)                

    except :
        print 'Deploying to server: ' + servername + ' FAILED: '
        
    finally:
        cli.disconnect()

    print 'Deploying MS for server: ' + servername + '...end.'

def deployPegaGateway(servername, username, password, applicationDeploymentSourceFolder):
    print 'Deploying Gateway/IAC for server: ' + servername + '...'
    
    cli = None

    connected = False
    
    try:        
        cli = connectSilent(servername, username, password)
        connected = True
        
        if cli.getCommandContext().isDomainMode():
            cli.cmd("cd /host=master/core-service=platform-mbean/type=runtime")
        else:
            cli.cmd("cd /core-service=platform-mbean/type=runtime")
        
        deploymentArtefact = 'prgateway.war'
        deployToServer(servername, username, password, applicationDeploymentSourceFolder, deploymentArtefact)                

    except :
        print 'Deploying to server: ' + servername + ' FAILED: '
        
    finally:
        if (connected) : cli.disconnect()

    print 'Deploying Gateway/IAC for server: ' + servername + '...end.'

def deployPegaADM(servername, username, password, applicationDeploymentSourceFolder):
    print 'Deploying ADM for server: ' + servername + '...'
    
    try:        
        deploymentArtefact = 'adm7.ear'
        deployToServer(servername, username, password, applicationDeploymentSourceFolder, deploymentArtefact)                
    except:
        print 'Deploying to server: ' + servername + ' FAILED: '
    finally:
        None
            
    print 'Deploying ADM for server: ' + servername + '...end.'
    

def upgradePegaADM(servername, username, password, applicationDeploymentSourceFolder):
    print 'Upgrading ADM for server: ' + servername + '...'
    
    try:        
        deploymentArtefact = 'adm7.ear'
        upgradeToServer(servername, username, password, applicationDeploymentSourceFolder, deploymentArtefact)                
    except:
        print 'Deploying to server: ' + servername + ' FAILED: '
        
    finally:
        None

    print 'Upgrading ADM for server: ' + servername + '...end.'
    
def deployPegaPRPC(servername, username, password, applicationDeploymentSourceFolder):
    print 'Deploying PRPC for server: ' + servername + '...'
    
    try:        
        deploymentArtefact = 'prpc_j2ee14_jboss61JBM.ear'
        deployToServer(servername, username, password, applicationDeploymentSourceFolder, deploymentArtefact)                            
    except:
        print 'Deploying to server: ' + servername + ' FAILED: '
        
    finally:
        None

    print 'Deploying PRPC for server: ' + servername + '...end.'
    
def upgradePegaPRPC(servername, username, password, applicationDeploymentSourceFolder):
    print 'Upgrading PRPC for server: ' + servername + '...'
    
    try:        
        deploymentArtefact = 'prpc_j2ee14_jboss61JBM.ear'
        upgradeToServer(servername, username, password, applicationDeploymentSourceFolder, deploymentArtefact)                            
    except :
        print 'Deploying to server: ' + servername + ' FAILED: '
    finally:
        None

    print 'Upgrading PRPC for server: ' + servername + '...end.'
    
def upgradePegaPRSysManage(servername, username, password, applicationDeploymentSourceFolder):
    print 'Upgrading PRPC for server: ' + servername + '...'
    
    try:        
        deploymentArtefact = 'prsysmgmt_jboss.ear'
        upgradeToServer(servername, username, password, applicationDeploymentSourceFolder, deploymentArtefact)                            
    except :
        print 'Deploying to server: ' + servername + ' FAILED: '
    finally:
        None

    print 'Upgrading PRPC for server: ' + servername + '...end.'
    

def deployPegaPRSYSManage(servername, username, password, applicationDeploymentSourceFolder):
    print 'Deploying PRSYSManage for server: ' + servername + '...'
    
    try:        
        deploymentArtefact = 'prsysmgmt_jboss.ear'
        deployToServer(servername, username, password, applicationDeploymentSourceFolder, deploymentArtefact)                                
    except:
        print 'Deploying to server: ' + servername + ' FAILED: '
        
    finally:
        None

    print 'Deploying PRSYSManage for server: ' + servername + '...end.'

def deployPegaPRHelp(servername, username, password, applicationDeploymentSourceFolder):
    print 'Deploying PRHelp for server: ' + servername + '...'
    
    try:        
        deploymentArtefact = 'prhelp.war'
        deployToServer(servername, username, password, applicationDeploymentSourceFolder, deploymentArtefact)                
    except:
        print 'Deploying to server: ' + servername + ' FAILED: '
    finally:
        None

    print 'Deploying PRHelp for server: ' + servername + '...end.'    

def deployPegaMarketingHelp(servername, username, password, applicationDeploymentSourceFolder):
    print 'Deploying MarketingHelp for server: ' + servername + '...'
    
    cli = None

    try:        
        cli = connectSilent(servername, 9999, username, password)
        deploymentArtefact = 'MarketingHelp.war'
        deployToServer(servername, username, password, applicationDeploymentSourceFolder, deploymentArtefact)                        

    except :
        print 'Install to server: ' + servername + ' FAILED: '

    finally:
        cli.disconnect()

    print 'Deploying MarketingHelp for server: ' + servername + '...end.' 

def deployPegaVBD(servername, username, password, applicationDeploymentSourceFolder):
    print 'Deploying VBD for server: ' + servername + '...'
    
    try:        
        deploymentArtefact = 'vbd.ear'
        deployToServer(servername, username, password, applicationDeploymentSourceFolder, deploymentArtefact)                                
    except:
        print 'Deploying to server: ' + servername + ' FAILED: '
    finally:
        None

    print 'Deploying VBD for server: ' + servername + '...end.'

def deployPegaApps(servername, username, password, applicationDeploymentSourceFolder):
    print 'Deploying Pega Suite - all applications...'
    deployPegaADM(servername, username, password, applicationDeploymentSourceFolder)
    deployPegaMarketingHelp(servername, username, password, applicationDeploymentSourceFolder)
    deployPegaMS(servername, username, password, applicationDeploymentSourceFolder)
    deployPegaPRHelp(servername, username, password, applicationDeploymentSourceFolder)
    deployPegaPRPC(servername, username, password, applicationDeploymentSourceFolder)
    deployPegaPRSYSManage(servername, username, password, applicationDeploymentSourceFolder)
    deployPegaVBD(servername, username, password, applicationDeploymentSourceFolder)
    print 'Deploying Pega Suite - all applications...end.'

def upgradePegaApps(servername, username, password, applicationDeploymentSourceFolder):
    print 'Upgrading Applications for server: ' + servername + '...'
    
    connected = False
    cli = None

    try:        
        cli = connectSilent(servername, username, password)
        if (cli) : connected = True

        print 'Upgrading prgateway.war...'
        result = cli.cmd("undeploy prgateway.war")
        print('prgateway.war remove result: ' + result.getResponse().asString())
        if (result.success):
            result = cli.cmd('deploy "' + applicationDeploymentSourceFolder + '\prgateway.war"')
            print('prgateway.war install result: ' + result.getResponse().asString())
        print 'Upgrading prgateway.war...end.'

        print 'Upgrading MS.war...'
        result = cli.cmd("undeploy MS.war")
        print('MS.war remove result: ' + result.getResponse().asString())
        if (result.success):
            result = cli.cmd('deploy "' + applicationDeploymentSourceFolder + '\MS.war"')
            print('MS.war install result: ' + result.getResponse().asString())
        print 'Upgrading MS.war...end.'
     
        print 'Upgrading PRPC ear...'
        result = cli.cmd("undeploy prpc_j2ee14_jboss61JBM.ear")
        print('prpc_j2ee14_jboss61JBM.ear remove result: ' + result.getResponse().asString())
        if (result.success):
            result = cli.cmd('deploy "' + applicationDeploymentSourceFolder + '\prpc_j2ee14_jboss61JBM.ear"')
            print('prpc_j2ee14_jboss61JBM.war install result: ' + result.getResponse().asString())
        print 'Upgrading PRPC ear...end.'
      
        print 'Upgrading PRSys Manage ear...'
        result = cli.cmd("undeploy prsysmgmt_jboss.ear")
        print('prsysmgmt_jboss.ear remove result: ' + result.getResponse().asString())
        if (result.success):
            result = cli.cmd('deploy "' + applicationDeploymentSourceFolder + '\prsysmgmt_jboss.ear"')
            print('prsysmgmt_jboss.ear install result: ' + result.getResponse().asString())
        print 'Upgrading PRSys Manage ear...end.'
 
        print 'Upgrading ADM7 ear...'
        result = cli.cmd("undeploy adm7.ear")
        print('adm7.ear remove result: ' + result.getResponse().asString())
        if (result.success):
            result = cli.cmd('deploy "' + applicationDeploymentSourceFolder + '\adm7.ear"')
            print('adm7.ear install result: ' + result.getResponse().asString())
        print 'Upgrading ADM7 ear...end.'
 
        print 'Upgrading VBD ear...'
        result = cli.cmd("undeploy vbd.ear")
        print('vbd.ear remove result: ' + result.getResponse().asString())
        if (result.success):
            result = cli.cmd('deploy "' + applicationDeploymentSourceFolder + '\vbd.ear"')
            print('vbd.ear install result: ' + result.getResponse().asString())
        print 'Upgrading VBD ear...end.'
 
        print 'Upgrading PRHelp war...'
        result = cli.cmd("undeploy prhelp.war")
        print('prhelp.war remove result: ' + result.getResponse().asString())
        if (result.success):
            result = cli.cmd('deploy "' + applicationDeploymentSourceFolder + '\prhelp.war"')
            print('prhelp.war install result: ' + result.getResponse().asString())
        print 'Upgrading PRHelp war...end.'

    except:
        print 'Update to server: ' + servername + ' FAILED: '
    finally:
        if (connected) : cli.disconnect()

    print 'Upgrading Applications for server: ' + servername + '...end.'

def perfTunePegaJBossForAviya(servername, username, password, numExpectedUsers):
    print 'perfTuneJBossForPega: ' + servername + '...' 

    poolSize = numExpectedUsers + round((numExpectedUsers * 30) / 100) 

    setStatelessSessionBeanStrictMaxPool(servername, username, password, poolSize)
    setMessageDrivenBeanStrictMaxPool(servername, username, password, poolSize)
    setAsyncConnectionFactoryPoolSize(servername, username, password, '64', poolSize)
    createCTIBoundedQueueThreadPool(servername, username, password)

    print 'perfTuneJBossForPega: ' + servername + '...end.' 

def perfTunePegaJBossForAviyaNoProvisionCalc(servername, username, password, poolSize):
    print 'perfTuneJBossForPega: ' + servername + '...' 

    setStatelessSessionBeanStrictMaxPool(servername, username, password, poolSize)
    setMessageDrivenBeanStrictMaxPool(servername, username, password, poolSize)
    setAsyncConnectionFactoryPoolSize(servername, username, password, '64', poolSize)
    createCTIBoundedQueueThreadPool(servername, username, password)

    print 'perfTuneJBossForPega: ' + servername + '...end.' 

def getJdbcConnectionUrlAllPegaDataSourceSingleServer(servername, username, password):
    print "getJdbcConnectionUrlAllPegaDataSourceSingleServer() for " + servername + "..."            
    returnResult = getJdbcConnectionUrlAllPegaDataSource(servername, username, password)
    print "getJdbcConnectionUrlAllPegaDataSourceSingleServer() for " + servername + "...end."
    
    return returnResult 
    
def getJdbcConnectionUrlAllPegaDataSource(servername, username, password):
    returnResult = []
    
    print "Getting Pega Datasources URL..."
    
    PegaRULESDs = getDatasourceConnectionURL(servername, username, password, "PegaRULES")
    adm7DataSourceDs = getDatasourceConnectionURL(servername, username, password, "adm7DataSource")
    ihDataSourceDs = getDatasourceConnectionURL(servername, username, password, "ihDataSource")
    vbdDataSourceDs = getDatasourceConnectionURL(servername, username, password, "vbdDataSource")
    padDataSourceDs = getDatasourceConnectionURL(servername, username, password, "padDataSource")
    nbamDataSourceDs = getDatasourceConnectionURL(servername, username, password, "nbamDataSource")
    AdminPegaRULESDs = getDatasourceConnectionURL(servername, username, password, "AdminPegaRULES")
    
    if (PegaRULESDs != "") : returnResult.append(PegaRULESDs)
    if (adm7DataSourceDs != "") : returnResult.append(adm7DataSourceDs)
    if (ihDataSourceDs != "") : returnResult.append(ihDataSourceDs)
    if (vbdDataSourceDs != "") : returnResult.append(vbdDataSourceDs)
    if (padDataSourceDs != "") : returnResult.append(padDataSourceDs)
    if (nbamDataSourceDs != "") : returnResult.append(nbamDataSourceDs)
    if (AdminPegaRULESDs != "") : returnResult.append(AdminPegaRULESDs)
    
    print "Getting Pega Datasources URL...end."
    
    return returnResult
    
def setJdbcConnectionURLAllPegaDS(servername, username, password, connectionUrl):
    
    print 'setJdbcConnectionURLAllPegaDS...'
     
    setDatasourceConnectionURL(servername, username, password, "PegaRULES", connectionUrl)
    setDatasourceConnectionURL(servername, username, password, "adm7DataSource", connectionUrl)
    setDatasourceConnectionURL(servername, username, password, "ihDataSource", connectionUrl)
    setDatasourceConnectionURL(servername, username, password, "vbdDataSource", connectionUrl)
    setDatasourceConnectionURL(servername, username, password, "padDataSource", connectionUrl)
    setDatasourceConnectionURL(servername, username, password, "nbamDataSource", connectionUrl)
    setDatasourceConnectionURL(servername, username, password, "AdminPegaRULES", connectionUrl)       

    print 'setJdbcConnectionURLAllPegaDS...end.'
    
def switchOffPrWebForDMZServers(servername, username, password, virtualServerName):
    print 'switch Off PrWeb For DMZ Servers...'
    
    cliConnected = connectSilent(servername, username, password)    
    cliConnected.cmd('/subsystem=web/virtual-server=' + virtualServerName + '/rewrite=noPrWeb/:add(substitution=/,flags=nocase,pattern=^/prweb/)')    
    if (cliConnected != None) : cliConnected.disconnect()    
    
    print 'switch Off PrWeb For DMZ Servers...end.'
    
def securityHardenJBoss(servername,username,password):    
    disableWelcomePage(servername, username, password)
    removeSampleWebAlias(servername, username, password)
    setCustomServerHeader(servername, username, password)
    removeXpoweredBy(servername, username, password)
    restrictHttpMethods(servername, username, password)
    setUtf8Encoding(servername, username, password)

