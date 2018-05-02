'''
Created on 11 Oct 2016

@author: ...
'''
 


from environmentProperties.localhost.inventory import servers as localServers
from environmentProperties.localhost.properties import dictionary as localServerDictionary
from library.auditing.auditingLibrary import auditInitAudit
from library.informatica.auditServersMdm import auditServersMdm


auditInitAudit("localMachine", "MDM")

# whether to allow the auditing framework to make changes to correct its findings...
applyChanges = False

auditServersMdm("Local Reference - MDM", localServers, localServerDictionary, applyChanges)

exit()    
