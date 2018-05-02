'''
@author: ...
'''

from environmentProperties.allEnvs.propertiesPega import dictionary as globalDictionary
from library.auditing.auditServerBase import auditServersBaseAudit
from library.auditing.auditingLibrary import auditObjectAtoms, auditObjectAtom, \
    auditObjectMolecule
from library.jboss.jbossLibrary import connectSilent


global serversAlreadyBasePegaAudited
serversAlreadyBasePegaAudited = []

def auditServersBasePega(environment, servername, propertiesDictionary, bApplyRequiredChanges) :
    # merge global properties into dict - deliberately overwriting local with global dict all values
    runtimeProperties = dict()
    runtimeProperties.update(globalDictionary)
    runtimeProperties.update(propertiesDictionary)

    if connectSilent(servername, runtimeProperties["username"], runtimeProperties["password"]) == None:
        return
           
    ##############################################################
    # Base server audit...
    ##############################################################
    auditServersBaseAudit(environment, servername, runtimeProperties, bApplyRequiredChanges)
            
    ##############################################################
    # OO based auditing atoms - automatically reported on...
    ##############################################################
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Messaging Provider (Hornet Q)", "/subsystem=ejb3/", "default-resource-adapter-name", runtimeProperties["targetMessagingProvider"], bApplyRequiredChanges)) 
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "HornetQ Max Delivery Attempts", "/subsystem=messaging/hornetq-server=default/address-setting=#/", "max-delivery-attempts", runtimeProperties["targetHornetMaxdeliveryAttempts"], bApplyRequiredChanges))
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "HornetQ ReDelivery Delay", "/subsystem=messaging/hornetq-server=default/address-setting=#/", "redelivery-delay", runtimeProperties["targetHornetQRedeliveryDelay"], bApplyRequiredChanges))        
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "HornetQ Consumer Window Size", "/subsystem=messaging/hornetq-server=default/pooled-connection-factory=hornetq-ra/", "consumer-window-size", runtimeProperties["consumer-window-size"], bApplyRequiredChanges))        
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "uRandom RNG", "/core-service=platform-mbean/type=runtime", "input-arguments", runtimeProperties["uRandomRNG"], False))
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Pega User Home - Outside Container Folders", "/core-service=platform-mbean/type=runtime", "input-arguments", "-Duser.home", False))
    
    oAuditObjectMolecule = auditObjectMolecule("Bean Poola - Avaya VoIP (EJB) : " + str(runtimeProperties["targetEjbStrictMaxPool"]), servername, False)        
    oAuditObjectMolecule.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "EJB Pool maxsize: " + str(runtimeProperties["targetEjbStrictMaxPool"]), "/subsystem=ejb3/strict-max-bean-instance-pool=slsb-strict-max-pool/", "max-pool-size", runtimeProperties["targetEjbStrictMaxPool"], False))     

    oAuditObjectMolecule2 = auditObjectMolecule("Bean Pools - Avaya VoIP (MDB) : " + str(runtimeProperties["targetEjbStrictMaxPool"]), servername, False)        
    oAuditObjectMolecule2.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "MDB Pool maxsize: " + str(runtimeProperties["targetEjbStrictMaxPool"]), "/subsystem=ejb3/strict-max-bean-instance-pool=mdb-strict-max-pool/", "max-pool-size", runtimeProperties["targetEjbStrictMaxPool"], False))    

    oAuditObjectMolecule3 = auditObjectMolecule("Bean Pools - Avaya VoIP (Async / CTI) : ", servername, bApplyRequiredChanges)
    oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Async Pool minsize: " + str(runtimeProperties["AsyncConnectionFactory-min-pool-size"]), "/subsystem=messaging/hornetq-server=default/pooled-connection-factory=AsyncConnectionFactory/", "min-pool-size", runtimeProperties["AsyncConnectionFactory-min-pool-size"], bApplyRequiredChanges))    
    oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Async Pool maxsize: " + str(runtimeProperties["AsyncConnectionFactory-max-pool-size"]), "/subsystem=messaging/hornetq-server=default/pooled-connection-factory=AsyncConnectionFactory/", "max-pool-size", runtimeProperties["AsyncConnectionFactory-max-pool-size"], bApplyRequiredChanges))    
    oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "CTI thread Pool maxsize: " + str(runtimeProperties["targetEjbStrictMaxPool"]), "/subsystem=threads/bounded-queue-thread-pool=ctiThreadPool/", "max-threads", runtimeProperties["ctiThreadPool-maxThreads"], bApplyRequiredChanges))    

    oAuditObjectMolecule4 = auditObjectMolecule("Security Hardening - Pega", servername, True)        
    oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - Disable Welcome Page", "/subsystem=web/virtual-server=default-host/", "enable-welcome-root", runtimeProperties["enable-welcome-root"], bApplyRequiredChanges))
    oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - Remove Sample Web Alias", "/subsystem=web/virtual-server=default-host/", "alias", runtimeProperties["sampleWebAlias"], bApplyRequiredChanges))
    oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - Custom Server Header", "/system-property=org.apache.coyote.http11.Http11Protocol.SERVER/", "value", runtimeProperties["customServerHeader"], bApplyRequiredChanges))
    oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - X Powered By - JSP", "/subsystem=web/configuration=jsp-configuration/", "x-powered-by", runtimeProperties["x-powered-by"], bApplyRequiredChanges))
    oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - X Powered By - Catalina Connector", "/system-property=org.apache.catalina.connector.X_POWERED_BY/", "value", runtimeProperties["x-powered-by"], bApplyRequiredChanges))        
    oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - Utf8Encoding - URI_ENCODING", "/system-property=org.apache.catalina.connector.URI_ENCODING/", "value", runtimeProperties["URI_ENCODING"], bApplyRequiredChanges))
    oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - Utf8Encoding - USE_BODY_ENCODING_FOR_QUERY_STRING", "/system-property=org.apache.catalina.connector.USE_BODY_ENCODING_FOR_QUERY_STRING/", "value", runtimeProperties["USE_BODY_ENCODING_FOR_QUERY_STRING"], bApplyRequiredChanges))
                
        
