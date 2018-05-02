'''
Created on 11 Oct 2016

@author: ...
'''
 
from environmentProperties.localhost.inventory import servers as localServers
from environmentProperties.localhost.properties import dictionary as localServerDictionary
from library.auditing.auditingLibrary import auditInitAudit
from library.pega.auditServers_CCI import auditServersCCI

auditInitAudit("localMachine", "pegaCCI")

# whether to allow the auditing framework to make changes to correct its findings...
applyChanges = False

auditServersCCI("Local Reference - Pega CCI", localServers, localServerDictionary, applyChanges)

exit()    
