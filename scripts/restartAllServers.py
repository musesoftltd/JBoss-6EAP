from library.jboss.jbossLibrary import restartServer


print '### Querying Servers...'
restartServer('localhost', 'admin', 'admin123#')
print '### Querying Servers...end.'

exit()
