import datetime
from time import sleep

from library.jboss.jbossLibrary import getParameterValue, connectSilent, \
 issueCliCommand
from library.util import appendToFile

username = "admin"
password = "admin123#"

serverList = {"localhost",
              "127.0.0.1",
 }

for servername in serverList:
    cli = connectSilent(servername, username, password)
    if (cli) :
        result = issueCliCommand(cli, "/deployment=prpc_j2ee14_jboss61JBM.ear/subdeployment=pradapter.rar/subsystem=resource-adapters/statistics=statistics/connection-definitions=java\:\/eis\/PRAdapterConnectionFactory/:write-attribute(name=statistics-enabled,value=true)")
        print "cli stats enable complete..."
    else :
        print "CLI connection FAILED..."
        exit()

datetimeSuffix = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H.%M.%S')
filename = "ConnectionFactoryPool-" + datetimeSuffix + ".csv"
# Title for table
appendToFile("PRPC PRAdapterConnectionFactory In-Use,", filename)
for servername in serverList:
    appendToFile(servername + ",", filename)
appendToFile("\n", filename)

while (1 == 1) :
    appendToFile(datetime.datetime.strftime(datetime.datetime.now(), '%H.%M.%S %Y-%m-%d') + ",", filename)
    for servername in serverList:

        maxPoolCountStr = getParameterValue(servername, username, password, "/deployment=prpc_j2ee14_jboss61JBM.ear/subdeployment=pradapter.rar/subsystem=resource-adapters/ironjacamar=ironjacamar/resource-adapter=prpc_j2ee14_jboss61JBM.ear#pradapter/connection-definitions=eis\/PRAdapterConnectionFactory/", "max-pool-size") 
        currentPoolFreeStr = getParameterValue(servername, username, password, "/deployment=prpc_j2ee14_jboss61JBM.ear/subdeployment=pradapter.rar/subsystem=resource-adapters/statistics=statistics/connection-definitions=java\:\/eis\/PRAdapterConnectionFactory/", "AvailableCount")
        
        maxPoolCount = int(maxPoolCountStr)
        currentPoolFree = int(currentPoolFreeStr)
        inUsePoolCount = maxPoolCount - currentPoolFree

        print servername + " in use pool count:" + str(inUsePoolCount)
        appendToFile(str(inUsePoolCount) + ",", filename)

    appendToFile("\n", filename)

    # seconds
    sleep(15)
exit()
