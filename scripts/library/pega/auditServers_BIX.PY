'''
@author: ...
'''

from environmentProperties.allEnvs.propertiesPega import dictionary as globalDictionary
from library.auditing.auditingLibrary import auditObjectAtom, \
    auditObjectMolecule, auditReport, auditObjectAtoms
from library.jboss.jbossLibrary import getAllDataSources, connectSilent
from library.pega.auditServers_basePega import auditServersBasePega
from library.util import scatterThread, gatherThreads


def auditServersBIXThread(environment, servers, propertiesDictionary, bApplyRequiredChanges) :
    # merge global properties into dict - deliberately overwriting local with global dict all values
    runtimeProperties = dict()
    runtimeProperties.update(globalDictionary)
    runtimeProperties.update(propertiesDictionary)
       
    ##############################################################
    # Base server audit...
    ##############################################################
    auditServersBasePega(environment, servers, runtimeProperties, bApplyRequiredChanges)

    for servername in servers:
        
        if connectSilent(servername, runtimeProperties["username"], runtimeProperties["password"]) == None:
            return

        ##############################################################
        # OO based auditing atoms - automatically reported on...
        ##############################################################
        
        bAllMustPass = True
        AllDatasources = getAllDataSources(servername, runtimeProperties["username"], runtimeProperties["password"])
        if (AllDatasources) :
            auditObjectMolecule1 = auditObjectMolecule("JDBC URL", servername, bAllMustPass)
            for ds in AllDatasources:
                auditObjectMolecule1.auditObjectAtoms.append(auditObjectAtom(servername, runtimeProperties["username"], runtimeProperties["password"], "JDBC URL - " + ds, "/subsystem=datasources/data-source=" + ds + "/", "connection-url", runtimeProperties["targetDSUrl"], bApplyRequiredChanges))
            
        auditReport(environment, servername)

def auditServersBIX(environment, servers, propertiesDictionary, bApplyRequiredChanges) :
    # merge global properties into dict - deliberately overwriting local with global dict all values

    strThreadPoolId = "auditServersBIX"
    for servername in servers:
        # Create new threads
        scatterThread(strThreadPoolId, auditServersBIXThread, args=(environment, servername, propertiesDictionary, bApplyRequiredChanges))

    gatherThreads(strThreadPoolId)

    for servername in servers:
        auditReport(environment, servername)
