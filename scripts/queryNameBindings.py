from library.jboss.jbossLibrary import queryNameBindings


print '### Querying Servers...'
queryNameBindings('localhost', 'admin', 'admin123#')
print '### Querying Servers...end.'

exit()
