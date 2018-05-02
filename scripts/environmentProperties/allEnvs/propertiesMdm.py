'''
Created on 4 Apr 2017

@author: x
'''

dictionary = {
    "transactionsDefaultTimeout" : "3600",
    "hornetq-security-enabled" : "false",
    "hornetq-persistence-enabled" : "true",
    "remoting-security-realm" : "undefined",
    "siperian-min-pool-size" : 50,
    "siperian-max-pool-size" : 500,
    "targetCmdEjbStrictMaxPool" : 300,
    "consumer-window-size" : "0",
    "AsyncConnectionFactory-min-pool-size" : "64",
    "AsyncConnectionFactory-max-pool-size" : "200",
    "ctiThreadPool-maxThreads" : 200,
    "httpsScheme" : "https",
    "targetAuditLoggingCustomHandler" : 'true',
    "targetCustomLoggerLevel" : "ALL",
    "targetEjbStrictMaxPool" : 250,
    "targetEjbStrictMaxPool2" : 260,
    "targetEjbStrictMaxPool3" : 400,
    "targetHornetMaxdeliveryAttempts" : 1,
    "targetHornetQRedeliveryDelay" : 0,
    "targetManagementBindAddr" : "${jboss.bind.address.management:0.0.0.0}",
    "targetPublicBindAddr" : "${jboss.bind.address:0.0.0.0}",
    "targetMessagingProvider" : "${ejb.resource-adapter-name:hornetq-ra}",
    "targetRootLoggerLevel" : "INFO",
    "targetRunState" : "running",
    "targetWebMaxConnections" : "undefined",
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
    
    # security hardening
    "x-powered-by" : "false",
    "rewrite-pattern" : "^(PUT|HEAD|DELETE|TRACE|TRACK|OPTIONS)$",
    "rewrite-flags" : "NC",
    "Http11Protocol" : "NotAvailable",
    "URI_ENCODING" : "UTF-8",
    "USE_BODY_ENCODING_FOR_QUERY_STRING" : "true",
    "enable-welcome-root": "false",
    "sampleWebAlias": "[\"localhost\"]",
    "customServerHeader": "NotAvailable",
    
    # SSL Ciphers
    "sslProtocols" : "TLSv1,TLSv1.1,TLSv1.2",
    "cipherSuite" : "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256"

}
