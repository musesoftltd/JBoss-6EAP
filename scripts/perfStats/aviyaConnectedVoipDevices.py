import datetime
from time import sleep

from library.jboss.jbossLibrary import getParameterValue
from library.util import appendToFile

username = "admin"
password = "admin123#"

serverList = {"localhost",
#             "127.0.0.1",
            }

# # enable EJB stats first...
# for servername in serverList:
#     cli = connectSilent(servername, username, password)
#     if (cli) :
#         result = issueCliCommand(cli, "/subsystem=ejb3:write-attribute(name=enable-statistics, value=true)")
#
#         print "cli include defaults complete..."
#     else :
#         print "CLI connection FAILED..."
#         exit()

datetimeSuffix = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H.%M.%S')
filename = "AviyaConnectedVoipDevices-" + datetimeSuffix + ".csv"

# Title for table
appendToFile("Aviya Connected VOIP Devices,", filename)
for servername in serverList:
    appendToFile(servername + ",", filename)

appendToFile("\n", filename)

while (1 == 1) :
    appendToFile(datetime.datetime.strftime(datetime.datetime.now(), '%H.%M.%S %Y-%m-%d') + ",", filename)
    for servername in serverList:
        maxPoolCountStr = getParameterValue(servername, username, password, "/deployment=prpc_j2ee14_jboss61JBM.ear/subdeployment=prbeans.jar/subsystem=ejb3/stateless-session-bean=EngineBMT/", "pool-max-size")

        currentPoolCountStr = getParameterValue(servername, username, password, "/deployment=prpc_j2ee14_jboss61JBM.ear/subdeployment=prbeans.jar/subsystem=ejb3/stateless-session-bean=EngineBMT/", "pool-available-count")
        maxPoolCount = int(maxPoolCountStr)
        currentPoolCount = int(currentPoolCountStr)
        inUsePoolCount = maxPoolCount - currentPoolCount
        print servername + " Aviya Connected User count:" + str(inUsePoolCount)
        appendToFile(str(inUsePoolCount) + ",", filename)
    appendToFile("\n", filename)

    # seconds
    sleep(15)
exit()
