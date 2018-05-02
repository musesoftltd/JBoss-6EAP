from library.jboss.jbossLibrary import applySecurity


print '### Querying Servers...'
applySecurity('localhost', 'admin', 'admin123#', 'myKeyPassword[hint: admin123#]', 'myKeyAlias', 'c:\\myKeyStoreLocation\\myKeyStore.p12')
print '### Querying Servers...end.'

exit()
