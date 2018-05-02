'''
Created on 11 Oct 2016

@author: ...
'''
 
from environmentProperties.localhost.inventory import servers as localServers
from environmentProperties.localhost.properties import dictionary as localServerDictionary
from library.auditing.auditingLibrary import auditInitAudit
from library.pega.auditServers_MarketingDMZ import auditServersMarketingDMZ

auditInitAudit("localMachine", "pegaDMZ")

# whether to allow the auditing framework to make changes to correct its findings...
applyChanges = False

auditServersMarketingDMZ("Local Reference - Pega CCI", localServers, localServerDictionary, applyChanges)

exit()    
