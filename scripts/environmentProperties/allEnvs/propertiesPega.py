'''
Created on 17 Oct 2016

@author: ...
'''
dictionary = {
    "AsyncConnectionFactory-min-pool-size" : "64",
    "AsyncConnectionFactory-max-pool-size" : "200",
    "targetWebMaxConnections" : "undefined",
    "targetManagementBindAddr" : "${jboss.bind.address.management:0.0.0.0}",
    "targetPublicBindAddr" : "${jboss.bind.address:0.0.0.0}",
    "targetMessagingProvider" : "${ejb.resource-adapter-name:hornetq-ra}",
    "targetHornetQRedeliveryDelay" : 0,
    "targetHornetMaxdeliveryAttempts" : 1,
    "targetAuditLoggingCustomHandler" : 'true',
    "targetRunState" : "running",
    "targetCustomLoggerLevel" : "ALL",
    "targetRootLoggerLevel" : "ALL",
    "targetEjbStrictMaxPool" : 400,
    "consumer-window-size" : "0",
    "AsyncConnectionFactory-min-pool-size" : "64",
    "AsyncConnectionFactory-max-pool-size" : "200",
    "ctiThreadPool-maxThreads" : 200,
    "exampleDSDataSourceMaxPoolSize" : 50,
    "uRandomRNG" : "-Djava.security.egd=file:/dev/./urandom",
    "jdbcTargetCheckValidConnectionSql" : "\"select 1 from dual\"",
    "jdbcValidateOnMatch" : "false",
    "jdbcBackgroundValidation" : "true",
    "jdbcBackgroundValidationMillis" : "60000",
    "jdbcUseFastFail" : "true",
    "jdbcExceptionSorterClassName" : "org.jboss.jca.adapters.jdbc.extensions.oracle.OracleExceptionSorter",
    "jdbcTrackStatements" : "NOWARN",
    "jdbcValidConnectionCheckerClassName" : "org.jboss.jca.adapters.jdbc.extensions.oracle.OracleValidConnectionChecker",
    "jdbcFlushStrategy" : "FailingConnectionOnly",
    "jdbcIdleTimeoutMinutes" : "5",
    "jdbcBlockingTimeoutWaitMillis" : "90000",
    "jdbcPoolPrefill" : "false",
    
    # Pega Application deployments
    "admVersionHash" : "[{\"hash\" => bytes { 0xe0, 0x32, 0x0f, 0x9a, 0x52, 0xe4, 0x78, 0x9a, 0xad, 0xee, 0x52, 0x7a, 0x3b, 0xa5, 0xbd, 0xd7, 0x77, 0xcc, 0x95, 0x59 }}]",
    "prpcVersionHash" : "[{\"hash\" => bytes { 0x01, 0x61, 0x4e, 0x9c, 0xac, 0xd7, 0x4a, 0x0f, 0x4a, 0x73, 0x85, 0x60, 0x7b, 0x38, 0xae, 0xc6, 0x96, 0xf7, 0xa5, 0x4d }}]",
    "prpcVersionHashDMZ" : "[{\"hash\" => bytes { 0x01, 0x61, 0x4e, 0x9c, 0xac, 0xd7, 0x4a, 0x0f, 0x4a, 0x73, 0x85, 0x60, 0x7b, 0x38, 0xae, 0xc6, 0x96, 0xf7, 0xa5, 0x4d }}]",
    "prsysmanageVersionHash" : "[{\"hash\" => bytes { 0x8d, 0xec, 0xec, 0xd3, 0x2e, 0xc5, 0x09, 0xf3, 0xf2, 0x15, 0x7c, 0x33, 0x62, 0xd6, 0x2c, 0x62, 0x4c, 0xad, 0x85, 0xdd }}]",
    "prgatewayVersionHash" : "[{\"hash\" => bytes { 0xd0, 0xfd, 0x6f, 0xe6, 0x57, 0x88, 0x8a, 0xf9, 0x18, 0x5b, 0xc2, 0x0a, 0x0b, 0x7b, 0xf7, 0x33, 0x1d, 0xf2, 0x50, 0x6b }}]",
    "prhelpVersionHash" : "[{\"hash\" => bytes { 0x91, 0x6c, 0xf1, 0x3c, 0xff, 0xc6, 0x74, 0xbc, 0x44, 0x65, 0xf7, 0x14, 0xfe, 0xdd, 0x1f, 0xdd, 0xf6, 0x2f, 0x79, 0xcd }}]",
    "vbdVersionHash" : "[{\"hash\" => bytes { 0x57, 0x19, 0x6f, 0xe9, 0x9f, 0xc4, 0xc3, 0xac, 0x23, 0x17, 0xaa, 0xa9, 0xc6, 0x10, 0xa6, 0x1c, 0xb1, 0xd0, 0x3d, 0x81 }}]",
    "mswarVersionHash" : "[{\"hash\" => bytes { 0x8d, 0x44, 0x39, 0x2e, 0x88, 0xf6, 0xe6, 0x1d, 0x61, 0x5e, 0x38, 0x2a, 0xac, 0xbd, 0xe8, 0xf8, 0xb6, 0x3b, 0xbe, 0xd2 }}]",
    
    # security hardening
    "x-powered-by" : "false",
    "rewrite-flags" : "NC",
    
    # base pega servers
    "rewrite-HttpMethods-substitution" : "-",
    "rewrite-HttpMethods-pattern" : ".*",
    "rewrite-HttpMethods-flags" : "F",
    "rewrite-HttpMethods-cond0test" : "%(REQUEST_METHOD)",    
    "rewrite-HttpMethods-cond0pattern" : "^(POUT|HEAD|DELETE|TRACE|TRACK|OPTIONS)$",    
    "rewrite-HttpMethods-cond0FLAGS" : "NC",    

    # marketing DMZ pega servers
    "rewrite-prweb-substitution1" : "/",
    "rewrite-prweb-pattern1" : "^/prweb/",
    "rewrite-prweb-flags1" : "nocase",
    "rewrite-prweb-substitution2" : "-",
    "rewrite-prweb-pattern2" : "^/prweb/",
    "rewrite-prweb-flags2" : "nocase",
    "rewrite-prweb-substitution3" : "/",
    "rewrite-prweb-pattern3" : "^/prweb/PRServlet(.*)",
    "rewrite-prweb-flags3" : "nocase",

    "Http11Protocol" : "NotAvailable",
    "URI_ENCODING" : "UTF-8",
    "USE_BODY_ENCODING_FOR_QUERY_STRING" : "true",
    "enable-welcome-root": "false",
    "sampleWebAlias": "[\"localhost\"]",
    "customServerHeader": "NotAvailable",
    
    # SSL Ciphers
    "sslProtocols" : "TLSv1.1,TLSv1.2",
    "cipherSuite" : "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256"
}
