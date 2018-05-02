'''
Created on 15 Jul 2016

@author: 
'''
from library.jboss.jbossLibrary import disableWelcomePage, removeSampleWebAlias, \
    setCustomServerHeader, removeXpoweredBy, connectSilent, setUtf8Encoding, \
    restrictHttpMethods

def informaticaJBossConfigure(cli):
    print 'Setting transactions default-timeout...'
    cli.cmd('/subsystem=transactions:write-attribute(name=default-timeout,value=3600)')
    print 'Setting transactions default-timeout...end.'
    
    print 'Setting hornetq-server security-enabled...'
    cli.cmd('/subsystem=messaging/hornetq-server=default/:write-attribute(name=security-enabled,value=false)')
    print 'Setting hornetq-server security-enabled...end.'
    
    print 'Setting hornetq-server persistence-enabled...'
    cli.cmd('/subsystem=messaging/hornetq-server=default/:write-attribute(name=persistence-enabled,value=true)')
    print 'Setting hornetq-server persistence-enabled...end.'
    
    print 'Setting remoting-connector undefine security-realm...'
    cli.cmd('/subsystem=remoting/connector=remoting-connector/:undefine-attribute(name=security-realm)')
    print 'Setting remoting-connector undefine security-realm...end.'
    
    print 'Increase Siperian Datasource pool sizes...'
    cli.cmd('/subsystem=datasources/xa-data-source=jdbc\/siperian-cmx_system-ds/:write-attribute(name=min-pool-size,value=50)')
    cli.cmd('/subsystem=datasources/xa-data-source=jdbc\/siperian-cmx_system-ds/:write-attribute(name=max-pool-size,value=500)')
    print 'Increase Siperian Datasource pool sizes...end.'
    
    # Although detailed in the install guide, this is not necessary.
    # JBoss will allocate sufficient threads per cpu
#     print 'Increase Web Connections threads...'
#     cli.cmd('/subsystem=web/connector=http/:write-attribute(name=max-connections,value=300)')
#     cli.cmd('/subsystem=web/connector=https/:write-attribute(name=max-connections,value=300)')
#     print 'Increase Web Connections threads...end.'
    
    print 'Increase EJB Pool threads...'
    cli.cmd('/subsystem=ejb3/thread-pool=default/:write-attribute(name=max-threads,value=300)')
    print 'Increase EJB Pool threads...end.'
    
def upgradeMDMApps(servername, serverusername, serverPassword, applicationDeploymentSourceFolder):
    cli = None
    
    print 'upgradeCMD Applications for server: ' + servername + '...'
    
    try:        
        cli = connectSilent(servername, serverusername, serverPassword)
        
        result = cli.cmd("undeploy entity360view-ear.ear")
        print('entity360view-ear.ear remove result: ' + result.getResponse().asString())
        undeployResult = result.getResponse().asString()
        if (result.success):
            result = cli.cmd('deploy "' + applicationDeploymentSourceFolder + '\entity360view-ear.ear"')
            print('entity360view-ear.ear install result: ' + result.getResponse().asString())
 
        result = cli.cmd("undeploy informatica-mdm-platform-ear.ear")
        print('informatica-mdm-platform-ear.ear remove result: ' + result.getResponse().asString())
        undeployResult = result.getResponse().asString()
        if (result.success):
            result = cli.cmd('deploy "' + applicationDeploymentSourceFolder + '\informatica-mdm-platform-ear.ear"')
            print('informatica-mdm-platform-ear.ear install result: ' + result.getResponse().asString())
 
        result = cli.cmd("undeploy siperian-mrm.ear")
        print('siperian-mrm.ear remove result: ' + result.getResponse().asString())
        undeployResult = result.getResponse().asString()
        if (result.success):
            result = cli.cmd('deploy "' + applicationDeploymentSourceFolder + '\siperian-mrm.ear"')
            print('siperian-mrm.ear install result: ' + result.getResponse().asString())

        result = cli.cmd("undeploy siperian-mrm-cleanse.ear")
        print('siperian-mrm-cleanse.ear remove result: ' + result.getResponse().asString())
        undeployResult = result.getResponse().asString()
        if (result.success):
            result = cli.cmd('deploy "' + applicationDeploymentSourceFolder + '\siperian-mrm-cleanse.ear"')
            print('siperian-mrm-cleanse.ear install result: ' + result.getResponse().asString())

    # except Exception, e:
    except:
        print 'Upgrade for server: ' + servername + ' FAILED: '
    finally:
        if (cli != None) : cli.disconnect()

    print 'upgradeCMD Applications for server: ' + servername + '...end.'

def deployMDMApps(servername, serverusername, serverPassword, applicationDeploymentSourceFolder):
    
    print 'deployMDM Applications for server: ' + servername + '...'
    
    cli = None

    try:        
        cli = connectSilent(servername, serverusername, serverPassword)
      
        print 'Deploying entity360view...'
        result = cli.cmd('deploy --force "' + applicationDeploymentSourceFolder + '\entity360view-ear.ear"')
        print('entity360view-ear.ear install result: ' + result.getResponse().asString())
        print 'Deploying entity360view...end.'
 
        print 'Deploying informatica-mdm-platform-ear...'
        result = cli.cmd('deploy --force "' + applicationDeploymentSourceFolder + '\informatica-mdm-platform-ear.ear"')
        print('informatica-mdm-platform-ear.ear install result: ' + result.getResponse().asString())
        print 'Deploying informatica-mdm-platform-ear...end.'
 
        print 'Deploying siperian-mrm...'
        result = cli.cmd('deploy --force "' + applicationDeploymentSourceFolder + '\siperian-mrm.ear"')
        print('siperian-mrm.ear install result: ' + result.getResponse().asString())
        print 'Deploying siperian-mrm...end.'

        print 'Deploying siperian-mrm-cleanse...'
        result = cli.cmd('deploy --force "' + applicationDeploymentSourceFolder + '\siperian-mrm-cleanse.ear"')
        print('siperian-mrm-cleanse.ear install result: ' + result.getResponse().asString())
        print 'Deploying siperian-mrm-cleanse...end.'

    # except Exception, e:
    except:
        print 'Deploy for server: ' + servername + ' FAILED: '
    finally:
        if (cli != None) : cli.disconnect()

    print 'deployMDM Applications for server: ' + servername + '...end.'

def securityHardenJBoss(servername, username, password):    
    disableWelcomePage(servername, username, password)
    removeSampleWebAlias(servername, username, password)
    setCustomServerHeader(servername, username, password)
    removeXpoweredBy(servername, username, password)
    setUtf8Encoding(servername, username, password)
    
    # Restricting HTTP methods breaks MDM
    # restrictHttpMethods(servername, username, password)
