'''
Created on 20 Oct 2016

@author: ...
'''
from environmentProperties.allEnvs.propertiesPega import dictionary as globalDictionary
from library.auditing.auditingLibrary import auditObjectAtom, \
    auditObjectMolecule, reportingObject, auditObjectAtoms
from library.jboss.jbossLibrary import getAllDataSources, connectSilent
from library.pega.auditServers_basePega import auditServersBasePega
from library.util import scatterThread, gatherThreads


def auditServersMarketingDMZThread(environment, servername, propertiesDictionary, bApplyRequiredChanges) :
    # merge global properties into dict - deliberately overwriting local with global dict all values
    runtimeProperties = dict()
    runtimeProperties.update(globalDictionary)
    runtimeProperties.update(propertiesDictionary)

    if connectSilent(servername, runtimeProperties["username"], runtimeProperties["password"]) == None:
        return
           
    ##############################################################
    # Base server audit...
    ##############################################################
    auditServersBasePega(environment, servername, runtimeProperties, bApplyRequiredChanges)
        
    ##############################################################
    # OO based auditing atoms - automatically reported on...
    ##############################################################
    oAuditObjectMolecule = auditObjectMolecule("Bind Addresses", servername, True)
    oAuditObjectMolecule.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Bind Addr Management", "/interface=management/", "inet-address", "${jboss.bind.address.management:" + servername + ".theaa.local}", bApplyRequiredChanges))    
    oAuditObjectMolecule.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Bind Addr Public", "/interface=public/", "inet-address", runtimeProperties["targetPublicBindAddr"], bApplyRequiredChanges))                
    
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "App: prsysmgmt Version", "/deployment=prsysmgmt_jboss.ear/", "content", runtimeProperties["prsysmanageVersionHash"], False))
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "App: PRPC Version", "/deployment=prpc_j2ee14_jboss61JBM.ear/", "content", runtimeProperties["prpcVersionHashDMZ"], False))

    oAuditObjectMolecule2 = auditObjectMolecule("Security Hardening DMZ", servername, True)    
    oAuditObjectMolecule2.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - PRWeb Disabled - substitution1", "/subsystem=web/virtual-server=default-host/rewrite=rule-1", "substitution", runtimeProperties["rewrite-prweb-substitution1"], bApplyRequiredChanges))
    oAuditObjectMolecule2.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - PRWeb Disabled - pattern1", "/subsystem=web/virtual-server=default-host/rewrite=rule-1", "pattern", runtimeProperties["rewrite-prweb-pattern1"], bApplyRequiredChanges))
    oAuditObjectMolecule2.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - PRWeb Disabled - flags1", "/subsystem=web/virtual-server=default-host/rewrite=rule-1", "flags", runtimeProperties["rewrite-prweb-flags1"], bApplyRequiredChanges))
    
    oAuditObjectMolecule2.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - PRWeb Disabled - substitution2", "/subsystem=web/virtual-server=default-host/rewrite=rule-2", "substitution", runtimeProperties["rewrite-prweb-substitution2"], bApplyRequiredChanges))
    oAuditObjectMolecule2.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - PRWeb Disabled - pattern2", "/subsystem=web/virtual-server=default-host/rewrite=rule-2", "pattern", runtimeProperties["rewrite-prweb-pattern2"], bApplyRequiredChanges))
    oAuditObjectMolecule2.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - PRWeb Disabled - flags2", "/subsystem=web/virtual-server=default-host/rewrite=rule-2", "flags", runtimeProperties["rewrite-prweb-flags2"], bApplyRequiredChanges))
    
    oAuditObjectMolecule2.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - PRWeb Disabled - substitution3", "/subsystem=web/virtual-server=default-host/rewrite=rule-3", "substitution", runtimeProperties["rewrite-prweb-substitution3"], bApplyRequiredChanges))
    oAuditObjectMolecule2.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - PRWeb Disabled - pattern3", "/subsystem=web/virtual-server=default-host/rewrite=rule-3", "pattern", runtimeProperties["rewrite-prweb-pattern3"], bApplyRequiredChanges))
    oAuditObjectMolecule2.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "Security Hardening - PRWeb Disabled - flags3", "/subsystem=web/virtual-server=default-host/rewrite=rule-3", "flags", runtimeProperties["rewrite-prweb-flags3"], bApplyRequiredChanges))
    
    bAllMustPass = True
    AllDatasources = getAllDataSources(servername, runtimeProperties["username"], runtimeProperties["password"])
    if (AllDatasources) :
        auditObjectMolecule1 = auditObjectMolecule("JDBC URL", servername, bAllMustPass)
        for ds in AllDatasources:
            auditObjectMolecule1.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "JDBC URL - Marketing DMZ - " + ds, "/subsystem=datasources/data-source=" + ds + "/", "connection-url", runtimeProperties["targetDSUrlMarketing"], bApplyRequiredChanges))            

def auditServersMarketingDMZ(environment, servers, propertiesDictionary, bApplyRequiredChanges) :
    # merge global properties into dict - deliberately overwriting local with global dict all values
    
    strThreadPoolId = "auditServersMarketingDMZ"    
    for servername in servers:
        # Create new threads
        scatterThread(strThreadPoolId, auditServersMarketingDMZThread, args=(environment, servername, propertiesDictionary, bApplyRequiredChanges))

    gatherThreads(strThreadPoolId)

    for servername in servers:
        reportingObject.auditReport(environment, servername)
