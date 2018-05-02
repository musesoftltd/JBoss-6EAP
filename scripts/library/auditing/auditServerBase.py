'''
@author: ...
'''
from environmentProperties.allEnvs.propertiesPega import dictionary as globalDictionary
from library.auditing.auditingLibrary import auditObjectAtom, auditObjectAtoms, \
    auditObjectMolecule
from library.jboss.jbossLibrary import getAllDataSources, getAllXaDataSources

def auditServersBaseAudit(environment, servername, propertiesDict, bApplyRequiredChanges) :
    # merge global propertiesDict into dict - deliberately overwriting local with global dict all values
    runtimeProperties = dict()
    runtimeProperties.update(globalDictionary)
    runtimeProperties.update(propertiesDict)

    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Running", "/", "server-state", runtimeProperties["targetRunState"], False))

    ##############################################################
    # OO based auditing atoms - automatically reported on...
    ##############################################################
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Custom Logger Exists", "/subsystem=logging/custom-handler=FILESIZEDATE/", "enabled", runtimeProperties["targetAuditLoggingCustomHandler"], bApplyRequiredChanges)) 
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Custom Logger Level (ALL)", "/subsystem=logging/custom-handler=FILESIZEDATE/", "level", runtimeProperties["targetCustomLoggerLevel"], bApplyRequiredChanges)) 
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Root Logging level (ALL)", "/subsystem=logging/root-logger=ROOT/", "level", runtimeProperties["targetRootLoggerLevel"], bApplyRequiredChanges)) 

    ##############################################################
    # an auditObjectMolecule enables the user to group atoms together as one
    ##############################################################
    oAuditObjectMolecule = auditObjectMolecule("Bind Addresses", servername, True)
    oAuditObjectMolecule.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Bind Addr Management", "/interface=management/", "inet-address", runtimeProperties["targetManagementBindAddr"], bApplyRequiredChanges))    
    oAuditObjectMolecule.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Bind Addr Public", "/interface=public/", "inet-address", runtimeProperties["targetPublicBindAddr"], bApplyRequiredChanges))                

    oAuditObjectMolecule2 = auditObjectMolecule("Security Hardening - Protocols-Suites", servername, True)
    oAuditObjectMolecule2.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "SSL Protocols", "/subsystem=web/connector=https/configuration=ssl/", "protocol", runtimeProperties["sslProtocols"], bApplyRequiredChanges))
    oAuditObjectMolecule2.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Cipher Suite", "/subsystem=web/connector=https/configuration=ssl/", "cipher-suite", runtimeProperties["cipherSuite"], bApplyRequiredChanges))

    allDatasourcesResponseResultList = getAllDataSources(servername, runtimeProperties["username"], runtimeProperties["password"])
    if (allDatasourcesResponseResultList) :
        oAuditObjectMolecule3 = auditObjectMolecule("Datasource (Non XA) Connection Perf Options", servername, True)
        for datasource in allDatasourcesResponseResultList :
            oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": check-valid-connection-sql", "/subsystem=datasources/data-source=" + datasource + "/", "check-valid-connection-sql", runtimeProperties["jdbcTargetCheckValidConnectionSql"], bApplyRequiredChanges))    
            oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": validate-on-match", "/subsystem=datasources/data-source=" + datasource + "/", "validate-on-match", runtimeProperties["jdbcValidateOnMatch"], bApplyRequiredChanges))    
            oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": background-validation", "/subsystem=datasources/data-source=" + datasource + "/", "background-validation", runtimeProperties["jdbcBackgroundValidation"], bApplyRequiredChanges))    
            oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": use-fast-fail", "/subsystem=datasources/data-source=" + datasource + "/", "use-fast-fail", runtimeProperties["jdbcUseFastFail"], bApplyRequiredChanges))    
            oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": exception-sorter-class-name", "/subsystem=datasources/data-source=" + datasource + "/", "exception-sorter-class-name", runtimeProperties["jdbcExceptionSorterClassName"], bApplyRequiredChanges))
            oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": track-statements", "/subsystem=datasources/data-source=" + datasource + "/", "track-statements", runtimeProperties["jdbcTrackStatements"], bApplyRequiredChanges))
            oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": valid-connection-checker-class-name", "/subsystem=datasources/data-source=" + datasource + "/", "valid-connection-checker-class-name", runtimeProperties["jdbcValidConnectionCheckerClassName"], bApplyRequiredChanges))
            oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": flush-strategy", "/subsystem=datasources/data-source=" + datasource + "/", "flush-strategy", runtimeProperties["jdbcFlushStrategy"], bApplyRequiredChanges))
            oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": idle-timeout-minutes", "/subsystem=datasources/data-source=" + datasource + "/", "idle-timeout-minutes", runtimeProperties["jdbcIdleTimeoutMinutes"], bApplyRequiredChanges))
            oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": blocking-timeout-wait-millis", "/subsystem=datasources/data-source=" + datasource + "/", "blocking-timeout-wait-millis", runtimeProperties["jdbcBlockingTimeoutWaitMillis"], bApplyRequiredChanges))
            oAuditObjectMolecule3.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": pool-prefill", "/subsystem=datasources/data-source=" + datasource + "/", "pool-prefill", runtimeProperties["jdbcPoolPrefill"], bApplyRequiredChanges))

    allDatasourcesResponseResultListXa = getAllXaDataSources(servername, runtimeProperties["username"], runtimeProperties["password"])
    if (allDatasourcesResponseResultListXa) :
        oAuditObjectMolecule4 = auditObjectMolecule("Datasource (XA) Connection Perf Options", servername, True)
        for datasource in allDatasourcesResponseResultListXa :
            oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": check-valid-connection-sql", "/subsystem=datasources/xa-data-source=" + datasource + "/", "check-valid-connection-sql", runtimeProperties["jdbcTargetCheckValidConnectionSql"], bApplyRequiredChanges))    
            oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": validate-on-match", "/subsystem=datasources/xa-data-source=" + datasource + "/", "validate-on-match", runtimeProperties["jdbcValidateOnMatch"], bApplyRequiredChanges))    
            oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": background-validation", "/subsystem=datasources/xa-data-source=" + datasource + "/", "background-validation", runtimeProperties["jdbcBackgroundValidation"], bApplyRequiredChanges))    
            oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": use-fast-fail", "/subsystem=datasources/xa-data-source=" + datasource + "/", "use-fast-fail", runtimeProperties["jdbcUseFastFail"], bApplyRequiredChanges))    
            oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": exception-sorter-class-name", "/subsystem=datasources/xa-data-source=" + datasource + "/", "exception-sorter-class-name", runtimeProperties["jdbcExceptionSorterClassName"], bApplyRequiredChanges))
            oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": track-statements", "/subsystem=datasources/xa-data-source=" + datasource + "/", "track-statements", runtimeProperties["jdbcTrackStatements"], bApplyRequiredChanges))
            oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": valid-connection-checker-class-name", "/subsystem=datasources/xa-data-source=" + datasource + "/", "valid-connection-checker-class-name", runtimeProperties["jdbcValidConnectionCheckerClassName"], bApplyRequiredChanges))
            oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": flush-strategy", "/subsystem=datasources/xa-data-source=" + datasource + "/", "flush-strategy", runtimeProperties["jdbcFlushStrategy"], bApplyRequiredChanges))
            oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": idle-timeout-minutes", "/subsystem=datasources/xa-data-source=" + datasource + "/", "idle-timeout-minutes", runtimeProperties["jdbcIdleTimeoutMinutes"], bApplyRequiredChanges))
            oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": blocking-timeout-wait-millis", "/subsystem=datasources/xa-data-source=" + datasource + "/", "blocking-timeout-wait-millis", runtimeProperties["jdbcBlockingTimeoutWaitMillis"], bApplyRequiredChanges))
            oAuditObjectMolecule4.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], datasource + ": pool-prefill", "/subsystem=datasources/xa-data-source=" + datasource + "/", "pool-prefill", runtimeProperties["jdbcPoolPrefill"], bApplyRequiredChanges))
