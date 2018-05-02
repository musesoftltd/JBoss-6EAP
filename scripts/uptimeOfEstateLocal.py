
from inventoryLocal import servers
from library.jboss.jbossLibrary import checkUptime

def invoke (servername):
    checkUptime(servername, 'admin', 'admin123#')

for server in servers :
    invoke(server)
exit()
