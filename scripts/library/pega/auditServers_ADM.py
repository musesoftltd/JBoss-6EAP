'''
@author: ...
'''
from environmentProperties.allEnvs.propertiesPega import dictionary as globalDictionary
from library.auditing.auditingLibrary import \
    auditObjectAtom, auditObjectMolecule, auditObjectAtoms, reportingObject
from library.jboss.jbossLibrary import getAllDataSources, connectSilent
from library.pega.auditServers_basePega import auditServersBasePega
from library.util import scatterThread, gatherThreads


def auditServersADMThread(environment, servername, propertiesDictionary, bApplyRequiredChanges) :
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
        
    auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "App: ADM Version", "/deployment=adm7.ear/", "content", runtimeProperties["admVersionHash"], False))

    bAllMustPass = True
    AllDatasources = getAllDataSources(servername, runtimeProperties["username"], runtimeProperties["password"])
    if (AllDatasources) :
        auditObjectMolecule1 = auditObjectMolecule("JDBC URL", servername, bAllMustPass)
        for ds in AllDatasources:
            auditObjectMolecule1.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "JDBC URL - Marketing -" + ds, "/subsystem=datasources/data-source=" + ds + "/", "connection-url", runtimeProperties["targetDSUrlMarketing"], bApplyRequiredChanges))
    
def auditServersADM(environment, servers, propertiesDictionary, bApplyRequiredChanges) :
    # merge global properties into dict - deliberately overwriting local with global dict all values
    
    strThreadPoolId = "auditServersADM"
    for servername in servers:
        # Create new threads
        scatterThread(strThreadPoolId, targetMethod=auditServersADMThread, args=[environment, servername, propertiesDictionary, bApplyRequiredChanges]) 

    gatherThreads(strThreadPoolId)

    for servername in servers:
        reportingObject.auditReport(environment, servername)
