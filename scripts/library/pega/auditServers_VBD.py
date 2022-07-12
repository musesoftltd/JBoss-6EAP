'''
Created on 20 Oct 2016

@author: ...
'''
from environmentProperties.allEnvs.propertiesPega import dictionary as globalDictionary
from library.auditing.auditingLibrary import reportingObject, \
    auditObjectAtom, auditObjectMolecule, auditObjectAtoms
from library.jboss.jbossLibrary import getAllDataSources, connectSilent
from library.pega.auditServers_basePega import auditServersBasePega
from library.util import scatterThread, gatherThreads


def auditServersVBDThread(environment, servername, propertiesDictionary, bApplyRequiredChanges) :
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
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "App: VBD Version", "/deployment=vbd.ear/", "content", runtimeProperties["vbdVersionHash"], False))
    
    bAllMustPass = True
    AllDatasources = getAllDataSources(servername, runtimeProperties["username"], runtimeProperties["password"])
    if (AllDatasources) :
        auditObjectMolecule1 = auditObjectMolecule("JDBC URL", servername, bAllMustPass)
        for ds in AllDatasources:
            auditObjectMolecule1.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "JDBC URL - Marketing - " + ds, "/subsystem=datasources/data-source=" + ds + "/", "connection-url", runtimeProperties["targetDSUrlMarketing"], bApplyRequiredChanges))

def auditServersVBD(environment, servers, propertiesDictionary, bApplyRequiredChanges) :
    # merge global properties into dict - deliberately overwriting local with global dict all values
    
    strThreadPoolId = "auditServersVBD"    
    for servername in servers:
        # Create new threads
        scatterThread(strThreadPoolId, auditServersVBDThread, args=(environment, servername, propertiesDictionary, bApplyRequiredChanges))
        
    gatherThreads(strThreadPoolId)

    for servername in servers:
        reportingObject.auditReport(environment, servername)

