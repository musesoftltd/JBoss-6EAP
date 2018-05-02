'''
Created on 4 Apr 2017
 
@author: x
'''
# from environmentProperties.allEnvs import propertiesMdm as globalProperties
from environmentProperties.allEnvs import propertiesMdm as globalProperties
from library.auditing.auditServerBase import auditServersBaseAudit
from library.auditing.auditingLibrary import auditObjectAtoms, auditObjectAtom, \
        auditObjectMolecule, auditReport
from library.jboss.jbossLibrary import connectSilent
from library.util import scatterThread, gatherThreads
 
 
def auditServersMdmThread(environment, servername, propertiesDict, bApplyRequiredChanges) :
    # merge global propertiesDict into dict - deliberately overwriting local with global dict all values
    runtimeProperties = dict()
    runtimeProperties.update(globalProperties.dictionary)
    runtimeProperties.update(propertiesDict)

    if connectSilent(servername, runtimeProperties["username"], runtimeProperties["password"]) == None:
        return
       
    ##############################################################
    # Base server audit...
    ##############################################################
    auditServersBaseAudit(environment, servername, runtimeProperties, bApplyRequiredChanges)
    ##############################################################
    
    # OO based auditing atoms - automatically reported on...
    ##############################################################                 
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "JDBC URL - Siperian System DS", "/subsystem=datasources/xa-data-source=jdbc/siperian-cmx_system-ds/xa-datasource-properties=URL/", "value", runtimeProperties["targetDSUrl"], bApplyRequiredChanges))
    
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "App: Informatica Entity360View", "/deployment=entity360view-ear.ear/", "enabled", "true", False))
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "App: Informatica Mdm Platform", "/deployment=informatica-mdm-platform-ear.ear/", "enabled", "true", False))
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "App: Informatica Siperian Mrm", "/deployment=siperian-mrm.ear/", "enabled", "true", False))
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "App: Informatica Siperian Mrm Cleanse", "/deployment=siperian-mrm-cleanse.ear/", "enabled", "true", False))
    
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Transactions Default Timeout", "/subsystem=transactions/", "default-timeout", runtimeProperties["transactionsDefaultTimeout"], bApplyRequiredChanges))
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "HornetQ Security OFF", "/subsystem=messaging/hornetq-server=default/", "security-enabled", runtimeProperties["hornetq-security-enabled"], bApplyRequiredChanges))
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "HornetQ Persistence ON", "/subsystem=messaging/hornetq-server=default/", "persistence-enabled", runtimeProperties["hornetq-persistence-enabled"], bApplyRequiredChanges))
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Remoting-connector security-realm undefined", "/subsystem=remoting/connector=remoting-connector/", "security-realm", runtimeProperties["remoting-security-realm"], bApplyRequiredChanges))
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "EJB Pool threads", "/subsystem=ejb3/thread-pool=default/", "max-threads", runtimeProperties["targetCmdEjbStrictMaxPool"], bApplyRequiredChanges))
    
    ##############################################################
    # an auditObjectMolecule enables the user to group atoms together as one
    ############################################################## 
    oAuditObjectMolecule = auditObjectMolecule("Siperian System Datasource Pool Sizes", servername, True)
    oAuditObjectMolecule.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Siperian Datasource Pool Size (min)", "/subsystem=datasources/xa-data-source=jdbc/siperian-cmx_system-ds/", "min-pool-size", runtimeProperties["siperian-min-pool-size"], bApplyRequiredChanges))      
    oAuditObjectMolecule.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Siperian Datasource Pool Sizes (max)", "/subsystem=datasources/xa-data-source=jdbc/siperian-cmx_system-ds/", "max-pool-size", runtimeProperties["siperian-max-pool-size"], bApplyRequiredChanges))     
    
    oAuditObjectMolecule2 = auditObjectMolecule("Web Connections threads http(s)", servername, False)
    oAuditObjectMolecule2.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Web Connections threads (http)", "/subsystem=web/connector=http/", "max-connections", runtimeProperties["targetWebMaxConnections"], bApplyRequiredChanges))   
    oAuditObjectMolecule2.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Web Connections threads (https)", "/subsystem=web/connector=https/", "max-connections", runtimeProperties["targetWebMaxConnections"], bApplyRequiredChanges)) 
    
    oAuditObjectMolecule3 = auditObjectMolecule("Security Hardening - MDM", servername, True)              
    oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - Disable Welcome Page", "/subsystem=web/virtual-server=default-host/", "enable-welcome-root", runtimeProperties["enable-welcome-root"], bApplyRequiredChanges))
    oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - Remove Sample Web Alias", "/subsystem=web/virtual-server=default-host/", "alias", runtimeProperties["sampleWebAlias"], bApplyRequiredChanges))
    oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - Custom Server Header", "/system-property=org.apache.coyote.http11.Http11Protocol.SERVER/", "value", runtimeProperties["customServerHeader"], bApplyRequiredChanges))
    oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - X Powered By - JSP", "/subsystem=web/configuration=jsp-configuration/", "x-powered-by", runtimeProperties["x-powered-by"], bApplyRequiredChanges))
    oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - X Powered By - Catalina Connector", "/system-property=org.apache.catalina.connector.X_POWERED_BY/", "value", runtimeProperties["x-powered-by"], bApplyRequiredChanges))          
    oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - Utf8Encoding - URI_ENCODING", "/system-property=org.apache.catalina.connector.URI_ENCODING/", "value", runtimeProperties["URI_ENCODING"], bApplyRequiredChanges))
    oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - Utf8Encoding - USE_BODY_ENCODING_FOR_QUERY_STRING", "/system-property=org.apache.catalina.connector.USE_BODY_ENCODING_FOR_QUERY_STRING/", "value", runtimeProperties["USE_BODY_ENCODING_FOR_QUERY_STRING"], bApplyRequiredChanges))
#     oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - RestrictHttpMethods - Rewrite Flags", "/subsystem=web/virtual-server=default-host/rewrite=httpmethods/condition=condition-0/", "flags", runtimeProperties["rewrite-flags"], bApplyRequiredChanges))
#     oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - RestrictHttpMethods - Rewrite Pattern", "/subsystem=web/virtual-server=default-host/rewrite=httpmethods/condition=condition-0/", "pattern", runtimeProperties["rewrite-pattern"], bApplyRequiredChanges))
 
               
def auditServersMdm(environment, servers, propertiesDictionary, bApplyRequiredChanges) :
    # merge global properties into dict - deliberately overwriting local with global dict all values
 
    strThreadPoolId = "auditServersMDM"
    for servername in servers:
        # Create new threads
        scatterThread(strThreadPoolId, targetMethod=auditServersMdmThread, args=[environment, servername, propertiesDictionary, bApplyRequiredChanges])
 
    gatherThreads(strThreadPoolId)
 
    for servername in servers:
        auditReport(environment, servername)
